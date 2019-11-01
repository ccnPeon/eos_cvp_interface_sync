import requests
from getpass import getpass
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from device import Device

###################Define Global Variables###################
username = raw_input('Please enter your username: ')
password = getpass('Please enter your password: ')
cvp_server = '10.0.0.14'
api_headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    }
api_root = 'https://%s/cvpservice' % cvp_server
#############################################################

def authenticate():
	url_path = api_root+'/login/authenticate.do'
	payload = { "userId": username,
				"password" : password
			}
	
	response = requests.post(url=url_path, data=json.dumps(payload), headers=api_headers, verify=False)
	return(response.cookies)
	
def get_configlets(cookies):
    url_path = api_root+'/configlet/getConfiglets.do?startIndex=0&endIndex=0'
    response = requests.get(url=url_path, headers=api_headers, cookies=cookies, verify=False)
    configlets = json.loads(response.content)['data']
    return(configlets)

def update_configlet(config,key,name,cookies):
    url_path = api_root+'/configlet/updateConfiglet.do'
    data = {
      "config": config,
      "key": key,
      "name": name,
      "waitForTaskIds": False,
      "reconciled": False
    }
	
    response = requests.post(url=url_path, headers=api_headers, data = json.dumps(data), cookies=cookies, verify=False)
    print(response.content)



def main():
    cookies = authenticate()
    device = Device(username,password)
    configlet_name = device.fqdn+'_Interfaces'
    configlets = get_configlets(cookies)


    for configlet in configlets:
        if configlet['name'] == configlet_name:
            configlet_key = configlet['key']

    update_configlet(config=device.final_config, key=configlet_key, name=configlet_name, cookies=cookies)


if __name__ == '__main__':
    main()
