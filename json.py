from django.utils import simplejson

import model

class JsonEncoder(simplejson.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, model.Entry):
      return {
        'name': obj.name,
        'package': obj.package,
        'type': obj.type
      }
    if isinstance(obj, model.Group):
      return {
        'name': obj.name,
        'rootUrl': obj.root_url,
        'id': str(obj.key()),
      }
      
    return simplejson.JSONEncoder.default(self, obj)