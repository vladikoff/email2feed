import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
from urlparse import urlparse
from models.models import UserDetails
from google.appengine.ext import db
 
class Save(webapp.RequestHandler):
    def post(self):
        
        USER_EXISTS = "Username Taken!"        
        
        userExists = False;
        emailName = self.request.get('emailname') 
        
        if os.environ.get('HTTP_HOST'):
            hostname = os.environ['HTTP_HOST']
        else:
            hostname = os.environ['SERVER_NAME']            
        existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user())
        for existingUser in existingUsers:        
            userExists = True;    
       
        if userExists:
            self.redirect("/#exists")          
        else:
            userDetails = UserDetails()     
            if users.get_current_user():
                userDetails.accountName = users.get_current_user()       
           
            userDetails.emailName = emailName      
            userDetails.put()
            
            viewdata = {'emailName':emailName, 'hostname':hostname}            
            path = os.path.join(main.ROOT_DIR, 'views/register.html')           
            self.response.out.write(template.render(path,viewdata))