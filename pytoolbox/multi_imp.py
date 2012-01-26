
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
    """Return a new instance of a native module
    This class is meant to be used within a "with" context, ex:

    with load_native_module('myfortranmodule') as m:
        # do stuff
    """
    __NATIVE_LOADER = osp.join(osp.dirname(__file__),
                               '__native_loader.py')
    def __init__(self, name):
        """name: name of the module to import"""
        assert isinstance(name, str)
        self.__name = name
        self.__modulepath = None

    def __enter__(self):
        if self.__name.startswith('_'):
            logging.debug("loading native library in a temp dir")
        else:
            if not sys.modules.has_key(self.__name):
                logging.debug("First import of module `%s'." % self.__name)
                return __import__(self.__name)
            else:
                logging.debug("Module `%s' is already loaded, creating temp directory." %
                              self.__name)


        if self.__name.startswith('_'):
            loadername = self.__name[1:]
            nativename = self.__name
        else:
            loadername = self.__name
            nativename = '_' + self.__name

        self.__modulepath = tempfile.mkdtemp(prefix='py_new_native_module_' +
                                             loadername + '_')
        modulename = osp.basename(self.__modulepath)
        if not self.__name.startswith('_'):
            # probably a swig module
            origmodulepath = sys.modules[self.__name].__file__
            if origmodulepath.endswith('pyc'):
                origmodulepath = origmodulepath[:-1]
            self.__copy(origmodulepath)
            fp = None
        else:
            # importing a native library directly
            # import will be made by our custom loader
            self.__copy(load_native_module.__NATIVE_LOADER,
                        loadername + '.py')

        # get path to native module and copy it in temp dir
        fp = None
        try:
            fp, path, desc = imp.find_module(nativename)
            self.__copy(path)
        except ImportError:
            logging.debug("It seems there is not shared library named `%s'." %
                          nativename)
        finally:
            if fp:
                fp.close()


        # Now import the loader copied in temp dir
        fp, path, desc  = imp.find_module(loadername, [self.__modulepath])
        try:
            logging.debug("Loading module `%s' as `%s'" %
                          (loadername, modulename))
            return imp.load_module(modulename, fp, path, desc)
        finally:
            if fp:
                fp.close()

    def __copy(self, src, name=None):
        import os.path
        if name is not None:
            dest = os.path.join(self.__modulepath, name)
        else:
            dest = self.__modulepath
        logging.debug("Copy %s %s " % (src, dest))
        shutil.copy(src, dest)

    def __exit__(self, type, value, traceback):
        if self.__modulepath and osp.isdir(self.__modulepath):
            logging.debug("Deleting directory: " + self.__modulepath)
            shutil.rmtree(self.__modulepath)
            # FIXME: the module should be properly dereferenced
