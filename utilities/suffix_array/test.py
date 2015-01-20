import unittest

from utilities.suffix_array import applications as app


class SuffixArrayApplicationTest(unittest.TestCase):

    def testACS(self):
        a = u'jeffisacoolguywhoiscool'
        b = u'whoiscooljeffisacoolguy'
        acs = app.all_common_substrings(a, b)
        self.assertIn(u'jeffisacoolguy', acs)
        self.assertIn(u'whoiscool', acs)
        self.assertEqual(len(acs), 2)

        a = u'aabbccdefaabbcc'
        b = u'defabcc'
        acs = app.all_common_substrings(a, b)
        self.assertIn(u'defa', acs)
        self.assertIn(u'bcc', acs)
        self.assertIn(u'ab', acs)
        self.assertEqual(len(acs), 3)
