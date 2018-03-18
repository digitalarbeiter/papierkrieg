# -*- coding: utf-8 -*-
# searching: search index related functions

import io
import json
import logging
import requests


_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


SOLR_URL = "http://localhost:8983/solr/papierkrieg/"


def solr_post(url, endpoint, json_data):
    _log.debug(
        "POST %s\n%r",
        url + endpoint,
        json_data,
    )
    response = requests.post(
        url + endpoint,
        json=json_data,
        headers={"Content-type": "application/json"},
    )
    _log.debug(
        "HTTP status %i",
        response.status_code,
    )


def delete_index():
    solr_post(SOLR_URL, "update", {
        "delete": {"query": "*:*"},
    })
    solr_post(SOLR_URL, "update", {
        "commit": {},
    })


def index(doc):
    doc["content"] = " ".join([
        doc.get("original", ""),
        doc.get("tags", ""),
        doc.get("resource", ""),
        doc.get("create_date", ""),
    ])
    solr_post(SOLR_URL, "update/json/docs", doc)
    solr_post(SOLR_URL, "update", {
        "commit": {},
    })
