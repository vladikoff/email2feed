from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from urlparse import urlparse
from models.models import UserDetails
from google.appengine.ext import db
import os, sys, main, config, re, math, time, random, logging, datetime
from Base import App
 
class Check(webapp.RequestHandler):
    def get(self):
        self.redirect("/#")
    def post(self):        
             
    
        confirm_username = self.request.get('email_name')
        validator = AccountValidator()
        validation = validator.validate(self.request.get('email_name'))
        if validation['valid']:
            account_available = True
            confirm_url = "/confirm/" + validation['email_name']
            auth_control = users.create_login_url(confirm_url)  
                    
                    
                 
            feed_urls = Check.generate_box(validation['email_name'])       
            feed_url = feed_urls['feed']
            feed_view = feed_urls['view']
            feed_gen = feed_urls['gen']
                    
            validator = AccountValidator() 
            validation = validator.validate(confirm_username)       
            if validation['valid']:  
                userDetails = UserDetails()                
                userDetails.emailName = validation['email_name']
                userDetails.feedUrl = feed_gen     
                userDetails.put()
                
                self.redirect("/view/" + feed_gen)
            else:
                self.redirect("/#invalid" + validation['error'] + " " + confirm_username)            
                    
                    
                    
            app = App()               
            this_data = {'email_name':validation['email_name'], 'hostname':config.SETTINGS['hostname'], 'account_available':account_available, 'auth_control':auth_control, 'feed_url':feed_url, 'feed_view':feed_view}            
            view_data = app.data(this_data)     
            
            path = os.path.join(main.ROOT_DIR, 'views/register.html')           
            self.response.out.write(template.render(path,view_data))
        else:
            self.redirect("/#invalid-" + validation['error'])     
                
                
                
                
                
    @staticmethod
    def generate_box(email_name):
      
        length = config.SETTINGS['feed_url_length'];
        c = ("b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "x", "y", "z")
        v = ("a", "e", "i", "o", "u")
        generated_url = email_name + "-"
        i = 0
        max = length / 2

        while i < max:
            if i % 5:
                generated_url += "-"
            generated_url += c[random.randint(0, 18)]
            generated_url += v[random.randint(0, 4)]
            i = i + 1
                
        feed_urls = {}
        feed_urls['gen'] = generated_url
        feed_urls['view'] = config.SETTINGS['url'] + "/view/" + generated_url
        feed_urls['feed'] = config.SETTINGS['url'] + "/" + generated_url       
        return feed_urls


            
            
class AccountValidator():
    def validate(self,email_name):       
        
        error = "0"
        userExists = unavailable = emailExists = account_available = False;
        email_name = email_name.strip().replace('-', '').replace(' ', '') 
        email_name_length = len(email_name)
        valid = False
        full_email_name = email_name + config.SETTINGS['emaildomain']
        unavailable_names = config.SETTINGS['unavailable_names']   
        
    
        
        #Is this email taken?
        existingEmails = UserDetails.gql("WHERE emailName = :1 LIMIT 1",email_name)
        for existingEmail in existingEmails:        
            emailExists = True;          
        
        for unavailablename in unavailable_names:
            if unavailablename == email_name:
                unavailable = True
                        
        if AccountValidator.validateEmail(full_email_name) == 0:
            error = "1"
            #self.redirect("/#invalidemail")
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