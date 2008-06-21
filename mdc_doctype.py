import re
import urllib

from doctype import Doctype
from doctype import FetchedEntry

class MdcDoctype(Doctype):
  _CSS_RE = re.compile('href="/en/docs/CSS:([^"]+)"')

  '''Mozilla Developer Center documentation'''
  
  def __init__(self):
    Doctype.__init__(self, 'mdc', 'Mozilla Developer Center')
  
  def Fetch(self, args):
    css_url = args[0]
    
    css_html = self._FetchUrl(css_url)
    
    entries = []
    
    for (css_name) in MdcDoctype._CSS_RE.findall(css_html):    
      css_name = urllib.unquote(css_name)
      
      # Skip over non-CSS names
      if not css_name.islower() or css_name.find('_') != -1: continue
      
      css_type = 'property'
      if css_name[0] == ':':
        css_type = 'pseudo-class'
      elif css_name[0] == '@':
        css_type = 'at-rule'

      entries.append(FetchedEntry(css_name, 'CSS', css_type))
    
    return entries