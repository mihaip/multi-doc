import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import doctype
import model

class HomeHandler(webapp.RequestHandler):
  def get(self):
    doctypes = doctype.Doctype.GetAllDoctypes()
    groups = model.Group.all()
    
    path = os.path.join(os.path.dirname(__file__), 'templates/admin_home.html')
    self.response.out.write(template.render(path, {
      'doctypes': doctypes,
      'groups': groups,
    }))
