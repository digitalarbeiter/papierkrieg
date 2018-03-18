#!/usr/bin/python3
# -*- coding: utf-8 -*-

import click
import hashlib
import logging
import time

import papierkrieg.searching as search
import papierkrieg.scan2doc as scan2doc


@click.command()
@click.option("--input-file", help="file to import")
def main(input_file):
    click.echo("importing document {} ...".format(input_file))
    h = hashlib.md5()
    h.update(input_file.encode("utf-8"))
    doc_id = h.hexdigest()
    original_text = scan2doc.extract(input_file)
    click.echo("document {} contains {} chars: {} [...]".format(
        input_file,
        len(original_text),
        original_text[:20],
    ))
    search.index({
        "id": doc_id,
        "resource": input_file,
        "create_date": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "original": original_text,
    })
    click.echo("imported document {} as {}".format(input_file, doc_id))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARN)
    main()
