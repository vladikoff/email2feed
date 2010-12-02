import os
import sys
from google.appengine.ext import webapp
from models.models import MailMessage
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models.models import UserDetails
import main
from urlparse import urlparse
import datetime
import config
        
class App():    
    def data(self, view_data):
        
        view_data['logged_in'] = False        
        view_data['base_title'] = config.SETTINGS['platform']
        view_data['auth_link'] = users.create_login_url("/")             
        view_data['hostname'] = config.SETTINGS['hostname']
        
        user = users.get_current_user()
        if user:  
            view_data['logged_in'] = True
        
        return view_data   
    
    def account_exists(self, account_name): 
        exists = False    
        existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",account_name) 
        for existingUser in existingUsers:        
            exists = True
            account_name =  existingUser.emailName
            
        account = {}
        account['exists'] = exists
        account['account_name'] = account_name
        return account