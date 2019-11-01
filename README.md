# EOS CVP Interface Sync
The purpose of this script will be to get the interface running configuration from the local device and update a device specific configlet within CVP to allow for local switchport changes to be quickly replicated to CVP.

The script will prompt for your CVP username/password upon execution. This will be the user that is notated in the creation of the CVP Task. The task will not be execute and should not perform a change on the interfaces.

This script will also copy running configuration to startup

### Prerequisites
* CVP Configlet that matches the name of <switch_hostname>_Interfaces

### Setup
#### 1. Within the "cvp_sync.py" file, update the CVP server address.
#### 2. Copy eos_cvp_interface_sync folder to '/mnt/flash' on a switch
#### 3. Create an alias on the switch with the following command:
* alias <chosen_alias> bash sudo ip netns exec ns-<management_vrf> python /mnt/flash/eos_cvp_interface_sync/cvp_sync.py'
* Note: In my example I will use the alias 'syncconfig' with the management vrf of 'MGMT'
* Example alias: alias syncconfig bash sudo ip netns exec ns-MGMT python /mnt/flash/eos_cvp_sync/cvp_sync.py


### Example
```
switch#syncconfig
Please enter your username: cvpadmin
Please enter your password:
{"data":"Configlet DCA-Leaf1_Interfaces successfully updated and task initiated."}
```