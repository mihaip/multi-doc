import logging
import os

from google.appengine.ext import webapp
from google.appengine.ext import search
from google.appengine.ext.webapp import template

import json
import model

class SearchHandler(webapp.RequestHandler):
  def get(self):
  
    query = model.Entry.all().search(self.request.get('q'))
    
    results = []
    entries_by_group_and_package = {}
    for entry in query:
      group_id = str(entry.group.key())
      if group_id not in entries_by_group_and_package:
        entries_by_package = {}
        results.append({
          "group": entry.group,
          "entriesByPackage": entries_by_package,
        })
        entries_by_group_and_package[group_id] = entries_by_package
      if entry.package not in entries_by_group_and_package[group_id]:
        entries_by_group_and_package[group_id][entry.package] = []
      entries_by_group_and_package[group_id][entry.package].append(entry)
    
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(json.JsonEncoder(indent=2).encode(results))
