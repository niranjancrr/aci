import requests,json

class Post():

    def __init__(self):
        self.log.info('Initializing Post Class')

    def post(self,xml_data,additional_params=''):
        #Login to the APIC - JSON post
        login_url = "https://" + self.ip + "/api/aaaLogin.json"
        data = {"aaaUser":{"attributes":{"name": self.username, "pwd": self.password}}}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(login_url, data=json.dumps(data), headers=headers, verify=False)
        cookie=r.cookies.get_dict()

        data = xml_data
        if additional_params == '':
            url = '/api/policymgr/mo/.xml'
        else:
            url = additional_params

        #Send XML post
        post_url="https://" + self.ip + '/' + url
        #print post_url
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(post_url, data, headers=headers, verify=False, cookies=cookie)
