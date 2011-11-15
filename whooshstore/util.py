import os
import fnmatch

def filter_by_pattern(input, patterns):
    if patterns is None:
        return input
    output = set()
    for pattern in patterns:
        output.update(fnmatch.filter(input, pattern))
    return output

def find_files(directory, patterns = None):
    """
    If patterns is None, return all files from the given directory.
    """
    for root, dirnames, filenames in os.walk(directory):
        for filename in filter_by_pattern(filenames, patterns):
            yield unicode(os.path.join(root, filename), 'latin-1')
