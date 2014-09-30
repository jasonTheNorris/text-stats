# -*- coding: utf-8 -*-

import re
import sys
import requests
from flask import Flask, jsonify, render_template, request
from lxml import html
from text_stats import TextStats

MEDIUM_URL_RE = re.compile(r"(http(s)?://)?(www\.)?medium.com/")

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/api/calculate", methods=['POST'])
def calculate():
  text = request.form['text']
  if MEDIUM_URL_RE.match(text):
    text = _get_text_from_medium_url(text)
  stats = TextStats(text).calculate()
  return jsonify(**stats)

def _get_text_from_medium_url(url):
  if not url.startswith('http'):
    url = "https://%s" % url
  response = requests.get(url)
  dom = html.fromstring(response.text)
  text_nodes = dom.cssselect('[class^="graf--"]:not([class*="graf--empty"]):not([class*="graf--figure"])')
  return '\n'.join([node.text_content() for node in text_nodes])

if __name__ == "__main__":
  app.run()
