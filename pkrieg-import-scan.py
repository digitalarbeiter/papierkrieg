#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import click
from PIL import Image
import pytesseract
import enchant


def words(text):
    return re.findall(r'\w+', text)


@click.command()
@click.option("--input-file", help="file to import")
def main(input_file):
    text = pytesseract.image_to_string(Image.open(input_file), lang="deu")
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
    print("\n".join(clean_text))


if __name__ == "__main__":
    main()
