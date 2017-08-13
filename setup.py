import sys, os
from setuptools import setup, find_packages

# Import the file that contains the version number.
src_dir = os.path.join(os.path.dirname(__file__), 'whooshstore')
sys.path.insert(0, src_dir)
from version import __version__

# Import the project description from the README.
readme = open('README').read()
start  = readme.index('\n\n')
end    = readme.index('\n\n=')
descr  = readme[start:end].strip()

# Run the setup.
setup(name             = 'whooshstore',
      version          = __version__,
      description      = 'Whoosh based file indexer and search',
      long_description = descr,
      author           = 'Samuel Abels',
      author_email     = 'knipknap@gmail.com',
      license          = 'GPLv2',
      package_dir      = {'': '.'},
      packages         = [p for p in find_packages()],
      scripts          = ['ws-update', 'ws'],
      install_requires = ['Whoosh'],
      keywords         = 'index search whoosh grep id-utils fulltext',
      url              = 'http://github.com/knipknap/whooshstore',
      classifiers      = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ])
