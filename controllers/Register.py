import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
from urlparse import urlparse
from models.models import UserDetails
from google.appengine.ext import db
import config
import re
 
class Save(webapp.RequestHandler):
    def get(self):
        self.redirect("/#")
    def post(self):
        
        USER_EXISTS = "Username Taken!"        
        
        userExists = unavailable = emailExists = False;
       
        
        emailName = self.request.get('emailname').strip().replace('-', '').replace(' ', '') 
        emailNameLength = len(emailName)
        fullEmailName = emailName + config.SETTINGS['emaildomain']
        unavailablenames = config.SETTINGS['unavailablenames'] 

   
        #Does this Google account have an account already?      
        existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user())
        for existingUser in existingUsers:        
            userExists = True;
        
        #Is this email taken?
        existingEmails = UserDetails.gql("WHERE emailName = :1 LIMIT 1",emailName)
        for existingEmail in existingEmails:        
            emailExists = True;          
   
        for unavailablename in unavailablenames:
            if unavailablename == emailName:
                unavailable = True
                        
        if Save.validateEmail(fullEmailName) == 0:
            self.redirect("/#invalidemail")
        elif userExists:
            self.redirect("/#accountexists") 
        elif emailExists:
            self.redirect("/#emailexists")
        elif unavailable:
            self.redirect("/#unavailable")            
        elif emailNameLength <= config.SETTINGS['minusername']:
            self.redirect("/#short")        
        elif emailNameLength >= config.SETTINGS['maxusername']:
            self.redirect("/#long")                
        else:
            userDetails = UserDetails()     
            if users.get_current_user():
                userDetails.accountName = users.get_current_user()       
           
            userDetails.emailName = emailName      
            userDetails.put()
            
            viewdata = {'emailName':emailName, 'hostname':config.SETTINGS['hostname']}            
            path = os.path.join(main.ROOT_DIR, 'views/register.html')           
            self.response.out.write(template.render(path,viewdata))
            
            
    @staticmethod    
    def validateEmail(email):
       
        if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
            return 1 #Valid Email
        else:
            return 0 #Invalid Email
        