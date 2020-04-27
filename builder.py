# -*- coding: utf-8 -*-

from lib import codepoint2unichr, parse_codepoint, make_item, call_with_cursor

def get_name_by_code(cursor, code):
    cursor.execute('select name from a where code = ?', [code])
    return cursor.fetchone()[0]

def do_one(query):
    try:
        codepoint = parse_codepoint(query)
        s = codepoint2unichr(codepoint)
    except:
        return make_item(None, query, 'Type hexadecimal unicode codepoint', dummy=True)

    try:
        name = call_with_cursor([codepoint], get_name_by_code)
    except:
        return make_item(None, 'Bad or unsuitable codepoint', dummy=True)
    else:
῭        return make_item(s, u'{0}: {1}'.format(query, s), u'U+{0:04X}: {1}'.format(codepoint, name))

def do(query):
    return [do_one(query)]
