import os

#Application Settings
#Application root dir
APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
#Platform Name
PLATFORM_NAME = "email2feed"
#Application name (AppSpot App Id)
APPNAME = "sendfeedemail"
#Maximum RSS/Atom Fetch
MAX_FETCH = 50

#User Settings 
#Minimum user name characters
MIN_USERNAME_CHAR = 4
#Maximum user name characters
MAX_USERNAME_CHAR = 25
#Trusted Mode (If 'True' new users must add a trusted email forwarding source to use the service)
TRUSTED_MODE = False
#Unavailable names
UNAVAILABLE_NAMES = ["help","settings","view","rss","register","js","css","admin","domain","support"]
 

#Application host name (auto)
if os.environ.get('HTTP_HOST'): 
    HOSTNAME = os.environ['HTTP_HOST']
else:
    HOSTNAME = os.environ['SERVER_NAME']     
    
    
    
#Generated Application Settings, try not to change these, but use the ones above.
SETTINGS = {
    'appname': APPNAME,
    'hostname': HOSTNAME, 
    'url': 'http://'+APPNAME+'.appspot.com',
    'emaildomain': '@'+APPNAME+'.appspotmail.com',
    'minusername': MIN_USERNAME_CHAR,
    'maxusername': MAX_USERNAME_CHAR,
    'trustedmode': TRUSTED_MODE,
    'maxfetch': MAX_FETCH,
    'unavailable_names': UNAVAILABLE_NAMES, 
    'platform': PLATFORM_NAME
}