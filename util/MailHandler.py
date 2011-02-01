from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from models.models import UserDetails, TrustedEmails, BlockedEmails
from google.appengine.api.mail import EncodedPayload
from models.models import MailMessage
import logging, datetime, re

class MailHandler(InboundMailHandler):
    def receive(self, message):
        logging.info("Message from: " + message.sender + " to: " + message.to)
        original = message.original

        fromEmail = message.sender
        to = message.to   
        blocked = trusted = accountExists = blockMode = False        
        
        m = re.search("(?<=\<)(.*?)(?=\>)", to) #serching for gmail formatted emails. ex: 'user <user@example.com>'
        if m: #gmail format
            to = m.group()
                              
        emailName, emailDomain = to.split("@")        

        fm = re.search("(?<=\<)(.*?)(?=\>)", fromEmail) #serching for gmail formatted emails. ex: 'user <user@example.com>'
        if fm: #gmail format
            fromEmail = fm.group()
        
            
        existingUsers = UserDetails.gql("WHERE emailName = :1 LIMIT 1",emailName) 
        for existingUser in existingUsers:        
                accountExists = True
                blockMode = existingUser.trustedMode

        logging.info("Forwarder start")
        if original.has_key('X-Forwarded-To'):
                logging.info("Forwarder hit")
                forwardEmail = original.get('X-Forwarded-To')
                to = forwardEmail
                emailName, emailDomain = forwardEmail.split("@")
                logging.info("Forwarder: " + str(forwardEmail) + " :: to " + emailName)
                existingUsers2 = UserDetails.gql("WHERE emailName = :1 LIMIT 1",str(emailName))
                for existingUser2 in existingUsers2:
                        accountExists = True
                        blockMode = existingUser2.trustedMode
                        accountName = existingUser2.accountName
                        logging.info("Account Exists via Forward: " + str(emailName))
                        fromEmail = emailName

            
        if accountExists:     
                mailMessage = MailMessage()
                mailMessage.toAddress = to
                mailMessage.fromAddress = message.sender
                mailMessage.subject = message.subject
                mailMessage.body = self._getBody(message)
                mailMessage.dateSent = message.date
                mailMessage.dateReceived = datetime.datetime.now()
                mailMessage.put()            
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