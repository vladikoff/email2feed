import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
from models.models import UserDetails
from urlparse import urlparse
import config
from Base import App

class Index(webapp.RequestHandler): #front page     
    def get(self): 
               
        app = App()
        path = os.path.join(main.ROOT_DIR, 'views/index.html')
        user = users.get_current_user()       
        authControl = users.create_login_url("/") #dynamic link path to login or logout screens    
                   
        if user: #if logged in                    
            
            account = app.account_exists(users.get_current_user())
                
            if account['exists']: #Did this user get an email with us?
                if account['account_name']:
                    self.redirect("/view/"+account['account_name'])
                 
        this_data = {}        
        view_data = app.data(this_data)        
        
        self.response.out.write(template.render(path, view_data))    
                    

class Help(webapp.RequestHandler): #help and faqs page
    def get(self):
        path = os.path.join(main.ROOT_DIR, 'views/help.html')
        self.response.out.write(template.render(path, ""))