import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from doctype import Doctype
import model

class AddEntryHandler(webapp.RequestHandler):
  def post(self):
    group = model.Group.get(db.Key(encoded=self.request.get('group')))
    name = self.request.get('name')
    package = self.request.get('package')
    type = self.request.get('type')

    doctype = group.GetDoctype()
    
    entry = model.Entry.CreateAndSave(group, name, package, type)
    
    self.redirect("/admin/")