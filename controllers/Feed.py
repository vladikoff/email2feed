import os
import sys
from google.appengine.ext import webapp
from models.models import Recipient, MailMessage
from google.appengine.ext.webapp import template
from google.appengine.api import users
from models.models import UserDetails
import main
from urlparse import urlparse
import datetime
from libs import PyRSS2Gen
import config

        
class Show(webapp.RequestHandler): #Old Feed Controller, shows the feed
    def get(self):
        email = self.request.get("e")
        messages = MailMessage.all().filter("toAddress = ", email).order("-dateReceived")       
        viewdata = { 'messages':messages, 'to':email}

        path = os.path.join(main.ROOT_DIR, 'views/feed/show.html')
        self.response.out.write(template.render(path, viewdata))    

class List(webapp.RequestHandler): #Old Feed Controller, lists the feed
    def get(self):
         
        viewdata = {'recipients':Recipient.all()}

        path = os.path.join(main.ROOT_DIR, 'views/feed/list.html')
        self.response.out.write(template.render(path, viewdata))

class ShowAll(webapp.RequestHandler): #Displays the user's web feed
    def get(self, user):         
             
        EMAIL_TO = user + config.SETTINGS['emaildomain']        
        
        accountExists = False   
  
        
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
        
        emails = MailMessage.all().filter("toAddress = ", EMAIL_TO).order("-dateReceived")      
        emailCount = emails.count() 
        if emailCount == 0:
            empty = True 
        viewdata = { 'emails':emails, 'to':EMAIL_TO, 'user':user, 'loggedIn': loggedIn, 'authControl':users.create_login_url("/"), 'accountExists':accountExists, 'empty': empty}      
        
        path = os.path.join(main.ROOT_DIR, 'views/u/web.html')
        self.response.out.write(template.render(path, viewdata))      
        
        
class ShowXML(webapp.RequestHandler): #Displays the RSS feed
    def get(self, user):     
        
        FEED_TITLE = user + " feed at " + config.SETTINGS['hostname']
        FEED_URL = "http://"+config.SETTINGS['hostname']+"/xml/"+user      
        EMAIL_TO = user + config.SETTINGS['emaildomain']  # ex. user@appid.appspotmail.com  
        
        messages = MailMessage.all().filter("toAddress = ", EMAIL_TO).order("-dateReceived") #Get all emails for the current user     
        results = messages.fetch(10) #Only 10 results for now...  
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
        EMAIL_TO = user + config.SETTINGS['emaildomain']  # ex. user@appid.appspotmail.com  
        
        messages = MailMessage.all().filter("toAddress = ", EMAIL_TO).order("-dateReceived")            
        results = messages.fetch(10)          
        self.response.headers['Content-Type'] = 'application/atomsvc+xml'
        self.response.out.write(template.render("views/u/atom.xml", {"results": results,"feedTitle":FEED_TITLE,"feedUrl":FEED_URL}))     
        
