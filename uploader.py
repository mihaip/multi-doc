#!/usr/bin/env python

import csv
import getopt
import sys
import tempfile

sys.path.append('/usr/local/google_appengine')
sys.path.append('/usr/local/google_appengine/lib/yaml/lib')

from doctype import Doctype

def main(argv):
  opts, args = getopt.getopt(argv, "", ["doctype=", "group_id="])
  
  doctype = None
  group_id = None
  
  for opt, arg in opts:
    if opt == "--doctype":
      doctype = Doctype.GetDoctypeFromId(arg)
    if opt == "--group_id":
      group_id = arg
  
  assert doctype, "Doctype must be given"
  assert group_id, "Group ID must be specified"

  entries = doctype.Fetch(args)  
  
  print "Fetched %d entries" % len(entries)
  
  (csv_file, csv_filename) = tempfile.mkstemp(prefix=doctype.id, text=True)
  csv_file = file(csv_filename, 'w')
  csv_writer = csv.writer(csv_file)
  for entry in entries: 
    csv_writer.writerow([
      group_id,
      entry.name,
      entry.package,
      entry.type,
    ])
  
  csv_file.close()
  
  print "Fetched entries were written to %s" % csv_filename
  print """You should now run:
/usr/local/google_appengine/tools/bulkload_client.py \\
    --filename %s \\
    --kind FetchedEntry \\
    --cookie <admin cookie for your app> \\
    --url http://localhost:8080/admin/bulkload""" % csv_filename

if __name__ == '__main__':
  main(sys.argv[1:])
