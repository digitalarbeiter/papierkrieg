#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click
import hashlib
import logging
import json
import time

import enchant
import probspellchecker

import papierkrieg.searching as search
import papierkrieg.scan2doc as scan2doc



WORDS = json.load(open("probspellchecker/dictionary_dewiki_full10plus.json"))
CUSTOM_DICT = [
    "schemitz",
    "heß",
    "kompetenzaussage",
    "antwortfeld",
    "diakonissenstraße",
    "patientenbefragung",
    "krankenhausinformation",
]


@click.command()
@click.option("--input-file", help="file to import")
def main(input_file):
    click.echo("loading spellchecker...")
    spellchecker = probspellchecker.ProbabilisticSpellChecker(WORDS, CUSTOM_DICT)
    #spellchecker = enchant.Dict("de_DE")
    click.echo("importing document {} ...".format(input_file))
    h = hashlib.md5()
    h.update(input_file.encode("utf-8"))
    doc_id = h.hexdigest()
    original_text = scan2doc.extract(
        input_file,
        spellchecker=spellchecker.correction,  # for ProbabilisticSpellChecker
        #spellchecker=spellchecker.suggest,  # for enchant.Dict
    )
    click.echo("document {} contains {} chars: {} [...]".format(
        input_file,
        len(original_text),
        original_text[:20],
    ))
    #search.index({
    #    "id": doc_id,
    #    "resource": input_file,
    #    "create_date": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    #    "original": original_text,
    #})
    click.echo("imported document {} as {}".format(input_file, doc_id))
    print(original_text)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARN)
    main()
