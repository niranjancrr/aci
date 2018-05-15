from Logger import Logger
import time

class VM:

    def __init__(self):
        self.log = Logger()
        self.log.info('Initializing Vcenter VM Class')

    def power_off_vm(self,datacenterName,vmName):
        '''
            Powers off the specified VM based on the VM name and the Datacenter on which it resides
            arg1 : Datacenter Name under which the VM resides
            arg2 : Name of the Virtual Machine
        '''
        try:
            vm_mo = self.get_vm_mo_by_datacenter(datacenterName,vmName)
            self.log.info('Powering off VM {} under Datacenter {}' .format(vmName, datacenterName))
            status = vm_mo.PowerOffVM_Task()
            counter = 5
            while status.info.state != 'success':
                print "Sleeping for {} secs before retrying" .format(counter)
                time.sleep(counter)
            self.log.info('Power off Task for VM {} under Datacenter {} is Complete' .format(vmName, datacenterName))
            return True
        except:
            self.log.error('Failed to Power off VM {} under Datacenter {}' .format(vmName, datacenterName))
            return False

    def power_on_vm(self,datacenterName,vmName):
        '''
            Powers on the specified VM based on the VM name and the Datacenter on which it resides
            arg1 : Datacenter Name under which the VM resides
            arg2 : Name of the Virtual Machine
        '''
        try:
            vm_mo = self.get_vm_mo_by_datacenter(datacenterName,vmName)
            self.log.info('Powering on VM {} under Datacenter {}' .format(vmName, datacenterName))
            status = vm_mo.PowerOnVM_Task()
            counter = 5
            while status.info.state != 'success':
                print "Sleeping for {} secs before retrying" .format(counter)
                time.sleep(counter)
            self.log.info('Power on Task for VM {} under Datacenter {} is Complete' .format(vmName, datacenterName))
            return True
        except:
            self.log.error('Failed to Power on VM {} under Datacenter {}' .format(vmName, datacenterName))
            return False

    def rename_vm(self,datacenterName,vmOldName,vmNewName):
        '''
            Changes the specified VM's name based on the VM's old name and the Datacenter on which it resides
            arg1 : Datacenter Name under which the VM resides
            arg2 : Current Name of the Virtual Machine
            arg3 : New Name for the Virtual Machine
        '''
        try:
            vm_mo = self.get_vm_mo_by_datacenter(datacenterName,vmOldName)
            self.log.info('Renaming VM {} under Datacenter {} to {}' .format(vmOldName, datacenterName, vmNewName))
            status = vm_mo.Rename_Task(vmNewName)
            counter = 5
            while status.info.state != 'success':
                print "Sleeping for {} secs before retrying" .format(counter)
                time.sleep(counter)
            self.log.info('Rename Task for VM {} under Datacenter {} to {} is Complete' .format(vmOldName, datacenterName, vmNewName))
            return True
        except:
            self.log.error('Failed to Rename VM {} under Datacenter {} to {}' .format(vmOldName, datacenterName, vmNewName))
            return False
