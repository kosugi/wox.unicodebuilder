# -*- coding: utf-8 -*-

from lib import lower, to_item, unichr2codepoint, codepoint2unichr, normalize, call_with_cursor
import re

pat_divide_kwds = re.compile(r'\s+')
def normalize_keywords(query):
    query = normalize(query)
    query = lower(query)
    for x in ('*', "'", '"', ':', '(', ')'):
        query = query.replace(x, ' ')

    kwds = []
    for kwd in pat_divide_kwds.split(query):
        if kwd:
            kwds.append(kwd + '*')
    return u' '.join(kwds)

def do_row(row):
    code, name = row
    c = codepoint2unichr(code)
    return to_item(c, 'U+%04X: %s' % (code, name))

def get_row_by_char(cursor, query):
    try:
        code = unichr2codepoint(query)
        cursor.execute('select code, name from a where code = ?', [code])
        return cursor.fetchone()
    except:
        pass

def get_rows(cursor, query):
    cursor.execute('select code, name from a where name match ?', [normalize_keywords(query)])
    return cursor.fetchmany(30)

def error(s):
    return to_item('Error', 'Something went wrong...', dummy=True)

def make_results(cursor, query):

    if query.strip() == '':
        return [to_item('Type any unicode name or character itself', '', dummy=True)]

    items = []
    try:
        row = get_row_by_char(cursor, query)
        if row:
            items.append(do_row(row))

        rows = get_rows(cursor, query)
        for row in rows:
            items.append(do_row(row))

        if len(items) == 0:
            items.append(to_item(query, 'No characters matched', dummy=True))

        return items
    except Exception as e:
        print(str(e))
        return [error(str(e))]

def do(query):
    return call_with_cursor([query], make_results)
