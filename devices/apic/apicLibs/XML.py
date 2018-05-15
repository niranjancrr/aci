import sys
import lxml.etree as etree
from ApicPost import Post

class XML(Post):

    def __init__(self):
        self.log.info('Initializing XML class')
        Post.__init__(self)

    #Decorator to print XML
    #def xmlprint(function):
    #    def wrapper(*args,**kwargs):
    #        print '=' * 50
    #        print "\t XML Post : {} \t" .format(function.__name__)
    #        print '=' * 50
    #        xml_str = function(*args,**kwargs)
    #        xml = etree.fromstring(xml_str)
    #        print etree.tostring(xml, pretty_print = True)
            #return xml_str
    #    return wrapper

    def pretty_print(self,xml_str,function_name=''):
        self.log.info('\n')
        self.log.info('=' * 50)
        self.log.info("\t XML Post : {} \t" .format(function_name))
        self.log.info('=' * 50)
        xml = etree.fromstring(xml_str)
        self.log.info(etree.tostring(xml, pretty_print = True))
        self.log.info('\n')

    #Post to create a Tenant
    #@xmlprint
    def createTenant(self,tenantName):
        '''
            Creates Tenant in the current Apic
            arg1 : Tenant name as a string
        '''
        pathDn = "uni/tn-{}" .format(tenantName)
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvTenant descr="" dn="'+pathDn+'" name="'+tenantName+'" nameAlias="" ownerKey="" ownerTag="">'+\
                    '<vnsSvcCont />'+\
                    '<fvRsTenantMonPol tnMonEPGPolName="" />'+\
                '</fvTenant>'
        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to delete a Tenant
    #@xmlprint
    def deleteTenant(self,tenantName):
        '''
            Deletes Tenant from the current Apic
            arg1 : Tenant name as a string
        '''
        pathDn = "uni/tn-{}" .format(tenantName)
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvTenant descr="" dn="'+pathDn+'" name="'+tenantName+'" status="deleted">'+\
                 '</fvTenant>'
        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to create Application Profile
    #@xmlprint
    def createApplicationProfile(self,tenantName,apName):
        '''
            Creates AP on the current Apic
            arg1 : Tenant name as a string
            arg2 : Application Profile name as a string
        '''

        pathDn = "uni/tn-{}" .format(tenantName)

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvTenant descr="" dn="'+pathDn+'" name="'+tenantName+'" nameAlias="" ownerKey="" ownerTag="">'+\
                        '<vnsSvcCont />'+\
                        '<fvRsTenantMonPol tnMonEPGPolName="" />'+\
                        '<fvAp descr="" name="'+apName+'" nameAlias="" ownerKey="" ownerTag="" prio="unspecified" />'+\
                    '</fvTenant>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to delete an Application Profile
    #@xmlprint
    def deleteApplicationProfile(self,tenantName,apName):
        '''
            Deletes an AP on the current Apic
            arg1 : Tenant name as a string
            arg2 : Application Profile name as a string
        '''

        pathDn = "uni/tn-{}" .format(tenantName)

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvTenant descr="" dn="'+pathDn+'" name="'+tenantName+'">'+\
                        '<fvAp descr="" name="'+apName+'" status="deleted" />'+\
                    '</fvTenant>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to create VRF
    #@xmlprint
    def createVrf(self,tenantName,vrfName):
        '''
            Creates a VRF on the current Apic
            arg1 : Tenant name as a string
            arg2 : VRF name as a string
        '''

        pathDn = "uni/tn-{}" .format(tenantName)

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvTenant descr="" dn="'+pathDn+'" name="'+tenantName+'" nameAlias="" ownerKey="" ownerTag="">'+\
                        '<vnsSvcCont />'+\
                        '<fvRsTenantMonPol tnMonEPGPolName="" />'+\
                        '<fvCtx bdEnforcedEnable="no" descr="" knwMcastAct="permit" name="'+vrfName+'" nameAlias="" ownerKey="" ownerTag="" pcEnfDir="ingress" pcEnfPref="enforced">'+\
                        '<fvRsVrfValidationPol tnL3extVrfValidationPolName="" />'+\
                            '<vzAny descr="" matchT="AtleastOne" name="" nameAlias="" prefGrMemb="disabled" />'+\
                            '<fvRsOspfCtxPol tnOspfCtxPolName="" />'+\
                            '<fvRsCtxToEpRet tnFvEpRetPolName="" />'+\
                            '<fvRsCtxToExtRouteTagPol tnL3extRouteTagPolName="" />'+\
                            '<fvRsBgpCtxPol tnBgpCtxPolName="" />'+\
                        '</fvCtx>'+\
                     '</fvTenant>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to delete a VRF 
    #@xmlprint
    def deleteVrf(self,tenantName,vrfName):
        '''
            Deletes a VRF on the current Apic
            arg1 : Tenant name as a string
            arg2 : VRF name as a string
        '''

        pathDn = "uni/tn-{}" .format(tenantName)

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvTenant descr="" dn="'+pathDn+'" name="'+tenantName+'">'+\
                        '<fvCtx name="'+vrfName+'" status="deleted">'+\
                        '</fvCtx>'+\
                     '</fvTenant>'
        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to create a BD
    #@xmlprint
    def createBD(self,tenant,vrfName,bdName,bdSubnet):
        '''
            Creates a BD on the current Apic
            arg1 : Tenant name as a string
            arg2 : VRF name as a string
            arg3 : BD name as a string
            arg4 : BD subnet as a string
        '''
        pathDn = str("uni/tn-" + tenant + "/BD-" + bdName)
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvBD arpFlood="yes" descr="" dn="'+pathDn+'" epMoveDetectMode="" limitIpLearnToSubnets="no" multiDstPktAct="bd-flood" name="'+bdName+'" ownerKey="" ownerTag="" unicastRoute="yes" unkMacUcastAct="proxy" unkMcastAct="flood" vmac="not-applicable">'+\
                    '<fvRsBDToNdP tnNdIfPolName="" />'+\
                    '<fvRsCtx tnFvCtxName="'+vrfName+'" />'+\
                    '<fvRsIgmpsn tnIgmpSnoopPolName="" />'+\
                    '<fvSubnet ctrl="" descr="" ip="'+bdSubnet+'" name="" preferred="no" scope="private" virtual="no" />'+\
                    '<fvRsBdToEpRet resolveAct="resolve" tnFvEpRetPolName="" />'+\
                '</fvBD>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to delete a BD
    def deleteBD(self,tenant,bdName):

        pathDn = str("uni/tn-" + tenant + "/BD-" + bdName)
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvBD dn="'+pathDn+'" name="'+bdName+'" status="deleted" />'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to create an EPG
    #@xmlprint
    def createEPG(self,tenant,ap,epgName,bdName,vmmName='mininet'):
        '''
            Creates an EPG on the current Apic
            arg1 : Tenant name as a string
            arg2 : AP name as a string
            arg3 : EPG name as a string
            arg4 : BD name as a string
            arg5 : VMM domain name as a string
        '''
        pathDn = str("uni/tn-" + tenant + "/ap-" + ap + "/epg-" + epgName)
        pathDn2 = str("uni/vmmp-VMware/dom-" + vmmName)

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvAEPg descr="" dn="'+pathDn+'" isAttrBasedEPg="no" matchT="AtleastOne" name="'+epgName+'" prio="unspecified">'+\
                    '<fvRsDomAtt encap="unknown" instrImedcy="immediate" resImedcy="immediate" tDn="'+pathDn2+'" />'+\
                    '<fvRsCustQosPol tnQosCustomPolName="" />'+\
                    '<fvRsBd tnFvBDName="'+bdName+'" />'+\
                '</fvAEPg>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to delete an EPG
    def deleteEPG(self,tenant,ap,epgName):
        '''
            Creates an EPG on the current Apic
            arg1 : Tenant name as a string
            arg2 : AP name as a string
            arg3 : EPG name as a string
        '''

        pathDn = str("uni/tn-" + tenant + "/ap-" + ap + "/epg-" + epgName)
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvAEPg descr="" dn="'+pathDn+'" name="'+epgName+'" status="deleted" />'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #Post to change EPG level encap type, deployment immediacy and resolution immediacy
    #@xmlprint
    def change_encap_and_immediacy_epg(self,tenant,ap,epgName,vmmName='mininet',encapmode='auto',deployImmediacy='immediate',resImmediacy='immediate'):
        '''
            Change the encap type of specified EPG on current Apic
            Valid encap modes are 'auto', 'vlan', 'vxlan'
            Valid Deployment immediacy : 'on demand' and 'immediate'
            Valid Resolution immediacy : 'on demand' and 'immediate'
            arg1 : Tenant name as a string
            arg2 : AP name as a string
            arg3 : EPG name as a string
            arg4 : VMM domain name as a string
            arg5 : encap mode as a string
        '''

        pathDn = str('uni/tn-{}/ap-{}/epg-{}/rsdomAtt-[uni/vmmp-VMware/dom-{}]'.format(tenant,ap,epgName,vmmName))
        pathDn2 = str('uni/vmmp-VMware/dom-{}'.format(vmmName))

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        #xml_data += '<fvRsDomAtt classPref="encap" delimiter="" dn="'+pathDn+'" encap="unknown" encapMode="'+encapmode+'" epgCos="Cos0" epgCosPref="disabled" instrImedcy="'+deployImmediacy+'" netflowDir="both" netflowPref="disabled" primaryEncap="unknown" primaryEncapInner="unknown" resImedcy="'+resImmediacy+'" secondaryEncapInner="unknown" switchingMode="native" tDn="'+pathDn2+'" />'
        xml_data += '<fvRsDomAtt classPref="encap" delimiter="" dn="'+pathDn+'" encapMode="'+encapmode+'" instrImedcy="'+deployImmediacy+'" resImedcy="'+resImmediacy+'" tDn="'+pathDn2+'" />'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data
   
    #Post to enable/disable BD subnet check flag
    #@xmlprint
    def toggleBDSubnetCheckFlag(self,action='enable'):
        '''
            Enables/Disables the global BD subnet check flag on the current Apic
            'action' specifies whether you want to enable or disable (default action is enable)
        '''
        if action == 'enable':
            action = 'true'
        else:
            action = 'false'
        pathDn = str("uni/infra/settings") 
       
        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<infraSetPol dn="'+pathDn+'" enforceSubnetCheck="'+action+'">'+\
                    '</infraSetPol>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data,additional_params='/api/node/mo/uni/infra/settings/.xml')
        return xml_data

    #Post to enable/disable IGMP snooping flag on BD level
    #@xmlprint
    def toggleIgmpSnooping(self,action='enable'):
        '''
            Enables/Disables the global BD IGMP Snooping Flag
            'action' specifies whether you want to enable or disable (default action is enable)
        '''

        if action=='enable':
            action = 'enabled'
        else:
            action = 'disabled'

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<fvTenant dn="uni/tn-common" name="common">'+\
                        '<igmpSnoopPol adminSt="'+action+'" ctrl="opt-flood" descr="" dn="uni/tn-common/snPol-default" lastMbrIntvl="1" name="default" nameAlias="" ownerKey="" ownerTag="" queryIntvl="125" rspIntvl="10" startQueryCnt="2" startQueryIntvl="31"/>'+\
                    '</fvTenant>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #@xmlprint
    def uploadApicImage(self,path,host,username,password,image_name):
        '''
            Given a build directory, pick up the Apic image and upload it to the current Apic
            arg1 - path to build directory
            arg2 - host ip or hostname
            arg3 - host username
            arg4 - host password
        '''

        apic_img = self.get_apic_image(path)
        if not apic_img:
            return False

        url = host + ':/' + apic_img
        dn = "uni/fabric/fwrepop/osrc-{}" .format(image_name)

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<firmwareOSource authPass="password" childAction="" descr="" dn="'+dn+'" proto="scp" url="'+url+'" user="'+username+'" password="'+password+'"/>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data

    #@xmlprint
    def uploadSwitchImage(self,path,host,username,password,image_name):
        '''
            Given a build directory, pick up the Leaf image and upload it to the current Apic
            arg1 - path to build directory
            arg2 - host ip or hostname
            arg3 - host username
            arg4 - host password
        '''

        switch_img = self.get_switch_image(path)
        if not switch_img:
            return False

        url = host + ':/' + switch_img
        dn = "uni/fabric/fwrepop/osrc-{}" .format(image_name)

        xml_data = '<?xml version="1.0" encoding="UTF-8"?>'
        xml_data += '<firmwareOSource authPass="password" childAction="" descr="" dn="'+dn+'" proto="scp" url="'+url+'" user="'+username+'" password="'+password+'"/>'

        self.pretty_print(xml_data,sys._getframe().f_code.co_name)
        self.post(xml_data)
        return xml_data
