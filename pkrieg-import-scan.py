#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import re
import click
import hashlib
import time
from PIL import Image
import pytesseract
import enchant

import papierkrieg.searching as search


def words(text):
    return re.findall(r'\w+', text)


@click.command()
@click.option("--input-file", help="file to import")
def main(input_file):
    text = pytesseract.image_to_string(Image.open(input_file), lang="deu")
    click.echo("extracted {} chars: {} [...]".format(len(text), text[:20]))
    dictionary = enchant.Dict("de_DE")
    clean_text = []
    for word in words(text):
        if dictionary.check(word):
            clean_text.append(word)
        else:
            suggestions = dictionary.suggest(word)
            if suggestions:
                clean_text.append(suggestions[0] + "=" + word)
            else:
                clean_text.append(word + "?")
    original_text = " ".join(clean_text)
    h = hashlib.md5()
    h.update(input_file.encode("utf-8"))
    doc_id = h.hexdigest()
    search.index({
        "id": doc_id,
        "resource": input_file,
        "create_date": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "original": original_text,
    })
    click.echo("document {} indexed".format(doc_id))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
