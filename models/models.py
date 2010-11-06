from google.appengine.ext import db
import config

class MailMessage(db.Model):
    toAddress = db.StringProperty()
    fromAddress = db.StringProperty()
    subject = db.StringProperty(multiline=True)
    body = db.TextProperty() 
    dateSent = db.StringProperty()
    dateReceived = db.DateTimeProperty()

class UserDetails(db.Model):
    accountName = db.UserProperty() 
    emailName = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)    
    trustedMode = db.BooleanProperty(default=config.SETTINGS['trustedmode'])
    
class TrustedEmails(db.Model):
    accountName = db.UserProperty()
    email = db.StringProperty()

class BlockedEmails(db.Model):
    accountName = db.UserProperty()
    email = db.StringProperty()