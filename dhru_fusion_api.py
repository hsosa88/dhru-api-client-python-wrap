import requests
from xml.etree import ElementTree as ET


class ConfigurationSet():
    """
    This class is to store connection parameters
    """    
    
    def __init__(self, format, url, username, api_key):
        self.REQUESTFORMAT = format     # "JSON"
        self.DHRUFUSION_URL = url       # "http://yoursite.com/"
        self.USERNAME = username        # "XXXXXXXX"
        self.API_ACCESS_KEY = api_key   # "XXX-XXX-XXX-XXX-XXX-XXX-XXX-XXX"
       


class DhruFusion():
    """
        setting: Is a ConfigurationSet instance with connection data.\n
        user_agent: It's the User-Agent of client.\n
        debug: It's an option for developers 0 is off and 1 is on.
    """
          
    def __init__(self, setting, user_agent="", debug=0, veryfy_ssl=False):
        self.server_settings = setting
        self.USER_AGENT = user_agent
        self.DEBUG = debug
        self.verify_ssl = veryfy_ssl
        self.xmlData = ET.Element('')
    

    def action(self, action, args={}):
        if type(action) is str:
            if type(args) is dict:
                if len(args) > 0:
                    self.xmlData = ET.Element('PARAMETERS')
                    for key in args:
                        item = ET.SubElement(self.xmlData, key.upper())
                        item.text = args[key]
                
                posted = dict(
                    username=self.server_settings.USERNAME,
                    apiaccesskey=self.server_settings.API_ACCESS_KEY,
                    action=action,
                    requestformat=self.server_settings.REQUESTFORMAT,
                    parameters=ET.tostring(self.xmlData))

                headers = {'User-Agent': self.USER_AGENT}
                url = self.server_settings.DHRUFUSION_URL + "/api/index.php"
                
                try:
                    response = requests.post(url, data=posted, headers=headers, verify=self.verify_ssl)

                    if response.status_code is not 200:
                        return dict(response=response.text, error=response.status_code)
                    else:
                        return dict(response=response.text, error=None)
                except Exception as ex:
                    return dict(response=None, error=ex.__str__)
    

    def XMLtoET(self, raw_xml):
        return ET.parse(raw_xml)
    
    
    @staticmethod
    def get_account_info(api):
        """
        api: DhruFusion object 
        """
        response = api.action('accountinfo')
        if api.DEBUG is 1: DhruFusion.debug(response)
        return(response)


    @staticmethod
    def get_file_order_details(api, param):
        """
        api: DhruFusion object\n
        params: a dictionary like this\n
            {
                'ID': '60'
            }
        """
        response = api.action('getfileorder', param)
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response
    
    
    @staticmethod
    def get_imei_orders_details(api, param):
        """
        api: DhruFusion object\n
        params: a dictionary like this\n
            {
                'ID': '60'
            }
        """
        response = api.action('getimeiorder', param)
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response
    
        
    @staticmethod
    def get_imeiservice_list(api):
        """
        api: DhruFusion object 
        """
        response = api.action('imeiservicelist')
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response

    
    @staticmethod
    def get_fileservice_list(api):
        """
        api: DhruFusion object 
        """
        response = api.action('fileservicelist')
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response

    
    @staticmethod
    def get_mep_list(api):
        """
        api: DhruFusion object 
        """
        response = api.action('meplist')
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response

    
    @staticmethod
    def get_model_list(api, param):
        """
        api: DhruFusion object\n
        params: a dictionary like this\n
            {
                'ID': '60'
            }
        """
        response = api.action('modellist', param)
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response
    
    @staticmethod
    def get_provide_list(api, param):
        """
        api: DhruFusion object\n
        params: a dictionary like this\n
            {
                'ID': '60'
            }
        """
        response = api.action('providerlist')
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response

    
    @staticmethod
    def get_single_imei_service_details(api, param):
        """
        api: DhruFusion object\n
        params: a dictionary like this\n
            {
                'ID': '60'
            }
        """
        response = api.action('getimeiservicedetails', param)
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response


    @staticmethod
    def place_file_order(api, param):
        """
        api: DhruFusion object\n
        params: a dictionary like this\n
            {
                'ID': '60', 
                'FILENAME': 'ORDERID31TEST.txt', 
                'FILEDATA': 'TESTDATA '#encoded as Base64
            }
        """
        response = api.action('placefileorder', param)
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response
    

    @staticmethod
    def place_imei_order(api, param):
        """
        api: DhruFusion object \n
        params: a dictionary like this\n
            {
                'ID': '60', # got from 'imeiservicelist' [SERVICEID] 
                'IMEI': "111111111111116", 
                #PARAMETRES IS REQUIRED
                'MODELID': "",
                'PROVIDERID': "",
                'MEP': "",
                'PIN': "",
                'KBH': "",
                'PRD': "",
                'TYPE': "",
                'REFERENCE': "",
                'LOCKS': ""
            }
        """
        response = api.action('placeimeiorder', param)
        if api.DEBUG is 1: DhruFusion.debug(response)
        return response

    @staticmethod
    def debug(response):
        if response['error'] is None:
            print(response['response'])
        elif response['error'] is not None and response['response'] is not None:
            print(response['error'])
            print('\n--')
            print(response['response'])
        elif response['response'] is None:
            print(response['error'])

if __name__ == "__main__":
    api = DhruFusion(ConfigurationSet(
        "JSON", 
        "https://www.unlockking.us/", 
        "siouxsvp",
        "PJE-Z55-V2G-QVL-2ES-7JX-LKW-YSM"),debug=1, veryfy_ssl=True)
    DhruFusion.get_imeiservice_list(api)

