import requests
from getpass import getpass
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Device():
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.interface_list = []
        self.get_device_info()
        self.get_interface_list()
        self.get_interface_configs()

    def get_device_info(self):
        data = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "format": "json",
            "timestamps": False,
            "autoComplete": False,
            "expandAliases": False,
            "cmds": [
            "enable", "copy running-config startup-config", "show version", "show hostname"
            ],
            "version": 1
        },
        "id": "EapiExplorer-1"
        } 
        
        response = requests.post(url='http://{0}:{1}@127.0.0.1/command-api'.format(self.username,self.password), data=json.dumps(data), verify=False)
        device_info = json.loads(response.content)['result'][2]
        hostname = json.loads(response.content)['result'][3]
        
        self.mac_address = device_info['systemMacAddress']
        self.fqdn = hostname['fqdn']

    
    def get_interface_list(self):
        data = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "format": "json",
            "timestamps": False,
            "autoComplete": False,
            "expandAliases": False,
            "cmds": [
            "show interfaces status"
            ],
            "version": 1
        },
        "id": "EapiExplorer-1"
        } 
        
        response = requests.post(url='https://{0}:{1}@10.255.255.201/command-api'.format(self.username,self.password), data=json.dumps(data), verify=False)
        interfaces_dict = json.loads(response.content)['result'][0]['interfaceStatuses']

        for interface in interfaces_dict:
            if 'vlan' not in interface and 'MANAGEMENT' not in interface.upper():
                self.interface_list.append(interface)


    def get_interface_configs(self):
        
        commands = ["enable"]
        
        for interface in self.interface_list:
            commands.append('show running-config interfaces {0}'.format(interface))

        data = {
        "jsonrpc": "2.0",
        "method": "runCmds",
        "params": {
            "format": "text",
            "timestamps": False,
            "autoComplete": False,
            "expandAliases": False,
            "cmds": commands,
            "version": 1
        },
        "id": "EapiExplorer-1"
        } 

        response = requests.post(url='https://{0}:{1}@10.255.255.201/command-api'.format(self.username,self.password), data=json.dumps(data), verify=False)
        configs = json.loads(response.content)['result']

        self.final_config = ""
        for config in configs:
            self.final_config += config['output']+"!\n"
        
        
        
        
