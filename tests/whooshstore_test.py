# Copyright (c) 2010-2017 Samuel Abels
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import print_function
import sys
import unittest
import re
import os
import codecs
from glob import glob
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from whooshstore import util, open_index, update_index, search

dirname = os.path.dirname(__file__)
data_dir = os.path.join(dirname, 'data')
index_dir = os.path.join(dirname, 'index')

def _dosearch(ix, term, limit=None):
    result = search(term, ix=ix, limit=limit)
    result_dict = {}
    for hit in result:
        key = hit['filename'] + '/' + str(hit['number'])
        result_dict[key] = hit['line']
    return result_dict

class whooshstoreTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def testIndex(self):
        # Create an index.
        ix = open_index(index_dir)
        files = util.find_files(data_dir, ('*.txt',))
        update_index(files, ix=ix, incremental=False, batch=True)

        # Test the index.
        result = _dosearch(ix, 'here')
        self.assertEqual(2, len(result))
        expected = {data_dir + u'/file1.txt/2': u'line two here',
                    data_dir + u'/file2.txt/2': u'LINE two here'}
        self.assertEqual(expected, result)

        # Another test.
        result = _dosearch(ix, 'here', 1)
        self.assertEqual(1, len(result))

        # Another test.
        result = _dosearch(ix, 'line')
        self.assertEqual(6, len(result))

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(whooshstoreTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
