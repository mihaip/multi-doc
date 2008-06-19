from google.appengine.ext import bulkload
from google.appengine.ext import db
from google.appengine.api import datastore_types
from google.appengine.ext import search

import model

class EntryLoader(bulkload.Loader):
  def __init__(self):
    bulkload.Loader.__init__(self, 'FetchedEntry', [
      ('group_id', str),
      ('name', str),
      ('package', str),
      ('type', str),
    ])

  def HandleEntity(self, entity):
    group = model.Group.get(db.Key(encoded=entity['group_id']))
    name = entity['name']
    package = entity['package']
    type = entity['type']
    
    entry = model.Entry.CreateAndSave(group, name, package, type)

    return None

if __name__ == '__main__':
  bulkload.main(EntryLoader())