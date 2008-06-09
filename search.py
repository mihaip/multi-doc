import os

from google.appengine.ext import webapp
from google.appengine.ext import search
from google.appengine.ext.webapp import template

import json
import model

class SearchHandler(webapp.RequestHandler):
  def get(self):
  
    query = model.Entry.all().search(self.request.get('q'))

    entries = [entry for entry in query]
    
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(json.JsonEncoder(indent=2).encode(entries))
