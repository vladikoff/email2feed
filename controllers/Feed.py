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
from Base import App
        
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
            
        app = App()            
        
        emails = MailMessage.all().filter("toAddress = ", USER_EMAIL).order("-dateReceived")      
        emailCount = emails.count() 
        if emailCount == 0:
            empty = True 
        this_data = { 'emails':emails, 'to':USER_EMAIL, 'user_get':user, 'authControl':users.create_login_url("/"), 'empty': empty}      
                  
        
       
        view_data = app.data(this_data)
                
        path = os.path.join(main.ROOT_DIR, 'views/view/web.html')
        self.response.out.write(template.render(path, view_data))      

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
        
        feed_url = self.request.path.split('/')[2]
           
        prev_url = ""
        
        next_url = ""
               
            
        this_data = { 'email':email, 'to':USER_EMAIL, 'user':user, 'accountExists':accountExists, 'empty': empty, 'feed_url':feed_url[2], 'feed_url':feed_url, 'prev_url':prev_url}      
        
        app = App()
        view_data = app.data(this_data)
        
        path = os.path.join(main.ROOT_DIR, 'views/view/web-single.html')
        self.response.out.write(template.render(path, view_data))   
           
        
class ShowRSS(webapp.RequestHandler): #Displays the RSS feed
    def get(self, user):     
        
        FEED_TITLE = user + " - email2feed"
        FEED_URL = "http://"+config.SETTINGS['hostname']+"/rss/"+user      
        USER_EMAIL = user + config.SETTINGS['emaildomain']  # ex. user@appid.appspotmail.com
        USER_LINK = config.SETTINGS['url'] + "/view/" + user   
        
        messages = MailMessage.all().filter("toAddress = ", USER_EMAIL).order("-dateReceived") #Get all emails for the current user     
        results = messages.fetch(config.SETTINGS['maxfetch'])  
        rss_items = []
        
        #Feed Message Data
        for msg in results:
            genlink = USER_LINK + "/" + str(msg.key().id())
            item = PyRSS2Gen.RSSItem(title=msg.subject,description=msg.body,pubDate=msg.dateReceived,guid = PyRSS2Gen.Guid(genlink),link=genlink) #subject, body, date received, test guid
            rss_items.append(item) 

        #Feed Title Data
        rss = PyRSS2Gen.RSS2(title=FEED_TITLE,
                             link=FEED_URL,
                             description=USER_EMAIL,
                             lastBuildDate=datetime.datetime.now(),
                             items=rss_items
                            )
        
        rss_xml = rss.to_xml()
        self.response.headers['Content-Type'] = 'application/rss+xml'
        self.response.out.write(rss_xml)
        
class ShowAtom(webapp.RequestHandler):    
    def get(self, user):         
         
        FEED_TITLE = user + " - email2feed"
        FEED_URL = "http://"+config.SETTINGS['hostname']+"/"+user        
        USER_EMAIL = user + config.SETTINGS['emaildomain']  # ex. user@appid.appspotmail.com  
        USER_LINK = config.SETTINGS['url'] + "/view/" + user
        latestMessageVal = "";
        
        messages = MailMessage.all().filter("toAddress = ", USER_EMAIL).order("-dateReceived")
        results = messages.fetch(config.SETTINGS['maxfetch'])  
        
        latestEmailQry = MailMessage.all().filter("toAddress = ", USER_EMAIL).order("-dateReceived")
        latestMessageFtch = latestEmailQry.fetch(1)
        for latestMessage in latestMessageFtch:    
            latestMessageVal = latestMessage.dateReceived   
                
        this_data = {
                     "results"      :   results
                    ,"feedTitle"    :   FEED_TITLE
                    ,"feedUrl"      :   FEED_URL
                    ,"updated"      :   latestMessageVal
                    ,"name"         :   user
                    ,"email"        :   USER_EMAIL
                    ,"userlink"     :   USER_LINK  
                    }     
        app = App()
        view_data = app.data(this_data)      
       
        
        self.response.headers['Content-Type'] = 'application/atom+xml'
        self.response.out.write(template.render("views/view/atom.xml", view_data))