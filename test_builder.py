# -*- coding: utf-8 -*-

import unittest
from builder import *

class PreprocessTestCase(unittest.TestCase):

    def test_parse_codepoint(self):
        try:
            self.assertEqual(0, parse_codepoint(''))
            self.fail()
        except:
            self.assertTrue(True)

        self.assertEqual(0, parse_codepoint('0'))
        self.assertEqual(0x10, parse_codepoint('10'))
        self.assertEqual(0x12000, parse_codepoint('012000'))

    def test_do(self):
        r = do('')[0]
        self.assertEqual(r['data'], None)
        self.assertEqual(r['subtitle'], '')
        self.assertEqual(r['dummy'], True)

        r = do('a')[0]
        self.assertEqual(r['data'], None)
        self.assertEqual(r['title'], 'a')
        self.assertEqual(r['subtitle'], 'Bad or unsuitable codepoint')
        self.assertEqual(r['dummy'], True)

        r = do('0021')[0]
        self.assertEqual(r['data'], '!')
        self.assertEqual(r['subtitle'], 'U+0021: EXCLAMATION MARK')
        self.assertEqual(r['dummy'], False)

        r = do('200B')[0]
        self.assertEqual(r['data'], '\u200b')
        self.assertEqual(r['subtitle'], 'U+200B: ZERO WIDTH SPACE')
        self.assertEqual(r['dummy'], False)

if __name__ == '__main__':
    unittest.main()
