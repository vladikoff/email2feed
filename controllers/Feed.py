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
from libs import PyRSS2Gen
import config
        
class ShowAll(webapp.RequestHandler): #Displays the user's web feed
    def get(self, user):                    
        USER_EMAIL = user + config.SETTINGS['emaildomain']       
        accountExists = empty = False   
        emailName = ""
       
        currentUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user()) 
        for currentUser in currentUsers:  
            emailName =  currentUser.emailName
        
        existingUsers = UserDetails.gql("WHERE emailName = :1 LIMIT 1",user) 
        for existingUser in existingUsers:  
            accountExists = True
            
        if user == emailName: 
            loggedIn = True
        else:
            loggedIn = False
        
        emails = MailMessage.all().filter("toAddress = ", USER_EMAIL).order("-dateReceived")      
        emailCount = emails.count() 
        if emailCount == 0:
            empty = True 
        viewdata = { 'emails':emails, 'to':USER_EMAIL, 'user':user, 'loggedIn': loggedIn, 'authControl':users.create_login_url("/"), 'accountExists':accountExists, 'empty': empty}      
        
        path = os.path.join(main.ROOT_DIR, 'views/view/web.html')
        self.response.out.write(template.render(path, viewdata))      

class ShowMessage(webapp.RequestHandler): #show message by id
    def get(self, user, messageid):    
        
        USER_EMAIL = user + config.SETTINGS['emaildomain']        
        
        mId = int(messageid)
        accountExists = False   
        emailName = ""
        empty = True
        currentUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user()) 
        for currentUser in currentUsers:  
            emailName =  currentUser.emailName
        
        existingUsers = UserDetails.gql("WHERE emailName = :1 LIMIT 1",user) 
        for existingUser in existingUsers:  
            accountExists = True       
             
            
        if user == emailName: 
            loggedIn = True
        else:
            loggedIn = False
        
        email = MailMessage.get_by_id(mId)   
        if email:
            empty = False
            
        viewdata = { 'email':email, 'to':USER_EMAIL, 'user':user, 'loggedIn': loggedIn, 'authControl':users.create_login_url("/"), 'accountExists':accountExists, 'empty': empty}      
        
        path = os.path.join(main.ROOT_DIR, 'views/view/view.html')
        self.response.out.write(template.render(path, viewdata))   
           
        
class ShowXML(webapp.RequestHandler): #Displays the RSS feed
    def get(self, user):     
        
        FEED_TITLE = user + " feed at " + config.SETTINGS['hostname']
        FEED_URL = "http://"+config.SETTINGS['hostname']+"/xml/"+user      
        USER_EMAIL = user + config.SETTINGS['emaildomain']  # ex. user@appid.appspotmail.com  
        
        messages = MailMessage.all().filter("toAddress = ", USER_EMAIL).order("-dateReceived") #Get all emails for the current user     
        results = messages.fetch(config.SETTINGS['maxfetch'])  
        rss_items = []
        
        #Feed Message Data
        for msg in results:
            item = PyRSS2Gen.RSSItem(title=msg.subject,description=msg.body,pubDate=msg.dateReceived,guid = PyRSS2Gen.Guid(msg.fromAddress)) #subject, body, date received, test guid
            rss_items.append(item) 

        #Feed Title Data
        rss = PyRSS2Gen.RSS2(title=FEED_TITLE,
                             link=FEED_URL,
                             description="",
                             lastBuildDate=datetime.datetime.now(),
                             items=rss_items
                            )
        
        rss_xml = rss.to_xml()
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss_xml)
        
class ShowAtom(webapp.RequestHandler):    
    def get(self, user):         
         
        FEED_TITLE = user + " feed at " + config.SETTINGS['hostname']
        FEED_URL = "http://"+config.SETTINGS['hostname']+"/xml/"+user        
        USER_EMAIL = user + config.SETTINGS['emaildomain']  # ex. user@appid.appspotmail.com  
        
        messages = MailMessage.all().filter("toAddress = ", USER_EMAIL).order("-dateReceived")
             
        results = messages.fetch(config.SETTINGS['maxfetch'])          
        self.response.headers['Content-Type'] = 'application/atom+xml'
        self.response.out.write(template.render("views/view/atom.xml", {"results": results,"feedTitle":FEED_TITLE,"feedUrl":FEED_URL}))     
        
