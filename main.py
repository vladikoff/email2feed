from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from util.MailHandler import MailHandler
import logging, email, os
import controllers.Misc
import controllers.Feed
import controllers.Home
import controllers.Register
import controllers.Settings

ROOT_DIR = os.path.dirname(__file__)

application = webapp.WSGIApplication([
                                      MailHandler.mapping() #Used for email post mapping 
                                    ,(r'/view/(.*)/(.*)', controllers.Feed.ShowMessage) #show feed message  
                                    ,(r'/view/(.*)', controllers.Feed.ShowAll) #user web feed                                    
                                    ,(r'/rss/(.*)', controllers.Feed.ShowXML) #user RSS feed
                                    ,('/',controllers.Home.Index) #Home page 
                                    ,('/help', controllers.Home.Help) #Help page
                                    ,('/register', controllers.Register.Save) #Registration page
                                    ,('/settings', controllers.Settings.Index) #Settings page 
                                    ,(r'/(.*)', controllers.Feed.ShowAtom) #user Atom Feed 
                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
