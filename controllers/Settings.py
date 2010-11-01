import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db

import main
import config
from urlparse import urlparse
from models.models import UserDetails, MailMessage, BlockedEmails, TrustedEmails

class Index(webapp.RequestHandler): #User Settings
    def get(self):
        path = os.path.join(main.ROOT_DIR, 'views/settings.html')
        trustedMode = False
        user = users.get_current_user() 
        emailName = ""
        accountExists = False
        tResult = bResult = False
        
      
        if user: #if logged in                          
            existingUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",user) 
        
            for existingUser in existingUsers:         
                trustedMode = existingUser.trustedMode
                emailName = existingUser.emailName
                accountExists = True       
       
            
        if accountExists == False:
            self.redirect("/#login")
        else:
            
            
            
            trustedEmails = TrustedEmails.all().filter("accountName = ", user)
            for trustedEmail in trustedEmails:
                tResult = True  
            blockedEmails = BlockedEmails.all().filter("accountName = ", user) 
            for blockedEmail in blockedEmails:  
                bResult = True    
             
            
            
            
            
            viewdata = {'trustedModeCheck':trustedMode,'user':emailName, 'trustedEmails':trustedEmails, 'blockedEmails':blockedEmails, 'tResult':tResult, 'bResult':bResult}            
            self.response.out.write(template.render(path, viewdata))
            
    def post(self):
        
        submit = self.request.get('action')
        user = users.get_current_user() 
        emailName = ""
        
        currentUsers = UserDetails.gql("WHERE accountName = :1 LIMIT 1",users.get_current_user()) 
        for currentUser in currentUsers:  
            emailName =  currentUser.emailName
            
        userAddress = emailName + config.SETTINGS['emaildomain'];   
        
        if submit == "delete":
            qUser = db.GqlQuery("SELECT __key__ FROM UserDetails WHERE accountName = :1", user)
            resultsUser = qUser.fetch(1)
            db.delete(resultsUser)
            
            qMessages = db.GqlQuery("SELECT __key__ FROM MailMessage WHERE toAddress = :1", userAddress)
            qMessagesNumber = qMessages.count()
            resultsUser = qMessages.fetch(qMessagesNumber)           
            db.delete(qMessages)
            self.redirect("/#deleted")
        
        if submit == "trustmode": #Enabling Trust Only Mode
      
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
            self.redirect("/settings#post")
            
        if submit == "block":            
            addedEmail = self.request.get('email')
            
            blockedEmail = BlockedEmails()     
            if users.get_current_user():
                blockedEmail.accountName = users.get_current_user()       
           
            blockedEmail.email = addedEmail      
            blockedEmail.put()            
              
            self.redirect("/settings#block")
       
        if submit == "trust":           
            addedEmail = self.request.get('email')   
            
            trustedEmail = TrustedEmails()     
            if users.get_current_user():
                trustedEmail.accountName = users.get_current_user()       
           
            trustedEmail.email = addedEmail      
            trustedEmail.put()          
                  
            self.redirect("/settings#trust")         