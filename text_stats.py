# -*- coding: utf-8 -*-

import re
from collections import Counter, defaultdict
from itertools import islice, izip

class TextStats():

  RE = {
    'words':        re.compile(ur"[\w'\u2019]+"),
    'sentence_end': re.compile(r"[\.!?;][\"]?\s+"),
    'paragraph':    re.compile(r".+\n|\n.+$"),
  }

  def __init__(self, text):
    self._text = text or u''

  def calculate(self):
    stats = {
      'wordCount':        len(self._get_words()),
      'sentenceCount':    len(self._get_sentences()),
      'firstSentence':    self._get_sentences()[0],
      'paragraphCount':   self._get_paragraph_count(),
      'wordLengthCounts': self._get_word_length_counts(),
    }
    most_common_bigram = self._get_most_common_ngram(2)
    if (most_common_bigram):
      stats['bigram'] = most_common_bigram
    most_common_trigram = self._get_most_common_ngram(3)
    if (most_common_trigram):
      stats['trigram'] = most_common_trigram
    return stats

  def _get_words(self):
    if not getattr(self, '_words', None):
      self._words = self.RE['words'].findall(self._text)
    return self._words

  def _get_sentences(self):
    if not getattr(self, '_sentences', None):
      self._sentences = self.RE['sentence_end'].split(self._text)
    return self._sentences

  def _get_paragraph_count(self):
    paragraphs = self.RE['paragraph'].findall(self._text)
    return len(paragraphs)

  def _get_most_common_ngram(self, n):
    words = self._get_words()
    sliced_words = [islice(words, i, None) for i in range(1, n)]
    ngrams = izip(words, *sliced_words)
    ngram_counts = Counter(ngrams)
    most_common = ngram_counts.most_common(1)
    if len(most_common):
      return {
        'words': ' '.join(most_common[0][0]),
        'count': most_common[0][1],
      }

  def _get_word_length_counts(self):
    words = self._get_words()
    length_counts = defaultdict(int)
    for word in words:
      length_counts[len(word)] += 1
    return {
      'lengths': map(str, length_counts.keys()),
      'counts': length_counts.values()
    }


