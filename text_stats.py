# -*- coding: utf-8 -*-

import re
from collections import Counter, defaultdict
from itertools import islice, izip

RE_WORDS        = re.compile(ur"[\w'\u2019]+")
RE_SENTENCE_END = re.compile(r"[\.!?;][\"]?\s+")
RE_PARAGRAPH    = re.compile(r".+(?=\n)|(?<=\n).+$")

class TextStats():
  def __init__(self, text):
    self._text = text or u''

  def get_words(self):
    if not getattr(self, '_words', None):
      self._words = RE_WORDS.findall(self._text)
    return self._words

  def get_sentences(self):
    if not getattr(self, '_sentences', None):
      self._sentences = RE_SENTENCE_END.split(self._text)
    return self._sentences

  def get_paragraph_count(self):
    paragraphs = RE_PARAGRAPH.findall(self._text)
    return len(paragraphs)

  def get_most_common_ngram(self, n):
    words = self.get_words()
    sliced_words = [islice(words, i, None) for i in range(1, n)]
    ngrams = izip(words, *sliced_words)
    ngram_counts = Counter(ngrams)
    most_common = ngram_counts.most_common(1)
    if len(most_common):
      return {
        'words': ' '.join(most_common[0][0]),
        'count': most_common[0][1],
      }

  def get_word_length_counts(self):
    words = self.get_words()
    length_counts = defaultdict(int)
    for word in words:
      length_counts[len(word)] += 1
    return length_counts
