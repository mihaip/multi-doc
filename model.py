import logging
import re
import string

from google.appengine.ext import db
from google.appengine.ext import search

from doctype import Doctype

_CAMEL_CASE_RE = re.compile('[a-z][A-Z]')
_PUNCTUATION_RE = re.compile('[' + re.escape(string.punctuation) + ']')

class Group(db.Model):
  # Human-readable name for this group
  name = db.StringProperty()
  
  # ID that maps to a Doctype instance
  doctype = db.StringProperty()
  
  # Base URL for this group, with which links will be generated
  root_url = db.StringProperty()
  
  def GetDoctype(self):
    return Doctype.GetDoctypeFromId(self.doctype)

class Entry(search.SearchableModel):
  group = db.ReferenceProperty(Group)
  
  # Class/interface/enum/etc. name
  name = db.StringProperty()
  
  # Package name
  package = db.StringProperty()
  
  # Class, interface, enum, etc. (group-specific)
  type = db.CategoryProperty()
  
  # Optionally, if the name and package do not tokenize well for the full-text
  # search, additional whitespace-separated keywords may be included here
  keywords = db.TextProperty()
  
  def Create(group, name, package, type):
    # TODO(mihaip): validation?
    # TODO(mihaip): keywords
    
    current_keywords = name + " " + package + " " + type
    current_keywords = _PUNCTUATION_RE.sub(' ', current_keywords)
    current_keywords = current_keywords.split()
    
    additional_keywords = []
    for current_keyword in current_keywords:
      # TODO(mihaip): also handle underscores?
      
      # Handle camel-case if we detect mixed-case
      if not current_keyword.isupper() and not current_keyword.islower():

        def AddPossibleSubKeyword(sub_keyword):
          sub_keyword = sub_keyword.lower()
          if sub_keyword not in current_keywords and \
            sub_keyword not in additional_keywords:
            additional_keywords.append(sub_keyword)

      
        start = 0
        for camel_case_transition in _CAMEL_CASE_RE.finditer(current_keyword):
          end = camel_case_transition.start() + 1
          AddPossibleSubKeyword(current_keyword[start:end])
          start = end
        
        if start != 0:
          AddPossibleSubKeyword(current_keyword[start:])

    entry = Entry(
      group = group,
      name = name, 
      package = package,
      type = db.Category(type),
      keywords = ' '.join(additional_keywords),
    )
    
    return entry
  Create = staticmethod(Create)