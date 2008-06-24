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
    
    results_json = memcache.get(query)
    
    if not results_json:
      # If a query is composed entirely of stop-words or is too short, App
      # Engine ends up using an empty query, which returns all results. 
      # Returning nothing seems more appropriate.
      if len(query) < 3:
        results = []
      else:
        entry_query = model.Entry.all().search(query)
        results = self._GroupEntries(entry_query)

      results_json = json.JsonEncoder(indent=2).encode(results)
      
      memcache.add(query, results_json)
    
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(results_json)

  
  def _GroupEntries(self, entry_query):
    """Group a flat list of entries by group and then order by package and 
    name"""
    
    results = []
    entries_by_group = {}
    
    for entry in entry_query:
      try:
        group_id = str(entry.group.key())
      except:
        # Ignore orphaned entries
        continue
      
      if group_id not in entries_by_group:
        entries = []
        results.append({
          "group": entry.group,
          "entries": entries,
        })
        entries_by_group[group_id] = entries
      
      entries_by_group[group_id].append(entry)

    for entries in entries_by_group.values():
      entries.sort(SearchHandler._EntryComparator)
      
    return results
  
  def _EntryComparator(x, y):
    package_diff = cmp(x.package, y.package)
    if package_diff: return package_diff
    
    return cmp(x.name, y.name)
  _EntryComparator = staticmethod(_EntryComparator)    