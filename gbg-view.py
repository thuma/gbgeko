#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from gevent import Greenlet, sleep, signal, monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
from bottle import template, run, default_app, hook, request, response, TEMPLATE_PATH
import os
import json

conn = sqlite3.connect('gbg.db')

headers = [
  "förvaltning",
  "leverantör",
  "organisationsnummer",
  "verifikationsnummer",
  "konto",
  "kontotext",
  "belopp exkl moms",
  "summa"]

# Help Bottle find our templates
base_path = os.path.abspath(os.path.dirname(__file__))
templates_path = os.path.join(base_path, 'templates')
TEMPLATE_PATH.insert(0, templates_path)

app = default_app()


def format(rows):
  for row in rows:
    thisrow = list(row)
    thisrow[-1] = "{:.2f}".format(thisrow[-1]/100)
    size = len(thisrow[-1])
    final = ""
    for a in range(1,size+1):
      pos = size - a
      if a in [ 6, 9, 12 ]:
        final =  " " + thisrow[-1][pos] + final
      else:
        final =  thisrow[-1][pos] + final
    thisrow[-1]= final
    yield thisrow

@app.route('/')
def index():
  show = request.params.getlist("groupby")
  grouping = show
  groupBy = ", ".join(show)
  if not groupBy == "":
    groupBy = "GROUP BY " + groupBy
  filters = []
  filterssel = {}
  for filter in request.params.getlist("filter"):
    try:
      field, value = filter.split("-",1)
      filterssel[field] = value.decode("utf8")
      filters.append("\"%s\" = \"%s\"" % (field, value))
      show.append(field)
    except:
      pass
  filters = " AND ".join(filters)
  filters = "WHERE " + filters
  if filters == "WHERE ":
    filters = "WHERE 1"
  show = list(set(show))
  show.append("sum(Belopp)")
  shows = ", ".join(show)
  q = "SELECT %s as summa FROM bills %s %s ORDER BY summa DESC;" % (shows, filters, groupBy)
  print q
  result = conn.execute(q)
  headervalues = {}
  for header in headers:
    if header not in [ "belopp exkl moms", "summa", "konto", "organisationsnummer"]:
      q = "SELECT %s FROM bills %s GROUP BY %s ORDER BY %s LIMIT 150;" % (header, filters ,header,header)
      if not header == "verifikationsnummer":
        headervalues[header] = conn.execute(q)
      else:
        headervalues[header] = []
  return template("index.tpl", title="Göteborg" , selected=grouping, filters=filterssel, rows=format(result), headers=show, headervalues=headervalues)

if __name__ == "__main__":
    server = WSGIServer(('0.0.0.0', 9988), app)
    server.serve_forever()
