import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
import config
from urlparse import urlparse
from models.models import UserDetails

class Index(webapp.RequestHandler): #User Settings
    def get(self):
        path = os.path.join(main.ROOT_DIR, 'views/settings.html')
        trustedMode = False
        user = users.get_current_user() 
        
      
        if user: #if logged in                          
            existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",user) 
            for existingUser in existingUsers:         
                trustedMode = existingUser.trustedMode
                emailName = existingUser.emailName
          
        else:
            self.redirect("/#login")
            
        viewdata = {'trustedModeCheck':trustedMode,'user':emailName}
        
        self.response.out.write(template.render(path, viewdata))
    def post(self):
        
        submit = self.request.get('delacc')
        user = users.get_current_user() 
        userAddress = str(user) + config.SETTINGS['emaildomain'];   
        
        if submit == "dellacc":
            qUser = db.GqlQuery("SELECT * FROM UserDetails WHERE accountName = :1", user)
            resultsUser = qUser.fetch(1)
            db.delete(resultsUser)
            
            qMessages = db.GqlQuery("SELECT * FROM MailMessages WHERE toAddress = :1", userAddress)
            resultsMessages = qMessages.fetch()
            db.delete(resultsMessages)
            self.redirect("/#deleted")
        
        
        trustedValue = self.request.get('trusted')
        user = users.get_current_user() 
        if (trustedValue == "Enable"):
            trustedValueBool = True
        else: 
            trustedValueBool = False
        
        if user: #if logged in                          
            existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user()) 
            for existingUser in existingUsers:         
                existingUser.trustedMode = trustedValueBool
                existingUser.put()          
        else:
            self.redirect("/#login")
        
        
        self.redirect("/settings#post" + submit )