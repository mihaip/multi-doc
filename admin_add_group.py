import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from doctype import Doctype
import model

class AddGroupHandler(webapp.RequestHandler):
  def post(self):
    doctype = Doctype.GetDoctypeFromId(self.request.get('doctype'))
    name = self.request.get('name')
    root_url = self.request.get('root_url')
    
    group = model.Group(
      name = name,
      doctype = doctype.id,
      root_url = root_url,
    )
    group.save()
    
    self.redirect("/admin/")