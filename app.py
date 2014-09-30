# -*- coding: utf-8 -*-

import re
import sys
import requests
from flask import Flask, jsonify, render_template, request
from lxml import html
from text_stats import TextStats

RE_MEDIUM_URL = re.compile(r"(http(s)?://)?(www\.)?medium.com/")

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/api/calculate", methods=['POST'])
def calculate():
  text = request.form['text']
  if RE_MEDIUM_URL.match(text):
    text = _get_text_from_medium_url(text)
  ts = TextStats(text)
  stats = {
    'wordCount':        len(ts.get_words()),
    'sentenceCount':    len(ts.get_sentences()),
    'firstSentence':    ts.get_sentences()[0],
    'paragraphCount':   ts.get_paragraph_count(),
    'wordLengthCounts': ts.get_word_length_counts(),
  }
  most_common_bigram = ts.get_most_common_ngram(2)
  if (most_common_bigram):
    stats['bigram'] = most_common_bigram
  most_common_trigram = ts.get_most_common_ngram(3)
  if (most_common_trigram):
    stats['trigram'] = most_common_trigram
  return jsonify(**stats)

def _get_text_from_medium_url(url):
  if not url.startswith('http'):
    url = "https://%s" % url
  response = requests.get(url)
  dom = html.fromstring(response.text)
  text_nodes = dom.cssselect('[class^="graf--"]:not([class*="graf--empty"]):not([class*="graf--figure"])')
  return '\n'.join([node.text_content() for node in text_nodes])

if __name__ == "__main__":
  app.run(debug=True)
