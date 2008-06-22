import re
import urllib

from doctype import Doctype
from doctype import FetchedEntry

class W3cDoctype(Doctype):
  _HTML_RE = re.compile(
      '<td title="Name"><a href="(.+)#edef-([^"]+)">(.*)</a></td>')

  '''World Wide Web Consortium documentation'''
  
  def __init__(self):
    Doctype.__init__(self, 'w3c', 'W3C')
  
  def Fetch(self, args):
    html_url = args[0]
    
    html_html = self._FetchUrl(html_url)
    
    entries = []
    
    for (element_file, fragment_name, element_name) in \
        W3cDoctype._HTML_RE.findall(html_html):
      assert fragment_name.lower() == element_name.lower()
      
      element_name = element_name.lower()
      
      entries.append(FetchedEntry(element_name, 'HTML', element_file))
    
    return entries