import logging
import os

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext import search
from google.appengine.ext.webapp import template

import json
import model

class SearchHandler(webapp.RequestHandler):
  def get(self):
    query = self.request.get('q')
  
    results = memcache.get(query)
    
    if not results:
      entry_query = model.Entry.all().search(query)
      
      results = self._GroupEntries(entry_query)
      
      memcache.add(query, results)
    
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(json.JsonEncoder(indent=2).encode(results))

  
  def _GroupEntries(self, entry_query):
    """Group a flat list of entries by group and then by package"""
    
    results = []
    entries_by_group_and_package = {}
    
    for entry in entry_query:
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
      
    return results
  