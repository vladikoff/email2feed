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
from Base import App
 
class Check(webapp.RequestHandler):
    def get(self):
        self.redirect("/#")
    def post(self):        
        
        user = users.get_current_user()
        action = self.request.get('action')           
           
        validator = AccountValidator()
        validation = validator.validate(self.request.get('email_name'))
        if validation['valid']:
            account_available = True
            confirm_url = "/confirm/" + validation['email_name']
            auth_control = users.create_login_url(confirm_url)  
                    
            app = App()               
            this_data = {'email_name':validation['email_name'], 'hostname':config.SETTINGS['hostname'], 'account_available':account_available, 'auth_control':auth_control}            
            view_data = app.data(this_data)     
            
            path = os.path.join(main.ROOT_DIR, 'views/register.html')           
            self.response.out.write(template.render(path,view_data))
        else:
            self.redirect("/#invalid-" + validation['error'])     
                
                
        
class Confirm(webapp.RequestHandler):
    def get(self, confirm_username):
        
        user = users.get_current_user()
        if user:  
            validator = AccountValidator() 
            validation = validator.validate(confirm_username)       
            if validation['valid']:  
                userDetails = UserDetails()          
                userDetails.accountName = user           
                userDetails.emailName = validation['email_name']      
                userDetails.put()
                
                self.redirect("/view/" + str(validation['email_name']))
            else:
                self.redirect("/#invalid" + validation['error'])     
                          
        else:              
            self.redirect("/#confirmfail")
            
            
            
class AccountValidator():
    def validate(self,email_name):       
        
        error = "0"
        userExists = unavailable = emailExists = account_available = False;
        email_name = email_name.strip().replace('-', '').replace(' ', '') 
        email_name_length = len(email_name)
        valid = False
        full_email_name = email_name + config.SETTINGS['emaildomain']
        unavailable_names = config.SETTINGS['unavailable_names'] 
        
        
        #Does this Google account have an account already?      
        existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user())
        for existingUser in existingUsers:        
            userExists = True;
        
        #Is this email taken?
        existingEmails = UserDetails.gql("WHERE emailName = :1 LIMIT 1",email_name)
        for existingEmail in existingEmails:        
            emailExists = True;          
        
        for unavailablename in unavailable_names:
            if unavailablename == email_name:
                unavailable = True
                        
        if AccountValidator.validateEmail(full_email_name) == 0:
            error = "1"
            #self.redirect("/#invalidemail" + full_email_name)
        elif userExists:
            error = "2"
            #self.redirect("/#accountexists") 
        elif emailExists:
            error = "3"
            #self.redirect("/#emailexists")
        elif unavailable:
            error = "4"
            #self.redirect("/#unavailable")            
        elif email_name_length <= config.SETTINGS['minusername']:
            error = "5"
            #self.redirect("/#short")        
        elif email_name_length >= config.SETTINGS['maxusername']:
            error = "6"
            #self.redirect("/#long")    
        else:
            valid = True
            
        validation = {}
        validation['valid'] = valid
        validation['email_name'] = email_name
        validation['error'] = error
        return validation
    
    @staticmethod    
    def validateEmail(email):
       
        if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", email) != None:
            return 1 #Valid Email
        else:
            return 0 #Invalid Email