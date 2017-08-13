import sys, os
from setuptools import setup, find_packages

# Import the file that contains the version number.
src_dir = os.path.join(os.path.dirname(__file__), 'whooshstore')
sys.path.insert(0, src_dir)
from version import __version__

# Import the project description from the README.
descr  = '''
Whooshstore is a simple Python module for indexing and searching files
on your local hard drive. It supports incremental indexing, pagination,
and provides a Python API as well as a command line tool.
'''.strip()

# Run the setup.
setup(name             = 'whooshstore',
      version          = __version__,
      description      = 'Whoosh based file indexer and search',
      long_description = descr,
      author           = 'Samuel Abels',
      author_email     = 'knipknap@gmail.com',
      license          = 'MIT',
      package_dir      = {'whooshstore': 'whooshstore'},
      package_data     = {},
      packages         = find_packages(),
      scripts          = ['scripts/ws-update', 'scripts/ws'],
      install_requires = ['Whoosh'],
      keywords         = 'index search whoosh grep id-utils fulltext',
      url              = 'http://github.com/knipknap/whooshstore',
      classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ])
