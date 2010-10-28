import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
from urlparse import urlparse
from models.models import UserDetails
from google.appengine.ext import db
 
class Save(webapp.RequestHandler):
    def post(self):
        emailName = self.request.get('emailname') 
        userDetails = UserDetails()
        
        if users.get_current_user():
            userDetails.accountName = users.get_current_user()       
        
        userDetails.emailName = emailName      
        userDetails.put()
        
        viewdata = {'emailName':emailName}
        
        path = os.path.join(main.ROOT_DIR, 'views/register.html')
        self.response.out.write(template.render(path,viewdata))