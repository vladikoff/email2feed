from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from models.models import UserDetails, TrustedEmails, BlockedEmails
from google.appengine.api.mail import EncodedPayload
from models.models import MailMessage
import logging
import datetime
import re

class MailHandler(InboundMailHandler):
    def receive(self, message):
        logging.info("Message from: " + message.sender)
        logging.info("Message to: " + message.to)
         
        fromEmail = message.sender
        to = message.to   
        blocked = trusted = accountExists = blockMode = False    
        
        
        m = re.search("(?<=\<)(.*?)(?=\>)", to) #serching for gmail formatted emails. ex: 'user <user@example.com>'
        if m: #gmail format
            to = m.group()
            emailName, emailDomain = to.split("@")       
        else: #normal email          
            emailName, emailDomain = to.split("@") 
        

        fm = re.search("(?<=\<)(.*?)(?=\>)", fromEmail) #serching for gmail formatted emails. ex: 'user <user@example.com>'
        if fm: #gmail format
            fromEmail = fm.group()  
            
            
        existingUsers = UserDetails.gql("WHERE emailName = :1 LIMIT 1",emailName) 
        for existingUser in existingUsers:        
                accountExists = True
                blockMode = existingUser.trustedMode
                accountName = existingUser.accountName
                logging.info("Account Exists: " + str(accountName))                
    
            
        if accountExists:             
            if blockMode: #if trust only enabled
                logging.info("to " + str(to)) 
                trustedEmails = TrustedEmails.gql("WHERE accountName = :1 LIMIT 1",accountName)  #check Trust List
                for trustedEmail in trustedEmails:        
                    if trustedEmail.email == fromEmail:
                        trusted = True  
                                  
            else:     
                blockedEmails = BlockedEmails.gql("WHERE accountName = :1 LIMIT 1",accountName) #check Block List  
                for blockedEmail in blockedEmails:        
                    if blockedEmail.email == fromEmail:
                        blocked = True
                                             
            if trusted and blockMode or not blocked and not blockMode:
                mailMessage = MailMessage()
                mailMessage.toAddress = to
                mailMessage.fromAddress = message.sender
                mailMessage.subject = message.subject
                mailMessage.body = self._getBody(message)
                mailMessage.dateSent = message.date
                mailMessage.dateReceived = datetime.datetime.now()
                mailMessage.put()
            else:
                logging.info("Blocked an email to " + message.to)
        else: 
            logging.info("Account does not exist " + message.to + " with an email name of " + emailName)
    
    def _getBody(self, message):
        ret = None
        for contentType, body in message.bodies():
            if (contentType == 'text/html'):
                ret = body
                break
            if (contentType == 'text/plain'):
                ret = body
        if isinstance(ret, EncodedPayload):
            ret = ret.decode()
        return ret