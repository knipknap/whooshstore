#!/usr/bin/env python
# Copyright (C) 2010 Samuel Abels.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2, as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import sys
from optparse import OptionParser
from whooshstore import __version__, search, search_page

# Define CLI syntax.
parser = OptionParser(usage = '%prog [options] term', version = __version__)
parser.add_option('--page', '-p',
                  type    = 'int',
                  dest    = 'page',
                  metavar = 'INT',
                  default = None,
                  help    = 'Return only the given page of the results')
parser.add_option('--pagelen', '-P',
                  dest    = 'pagelen',
                  type    = 'int',
                  metavar = 'INT',
                  default = 20,
                  help    = 'The number of results per page. Implies -p0')
parser.add_option('--limit', '-l',
                  dest    = 'limit',
                  type    = 'int',
                  metavar = 'INT',
                  default = None,
                  help    = 'The maximum number of results')
parser.add_option('--index', '-i',
                  dest    = 'index',
                  metavar = 'STRING',
                  default = 'indexdir',
                  help    = 'Use the given index directory')

# Parse options.
options, args = parser.parse_args(sys.argv)
args.pop(0)

try:
    querystring = u' '.join(args)
except IndexError:
    parser.error('missing search term')

if options.page is not None:
    try:
        results = search_page(querystring,
                              ix = options.index,
                              page = options.page,
                              pagelen = options.pagelen)
    except ValueError, e:
        parser.error(e)
else:
    results = search(querystring,
                     ix    = options.index,
                     limit = options.limit)

for result in results:
    print '%s:%d: %s' % (result['filename'], result['number'], result['line'])
