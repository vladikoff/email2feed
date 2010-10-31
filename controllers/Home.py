import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
from models.models import UserDetails
from urlparse import urlparse
import config

class Index(webapp.RequestHandler): #front page     
    def get(self):
        
        USER_LOGIN = "Login"
        USER_LOGOUT = "Log out"
            
        path = os.path.join(main.ROOT_DIR, 'views/index.html')
        user = users.get_current_user() 
        regShow = False #hide registrations form
        authName = USER_LOGIN   
        authControl = users.create_login_url("/") #dynamic link path to login or logout screens    
        accountExists = False   
             
        if user: #if logged in
            existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user()) 
            for existingUser in existingUsers:        
                accountExists = True
                accountName =  existingUser.emailName
                
            if accountExists: #Did this user get an email with us?
                self.redirect("/u/"+accountName)
            else:            
                regShow = True
                authName = USER_LOGOUT

        
        viewdata = {'authControl':authControl, 'authName': authName, 'regShow': regShow,'hostname':config.SETTINGS['hostname']}
        
        self.response.out.write(template.render(path, viewdata))
        
                    

class Help(webapp.RequestHandler): #help and faqs page
    def get(self):
        path = os.path.join(main.ROOT_DIR, 'views/help.html')
        self.response.out.write(template.render(path, ""))
