import hashlib
import os
import tempfile
import urllib

from google.appengine.ext import db

class Doctype(object):
  _DOCTYPES_BY_ID = {}
  
  def __init__(self, id, name):
    Doctype._DOCTYPES_BY_ID[id] = self
    self.id = id
    self.name = name
  
  def GetAllDoctypes():
    return Doctype._DOCTYPES_BY_ID.values()
  GetAllDoctypes = staticmethod(GetAllDoctypes)
  
  def GetDoctypeFromId(id):
    return Doctype._DOCTYPES_BY_ID[id]
  GetDoctypeFromId = staticmethod(GetDoctypeFromId)
  
  def _FetchUrl(self, url):
    '''Helper method to fetch URLs, since many doctypes build themselves from
    pages'''
    filename = os.path.join(
        tempfile.gettempdir(), hashlib.md5(url).hexdigest())

    # TODO(mihaip): instead of this, actually implement if-modified-since
    # support
    if not os.path.exists(filename):    
      (filename, headers) = urllib.urlretrieve(url, filename)

    url_file = file(filename)
    url_html = url_file.read()
    url_file.close()
    return url_html
  
class FetchedEntry(object):
  """Lightweight version of model.Entry that doesn't have a group associated
  with it and is not tied to the datastore, mainly meant to be saved as a CSV
  file that is uploaded via the bulk upload API"""
  def __init__(self, name, package, type):
    self.name = name
    self.package = package
    self.type = type
  
# TOOD(mihaip): is the a better way of registering these?
import javadoc_doctype
import mdc_doctype
import w3c_doctype
  
_INSTANCES = [
  javadoc_doctype.JavadocDoctype(),
  mdc_doctype.MdcDoctype(),
  w3c_doctype.W3cDoctype(),
]