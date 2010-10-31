import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
from urlparse import urlparse

class Index(webapp.RequestHandler): #front page     
    def get(self):
        
        USER_LOGIN = "Login"
        USER_LOGOUT = "Log out"
        hostname = os.environ['SERVER_NAME']
        if os.environ.get('HTTP_HOST'):
            hostname = os.environ['HTTP_HOST']
        else:
            hostname = os.environ['SERVER_NAME']
        path = os.path.join(main.ROOT_DIR, 'views/index.html')
        user = users.get_current_user() 
        regShow = False #hide registrations form
        authName = USER_LOGIN   
        authControl = users.create_login_url("/") #dynamic link path to login or logout screens              
        if user: #if logged in and ready to register with the service  
            regShow = True
            authName = USER_LOGOUT  

        
        viewdata = {'authControl':authControl, 'authName': authName, 'regShow': regShow,'hostname':hostname}
        
        self.response.out.write(template.render(path, viewdata))
        
                    

class Help(webapp.RequestHandler): #help and faqs page
    def get(self):
        path = os.path.join(main.ROOT_DIR, 'views/help.html')
        self.response.out.write(template.render(path, ""))
