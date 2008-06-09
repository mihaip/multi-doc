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
      
    return simplejson.JSONEncoder.default(self, obj)