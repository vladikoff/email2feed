import os


#Application root dir
APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
#Application name
APPNAME = "sendfeedemail" 
#Minimum user name characters
MIN_USERNAME_CHAR = 5
#Maximum user name characters
MAX_USERNAME_CHAR = 25
#Application host name (auto)
if os.environ.get('HTTP_HOST'): 
    HOSTNAME = os.environ['HTTP_HOST']
else:
    HOSTNAME = os.environ['SERVER_NAME']     
    
    
    
#Generated Application Settings, try not to change these, but use the one above.
SETTINGS = {
    'appname': APPNAME,
    'hostname': HOSTNAME, 
    'url': 'http://'+APPNAME+'.appspot.com',
    'emaildomain': '@'+APPNAME+'.appspotmail.com',
    'minusername': MIN_USERNAME_CHAR,
    'maxusername': MAX_USERNAME_CHAR
    
}