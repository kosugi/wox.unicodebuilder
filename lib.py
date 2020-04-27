# -*- coding: utf-8 -*-

from contextlib import closing
import re
import unicodedata
import sqlite3

def normalize(value):
    return unicodedata.normalize('NFKC', value)

def parse_codepoint(query):
    return int(query, 16)

def codepoint2unichr(codepoint):
    return (r'\U' + '%08x' % codepoint).encode('ISO-8859-1').decode('unicode-escape')

pat_unichr = re.compile(r"^u'\\U([0-9a-f]{8})'$")
def unichr2codepoint(s):
    s = normalize(s)
    s = s.strip()
    if len(s) == 1:
        return ord(s)
    m = pat_unichr.match(repr(s))
    return parse_codepoint(m.group(1)) if m else 0

lower_map = dict([(n, chr(n + 0x20)) for n in range(ord(u'A'), ord(u'Z') + 1)])
def lower(s):
    return s.translate(lower_map)

def make_item(data, title, subtitle, dummy=False):
    return {
        'data': data, 'title': title, 'subtitle': subtitle, 'dummy': dummy
    }

def call_with_cursor(args, callback):
    with sqlite3.connect('db') as conn:
        with closing(conn.cursor()) as cursor:
            return callback(cursor, *args)
