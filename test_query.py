# -*- coding: utf-8 -*-

import unittest
from lib import call_with_cursor
from query import *

class QueryTestCase(unittest.TestCase):

    def test_normalize_keywords(self):
        self.assertEqual(u'', normalize_keywords(u''))
        self.assertEqual(u'', normalize_keywords(u'*'))
        self.assertEqual(u'', normalize_keywords(u"'"))
        self.assertEqual(u'', normalize_keywords(u'"'))
        self.assertEqual(u'', normalize_keywords(u':'))
        self.assertEqual(u'', normalize_keywords(u'('))
        self.assertEqual(u'', normalize_keywords(u')'))
        self.assertEqual(u'a*', normalize_keywords(u'a'))
        self.assertEqual(u'a* b*', normalize_keywords(u' a B'))
        self.assertEqual(u'a* b*', normalize_keywords(u' A b'))
        self.assertEqual(u'Σ*', normalize_keywords(u'Σ'))
        self.assertEqual(u'б*', normalize_keywords(u'б'))

    def test_get_row_by_char(self):
        self.assertEqual((0xe5, 'LATIN SMALL LETTER A WITH RING ABOVE'), call_with_cursor(u'å', get_row_by_char))

    def test_error(self):
        r = error('bad')
        self.assertEqual(r['data'], None)
        self.assertEqual(r['subtitle'], 'Something went wrong...')
        self.assertEqual(r['dummy'], True)

    def test_do(self):
        r = do('')[0]
        self.assertEqual(r['data'], None)
        self.assertEqual(r['title'], 'Type any unicode name or character itself')
        self.assertEqual(r['subtitle'], '')
        self.assertEqual(r['dummy'], True)

        r = do('å')[0]
        self.assertEqual(r['data'], '\u00e5')
        self.assertEqual(r['title'], '\u00e5')
        self.assertEqual(r['subtitle'], 'U+00E5: LATIN SMALL LETTER A WITH RING ABOVE')
        self.assertEqual(r['dummy'], False)

        r = do('_dummy_')[0]
        self.assertEqual(r['data'], None)
        self.assertEqual(r['title'], '_dummy_')
        self.assertEqual(r['subtitle'], 'No characters matched')
        self.assertEqual(r['dummy'], True)

        r = do('†')[0]
        self.assertEqual(r['data'], '\u2020')
        self.assertEqual(r['title'], '\u2020')
        self.assertEqual(r['subtitle'], 'U+2020: DAGGER')
        self.assertEqual(r['dummy'], False)

        r = do('fermata')[0]
        self.assertEqual(r['data'], '\u0352')
        self.assertEqual(r['title'], '\u0352')
        self.assertEqual(r['subtitle'], 'U+0352: COMBINING FERMATA')
        self.assertEqual(r['dummy'], False)

        r = do('fermata')[1]
        self.assertEqual(r['data'], '\U0001D110')
        self.assertEqual(r['title'], '\U0001D110')
        self.assertEqual(r['subtitle'], 'U+1D110: MUSICAL SYMBOL FERMATA')
        self.assertEqual(r['dummy'], False)

        r = do('fermata')[2]
        self.assertEqual(r['data'], '\U0001D111')
        self.assertEqual(r['title'], '\U0001D111')
        self.assertEqual(r['subtitle'], 'U+1D111: MUSICAL SYMBOL FERMATA BELOW')
        self.assertEqual(r['dummy'], False)

if __name__ == '__main__':
    unittest.main()
