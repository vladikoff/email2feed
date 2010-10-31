import os


#Application root dir
APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
#Application name (AppSpot App Id)
APPNAME = "sendfeedemail" 
#Minimum user name characters
MIN_USERNAME_CHAR = 5
#Maximum user name characters
MAX_USERNAME_CHAR = 25
#Trusted Mode (If 'True' new users must add a trusted email forwarding source to use the service)
TRUSTED_MODE = False

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
    'trustedmode': TRUSTED_MODE    
}