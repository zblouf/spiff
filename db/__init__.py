# -*- coding: utf_8 -*-

# spiff, a python-based framework
# Copyright (c) 2006-2020, Romain Gaches, <romain@ssji.net>
#
# db module

import types
#from xml.etree import ElementTree

from spiff.db import dbms

def dbms_factory(params_dict):
    _type = params_dict['type'].lower()
    if _type in dir(dbms):
        _db = getattr(dbms, _type).db()
        _db.connect(params_dict)
        return _db
    else:
        return False

# XML Utilities

def extract_dbs(xml_doc):
    pass

def extract_db(xml_doc, dbname):
    db_tags = xml_doc.findall("db")
    for db_tag in db_tags:
        if db_name == db_tag.get("name"):
            return extract_db_params(db_tag)
    return False

def extract_db_names(xml_doc):
    names = []
    db_tags = xml_doc.findall("db")
    for db_tag in db_tags:
        names.append(db_tag.get("name"))
    return names

def extract_db_params(db_tag):
    params = {}
    params ["name"] = db_tag.get("name")
    for child in db_tag.getchildren():
        if child.text == None:
            params[cild.tag] = ""
        else:
            params[child.tag] = child.text
    return params
