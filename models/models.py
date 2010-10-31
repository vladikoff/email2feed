from google.appengine.ext import db


class MailMessage(db.Model):
    toAddress = db.StringProperty()
    fromAddress = db.StringProperty()
    subject = db.StringProperty()
    body = db.TextProperty()
    dateSent = db.StringProperty()
    dateReceived = db.DateTimeProperty()


class Recipient(db.Model):
    toAddress = db.StringProperty()
    
class UserDetails(db.Model):
    accountName = db.UserProperty()
    emailName = db.StringProperty(multiline=False)
    date = db.DateTimeProperty(auto_now_add=True)