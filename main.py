#!/usr/bin/env python

import wsgiref.handlers

from google.appengine.ext import webapp

import home
import search

def main():
  application = webapp.WSGIApplication([
      ('/', home.HomeHandler),
      ('/search', search.SearchHandler),
    ],
    debug=True)

  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
