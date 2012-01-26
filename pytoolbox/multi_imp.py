
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

# TODO: create a dumb a C extension and update `load_native_module' accordingly:
#   if the module's name to load starts with `_' (a native one):
#     only copy the shared library
#   else:
#     look for the shared library path instead of picking it in the same directory
#     than the Python module.

class load_native_module:
    """Return a new instance of a module
    This class is meant to be used within a "with" context, ex:

    with load_native_module('myfortranmodule') as m:
        # do stuff
    """

    def __init__(self, name):
        """name: name of the module to import"""
        assert isinstance(name, str)
        self.__name = name
        self.__modulepath = None

        if name.startswith('_'):
            raise ImportError(textwrap.dedent("""
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
            modulename = osp.basename(modulepath)
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
        if self.__modulepath and osp.isdir(self.__modulepath):
            logging.debug("Deleting directory: " + self.__modulepath)
            shutil.rmtree(self.__modulepath)
            # FIXME: the module should be properly dereferenced
