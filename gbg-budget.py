#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sqlite3
conn = sqlite3.connect('gbg.db')

headers = [
  "förvaltning", 
  "leverantör",
  "organisationsnummer",
  "verifikationsnummer",
  "konto",
  "kontotext",
  "belopp exkl moms"]

types = [
  "text",
  "text",
  "int",
  "int",
  "int",
  "text",
  "real"]

urls = ["https://catalog.goteborg.se/rowstore/dataset/62244395-eb02-41eb-94ce-0ab89378932a"]

cols = []
for i in range(0,len(headers)):
  cols.append(headers[i] + " " + types[i])
cols = ', '.join(cols)

make = "CREATE TABLE IF NOT EXISTS bills (%s)" % cols
conn.execute(make)
conn.execute('''CREATE UNIQUE INDEX IF NOT EXISTS verifikationsnummer on bills (verifikationsnummer)''')
conn.commit()

def add_to_db(rader):
  for rad in rader:
    rad["förvaltning"] = rad["﻿förvaltning"]
    cols = []
    for head in headers:
      if head == "belopp exkl moms":
        cols.append(int(rad[head].replace(" ", "").replace(",","")))
      else:
        cols.append(rad[head])
    insert = ('INSERT OR IGNORE INTO bills VALUES ("%s","%s","%s","%s","%s","%s",%i)' % tuple(cols))
    print(insert)
    conn.execute(insert)
  conn.commit()

for url in urls:
  result = requests.get(url, headers={"Accept":"application/json"});
  print(result.content)
  print(result.encoding)
  add_to_db(result.json()["results"])
  while "next" in result.json():
    result = requests.get(result.json()["next"], headers={"Accept":"application/json"});
    add_to_db(result.json()["results"])
