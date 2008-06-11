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

_STOP_WORDS = frozenset([
  'java', 'class', 'interface', 'enum', 'annotation'])

class Entry(search.SearchableModel):
  group = db.ReferenceProperty(Group)
  
  # Class/interface/enum/etc. name
  name = db.BlobProperty()
  
  # Package name
  package = db.BlobProperty()
  
  # Class, interface, enum, etc. (group-specific)
  type = db.BlobProperty()
  
  # To control which keywords get indexed (since we want more fine-grained 
  # stopwords), we make all the other properties blobs, and we put in the 
  # keywords that we actually want indexed in this property
  keywords = db.TextProperty()
  
  def Create(group, name, package, type):
    # TODO(mihaip): validation?
    
    entry = Entry(
      group = group,
      name = str(name),
      package = str(package),
      type = str(type),
      keywords = ' '.join(Entry._GetKeywords(name, package, type)),
    )
    
    return entry
  Create = staticmethod(Create)
  
  def _GetKeywords( name, package, type):
    keywords = _PUNCTUATION_RE.sub(
        ' ', name + ' ' + package + ' ' + type).split()
    
    # Split keywords even more 
    for keyword in keywords:
      # TODO(mihaip): also handle underscores?
      
      # Handle camel-case if we detect mixed-case
      if not keyword.isupper() and not keyword.islower():

        start = 0
        for camel_case_transition in _CAMEL_CASE_RE.finditer(keyword):
          end = camel_case_transition.start() + 1
          keywords.append(keyword[start:end])
          start = end
        
        if start != 0:
          keywords.append(keyword[start:])
          
    return set([k.lower() for k in keywords if k.lower() not in _STOP_WORDS])
  _GetKeywords = staticmethod(_GetKeywords)    