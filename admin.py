#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp

import admin_add_entry
import admin_add_group
import admin_home

def main():
  application = webapp.WSGIApplication([
      ('/admin/', admin_home.HomeHandler),
      ('/admin/add_group', admin_add_group.AddGroupHandler),
      ('/admin/add_entry', admin_add_entry.AddEntryHandler),
    ],
    debug=True)

  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
