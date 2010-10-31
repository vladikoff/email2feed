import os
import sys
from google.appengine.ext import webapp
from models.models import Recipient, MailMessage
from google.appengine.ext.webapp import template
import main
from urlparse import urlparse
import datetime
from libs import PyRSS2Gen


class Index(webapp.RequestHandler):
    def get(self):
        self.response.out("home")
        
class Show(webapp.RequestHandler):
    def get(self):
        email = self.request.get("e")
        messages = MailMessage.all().filter("toAddress = ", email).order("-dateReceived")

        
        viewdata = { 'messages':messages
                    , 'to':email}

        path = os.path.join(main.ROOT_DIR, 'views/feed/show.html')
        self.response.out.write(template.render(path, viewdata))
    

class List(webapp.RequestHandler):
    def get(self):
         
        viewdata = {'recipients':Recipient.all()}

        path = os.path.join(main.ROOT_DIR, 'views/feed/list.html')
        self.response.out.write(template.render(path, viewdata))

class ShowAll(webapp.RequestHandler):
    def get(self, user):         
     
        
        
        to = user + "@localhost.appspotmail.com"
        emails = MailMessage.all().filter("toAddress = ", to).order("-dateReceived")

        
        viewdata = { 'emails':emails, 'to':to, 'user':user}
        
        
        path = os.path.join(main.ROOT_DIR, 'views/u/web.html')
        self.response.out.write(template.render(path, viewdata))     
        
        
        
class ShowXML(webapp.RequestHandler):
    def get(self, user):     
        
        if os.environ.get('HTTP_HOST'):
            hostname = os.environ['HTTP_HOST']
        else:
            hostname = os.environ['SERVER_NAME']   
        
        FEED_TITLE = user + " feed at " + hostname
        FEED_URL = "http://"+hostname+"/xml/"+user
        
            
        messages = MailMessage.all()        
        messages.order("-dateReceived")
        results = messages.fetch(10)
        


        rss_items = []
        for msg in results:
            item = PyRSS2Gen.RSSItem(title=msg.subject,
                                     description=msg.body,
                                     pubDate=msg.dateReceived,
                                     guid = PyRSS2Gen.Guid(msg.fromAddress)
                                     )
            rss_items.append(item)

    
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
        viewdata = {'user':user}
        path = os.path.join(main.ROOT_DIR, 'views/u/atom.xml')
        self.response.out.write(template.render(path, viewdata))                
