import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
import main
from urlparse import urlparse

class Index(webapp.RequestHandler): #help and faqs page
    def get(self):
        path = os.path.join(main.ROOT_DIR, 'views/settings.html')
        self.response.out.write(template.render(path, ""))