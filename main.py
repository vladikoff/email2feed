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
                                     (r'/u/(.*)', controllers.Feed.ShowAll) #user web feed
                                    ,(r'/rss/(.*)', controllers.Feed.ShowXML) #user RSS feed
                                    ,(r'/atom/(.*)', controllers.Feed.ShowAtom) #user Atom Feed
                                    ,('/',controllers.Home.Index) #Home page                                  
                                    ,('/feed/show',controllers.Feed.Show) #Old Feed controller 1
                                    ,('/feed/list',controllers.Feed.List) #Old Feed controller 2
                                    ,('/help', controllers.Home.Help) #Help page
                                    ,('/register', controllers.Register.Save) #Registration page
                                    ,('/settings', controllers.Settings.Index) #Settings page
                                    ,MailHandler.mapping() #Used for email post mapping
                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
