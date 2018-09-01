# -*- coding: utf-8 -*-

import logging

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


class ProbabilisticSpellChecker(object):

    def __init__(self, word_counts, word_whitelist, charset=None):
        total_word_count = float(sum(word_counts.values()))
        self.word_probabilities = {
            word: count / total_word_count
            for word, count in word_counts.items()
        }
        self.word_probabilities.update({
            word: 1.0
            for word in word_whitelist
        })
        self.words = set(self.word_probabilities.keys())
        _log.debug(
            "probabilistic spell checker, %i words represent a %i word corpus",
            len(self.words),
            total_word_count,
        )
        if charset:
            self.charset = charset
        else:
            self.charset = "abcdefghijklmnopqrstuvwxyzäöüß"

    def correction(self, word):
        if word in self.words:
            return word
        candidates = self.candidates(word)
        _log.debug("word: %s, candidates: %s", word, candidates)
        if not candidates:
            return None
        most_probable_candidate = max(
            candidates,
            key=self.word_probabilities.get,
        )
        _log.debug(
            "word: %s, most probable candidate: %s",
            word,
            most_probable_candidate,
        )
        return most_probable_candidate

    def candidates(self, word):
        leven_1 = self.levenshtein_1(word).intersection(self.words)
        if leven_1:
            return leven_1
        if len(word) > 2:
            return self.levenshtein_2(word).intersection(self.words)
        return set()

    def levenshtein_1(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word)+1)]
        deletes = [
            left + right[1:]
            for left, right in splits
            if right
        ]
        swaps = [
            left + right[1] + right[0] + right[2:]
            for left, right in splits
            if len(right) > 1
        ]
        replaces = [
            left + ch + right[1:]
            for left, right in splits
            if right
            for ch in self.charset
        ]
        inserts = [
            left + ch + right
            for left, right in splits
            for ch in self.charset
        ]
        return set(deletes + swaps + replaces + inserts)

    def levenshtein_2(self, word):
        return set(
            leven_2
            for leven_1 in self.levenshtein_1(word)
            for leven_2 in self.levenshtein_1(leven_1)
        )
