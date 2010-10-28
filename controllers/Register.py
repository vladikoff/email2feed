import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import main
from urlparse import urlparse
from models.models import UserDetails



from google.appengine.ext import db

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

 
class Save(webapp.RequestHandler):
    def post(self):
        
        userDetails = UserDetails()
        
        #userDetails.accountName = "AccountName"
        userDetails.emailName = "emailaddress@domain.com"
      
        userDetails.put()
        #email = self.request.get("e")
        #messages = MailMessage.all().filter("toAddress = ", email).order("-dateReceived")

      
        
        #viewdata = { 'messages':messages  , 'to':email}

        path = os.path.join(main.ROOT_DIR, 'views/register.html')
        self.response.out.write(template.render(path,""))
    
