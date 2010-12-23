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
        view_data['hostname'] = config.SETTINGS['hostname']
        view_data['emaildomain'] = config.SETTINGS['emaildomain']    
               
        user = users.get_current_user()
        if user:  
            view_data['logged_in'] = True
            view_data['auth_link'] = users.create_logout_url("/")
            
            current_users = UserDetails.gql("WHERE accountName = :1 LIMIT 1",user) 
            if current_users:
                view_data['account_name'] = current_users[0].emailName                        
        else:
            view_data['auth_link'] = users.create_login_url("/")    
        
        
        if view_data.get('user_get'):               
            view_data['account_exists'] = App.feed_exists(view_data['user_get'])
            view_data['rss_link'] = '<link rel="alternate" type="application/rss+xml" title="" href="">'
            view_data['atom_link'] = '<link href="atom.xml" type="application/atom+xml" rel="" title="" />'
            
        return view_data   
    
    def account_exists(self, account_name): 
        exists = False    
        existing_users = UserDetails.gql("WHERE accountName = :1 LIMIT 1",account_name)
        for existing_user in existing_users:             
            exists = True
            account_name =  existing_users[0].emailName
            
        account = {}
        account['exists'] = exists
        account['account_name'] = account_name
        return account
    
    @staticmethod   
    def feed_exists(feed_name): 
        exists = False    
        existing_feeds = UserDetails.gql("WHERE emailName = :1 LIMIT 1",feed_name) 
        for existing_feed in existing_feeds:                     
            exists = True       
               
        return exists