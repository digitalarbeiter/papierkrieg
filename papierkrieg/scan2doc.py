# -*- coding: utf-8 -*-

import logging
import re

import enchant
from PIL import Image
import pytesseract


_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


def extract(image_file):
    text = pytesseract.image_to_string(Image.open(image_file), lang="deu")
    dictionary = enchant.Dict("de_DE")
    clean_text = []
    for word in re.findall(r"\w+", text):
        word = word.strip()
        if not word:
            continue
        if dictionary.check(word):
            clean_text.append(word)
        else:
            suggestions = dictionary.suggest(word)
            if suggestions:
                clean_text.append(suggestions[0] + "=" + word)
            else:
                clean_text.append(word + "?")
    return " ".join(clean_text)
