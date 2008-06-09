import re

from doctype import Doctype
from doctype import FetchedEntry
import model

class JavadocDoctype(Doctype):
  _LINK_RE = re.compile(
      '<A HREF="(.*)" title="(.*) in (.*)" target="classFrame">(.*)</A>')

  _NAME_HTML_RE = re.compile('<.+>(.*)</.+>')

  _TYPES = {
    "class": "Class",
    "interface": "Interface",
    "enum": "Enum",
    "annotation": "Annotation",
  }

  def __init__(self):
    Doctype.__init__(self, 'javadoc', 'Javadoc')
  
  def Fetch(self, args):
    all_classes_url = args[0]
    
    all_classes_html = self._FetchUrl(all_classes_url)

    entries = []

    for (url, type, package, name) in JavadocDoctype._LINK_RE.findall(
        all_classes_html):

      assert type in JavadocDoctype._TYPES, "unknown type %s" % type
      
      name_match = JavadocDoctype._NAME_HTML_RE.match(name)
      if name_match:
        name = name_match.group(1)

      entries.append(FetchedEntry(name, package, type))
      
    return entries

