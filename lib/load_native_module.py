
from contextlib import contextmanager
import imp
import logging
import os
import os.path as osp
import platform
import sys
import shutil
import tempfile
import textwrap

__all__ = ['load_native_module']

class load_native_module:
    """
Python is "smart" because it prevents loading a module more than once.
Yeah this is so cool thank you very much little snake.
But what if you really need to deal with instances of the same module?

With a `classic' python module, this is actually pretty easy:
def classic_module(name):
    assert(isinstance(name, str))
    sys.modules.pop(name, None)
    __import__(name)

But when it comes to loading native libraries, it's a different story.
It turns out a Python module's hash key is the absolute path to that module.
So to get n instances of the same module, a workaround is to have n versions
of the files on your filesystem in different locations.

This is what this class intend to do: each time a new instance of a module
is asked, it copies both Python module and its shared library in a fresh new
directory and load it as a new module.

Usage:
------

    with load_native_module('a_swig_generated_module') as m:
        # do stuff
        # [...]
    # At this point, the temporary directory is deleted.

Notes:
-----
If a module submitted to `load_native_module' has not been loaded yet,
the function uses the `classic' module load. But things will get dirty
next time :)

Limitations:
------------
TODO: create a dumb a C extension and update `load_native_module' accordingly:
  if the module's name to load starts with `_' (a native one):
    only copy the shared library
  else:
    look for the shared library path instead of picking it in the same directory
    than the Python module.

Tested only on Linux 2.6:
- Swig 1.3 and Python 2.6
- Swig 2.0.4 and Python 2.7.1
    """

    def __init__(self, name, tempdir=None):
        assert isinstance(name, str)
        self.__name = name
        self.__modulepath = None

        if name.startswith('_'):
            raise ImportError(textwrap.dedent("""
    Can not load native library directly with this helper function.
    Instead create a python module named after the native library importing
    this native library. (like swig does)
  """))

    def __enter__(self):
        if not sys.modules.has_key(self.__name):
            logging.debug("First import of module `%s' using `classic' method." %
                          self.__name)
            return __import__(self.__name)
        else:
            logging.debug("Module `%s' is already loaded, creating temp directory." %
                          self.__name)
            origmodulepath = sys.modules[self.__name].__file__
            if origmodulepath.endswith('pyc'):
                origmodulepath = origmodulepath[:-1]

            modulepath = tempfile.mkdtemp(prefix='py_new_native_module_' + self.__name + '_')
            modulename = os.path.basename(modulepath)
            self.__modulepath = modulepath
            logging.debug("Copying file " + origmodulepath)
            shutil.copy(origmodulepath, modulepath)

            fp = None
            try:
                fp, path, desc = imp.find_module('_' + self.__name)
                logging.debug("Copy shared library: " + path)
                shutil.copy(path, modulepath)
            except ImportError:
                logging.debug("It seems there is not shared library named `%s'." % ('_' + self.__name))
            finally:
                if fp:
                    fp.close()
            fp, path, desc  = imp.find_module(self.__name, [modulepath])
            try:
                logging.debug("Loading module `%s' as `%s'" %
                              (self.__name, modulename))
                return imp.load_module(modulename, fp, path, desc)
            finally:
                if fp:
                    fp.close()
    def __exit__(self, type, value, traceback):
        if self.__modulepath and os.path.isdir(self.__modulepath):
            logging.debug("Deleting directory: " + self.__modulepath)
            shutil.rmtree(self.__modulepath)
            # FIXME: the module should be properly dereferenced
