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
import os
import codecs
from whooshstore import util
from whooshstore.version import __version__
from whoosh import index, sorting
from whoosh.fields import Schema, NUMERIC, ID, TEXT
from whoosh.analysis import SimpleAnalyzer
from whoosh.qparser import QueryParser

def open_index(indexdir, incremental = False):
    """
    Opens the index with the given name. If the directory or the index
    do not yet exist, the are created.

    @type  indexdir: str
    @param indexdir: The name of the index directory.
    @type  incremental: bool
    @param incremental: Whether to preserve existing index content.
    @rtype:  whoosh.Index
    @return: An object representing the index.
    """
    if not os.path.exists(indexdir):
        os.makedirs(indexdir)
    if incremental and index.exists_in(indexdir):
        return index.open_dir(indexdir)
    schema = Schema(number=NUMERIC(stored = True),
                    filename=ID(stored = True),
                    line=TEXT(analyzer = SimpleAnalyzer(), stored = True))
    return index.create_in(indexdir, schema)

def update_index(files,
                 ix           = 'indexdir',
                 incremental  = False,
                 batch        = False,
                 tmpdir       = None,
                 on_next_file = None):
    """
    Updates the given index. If an index object is not passed, it is
    loaded from (or created in) a directory named 'indexdir' in the
    current working directory.
    """
    # Load or create the index.
    if isinstance(ix, str):
        ix = open_index(ix, incremental)

    # Index the file content.
    if batch:
        writer = ix.writer(dir = tmpdir)
    for fileno, filename in enumerate(files, 1):
        if on_next_file:
            on_next_file(fileno, filename)
        if not os.path.exists(filename):
            continue # File may have disappeared after we found it.
        if not batch:
            writer = ix.writer(dir = tmpdir)
        if incremental:
            writer.delete_by_term('filename', filename)
        for number, line in enumerate(codecs.open(filename, 'r', 'latin-1'), 1):
            writer.add_document(filename = filename,
                                number = number,
                                line = line.rstrip('\n'))
        if not batch:
            writer.commit()
    if batch:
        writer.commit()

def search(term, ix = 'indexdir', limit = None):
    # Load the index.
    if isinstance(ix, str):
        ix = index.open_dir(ix)

    # Parse the search terms.
    s = ix.searcher()
    parser = QueryParser('line', schema = ix.schema)
    q = parser.parse(term)

    # Search and sort the results.
    mf = sorting.MultiFacet()
    mf.add_field('filename')
    mf.add_field('number')
    return s.search(q, limit = limit, sortedby = mf)

def search_page(term, ix = 'indexdir', page = None, pagelen = 20):
    # Load the index.
    if isinstance(ix, str):
        ix = index.open_dir(ix)

    # Parse the search terms.
    s = ix.searcher()
    parser = QueryParser('line', schema = ix.schema)
    q = parser.parse(term)

    # Search and sort the results.
    mf = sorting.MultiFacet()
    mf.add_field('filename')
    mf.add_field('number')
    return s.search_page(q, page, pagelen = pagelen, sortedby = mf)
