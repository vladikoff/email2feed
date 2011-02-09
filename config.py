import os

#Application Settings

#Application root dir
APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
#Platform Name
PLATFORM_NAME = "email2feed"
#Application name (AppSpot App Id)
APPNAME = os.environ['APPLICATION_ID']
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
  
#Feed URL Length
URL_LENGTH = 44
 
 
 
 
 
 

#Application host name (auto)
if os.environ.get('HTTP_HOST'): 
    HOSTNAME = os.environ['HTTP_HOST']
else:
    HOSTNAME = os.environ['SERVER_NAME']    
    
#Generated Application Settings, try not to change these, but modify the ones above.
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
    'platform': PLATFORM_NAME,
    'feed_url_length':URL_LENGTH
}

#Error Codes
ERRORS = {
          1: "This name is invalid for an email.",
          2: "Sorry, this name is already taken.",
          3: "This name is already taken.",
          4: "This email is unavailable.",
          5: "The name you chose is too short. It needs to be between " + str(MIN_USERNAME_CHAR) + " and  " +  str(MAX_USERNAME_CHAR) + " characters.",
          6: "The name you chose is too long. It needs to be between " +  str(MIN_USERNAME_CHAR) + " and  " +  str(MAX_USERNAME_CHAR) + " characters."      
}