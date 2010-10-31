from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from util.MailHandler import MailHandler
import logging, email, os
import controllers.Misc
import controllers.Feed
import controllers.Home
import controllers.Register

ROOT_DIR = os.path.dirname(__file__)

application = webapp.WSGIApplication([
                                     (r'/u/(.*)', controllers.Feed.ShowAll)
                                    ,(r'/xml/(.*)', controllers.Feed.ShowXML)
                                    ,(r'/atom/(.*)', controllers.Feed.ShowAtom)
                                    ,('/',controllers.Home.Index)                                   
                                    ,('/feed/show',controllers.Feed.Show)
                                    ,('/feed/list',controllers.Feed.List)
                                    ,('/help', controllers.Home.Help)
                                    ,('/register', controllers.Register.Save)
                                    ,MailHandler.mapping()
                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
