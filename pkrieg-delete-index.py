#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import papierkrieg.searching as search


def delete_index():
    search.delete_index()
    search.index({
        "id": "1",
        "resource": "/tmp/foobar.jpg",
        "create_date": "2018-01-01T20:00:00Z",
        "original": "dummy document",
    })


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if input("really delete index (enter YES to confirm)? ") == "YES":
        print("deleting index...")
        delete_index()
