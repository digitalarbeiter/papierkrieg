# -*- coding: utf-8 -*-

import logging
import re

from PIL import Image
import pyocr.tesseract as pytesseract

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


def extract(image_file, spellchecker=None):
    text = pytesseract.image_to_string(Image.open(image_file), lang="deu")
    clean_text = []
    for word in re.findall(r"\w+", text):
        word = word.strip()
        if not word:
            continue
        if word.isdigit():
            clean_text.append(word)
            continue
        if len(word) == 1:
            clean_text.append(word)
            continue
        if spellchecker:
            correction = spellchecker(word.lower())
            if correction and not isinstance(correction, str):
                # some spellcheckers return a list of suggestions -> use
                # first suggestion
                correction = correction[0]
        else:
            correction = None
        if correction:
            if word[0].isupper():
                # keep capitalization of first char.
                correction = correction[0].upper() + correction[1:]
            clean_text.append(correction)
        else:
            clean_text.append(word + "?")
    emails = []
    for email in re.findall(
        "\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        text,
        flags=re.UNICODE+re.IGNORECASE,
    ):
        _log.debug("email: %s", email)
        emails.append(email)
    return " ".join(clean_text), emails
