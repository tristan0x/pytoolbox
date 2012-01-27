
from contextlib import contextmanager
import imp
import inspect
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
    """Get a new fresh instance of a native module.
    If you intend to load a swig module, provide name of the Python wrapper,
    otherwise simply provide the native module name.

    This class is meant to be used in a "with" context, for example:

        with load_native_module('myfortranmodule') as m:
            # do stuff
    """
    def __init__(self, name):
        """name: a module or the string representing the module to import"""
        if not isinstance(name, str):
            assert inspect.ismodule(name)
            self.__name = name.__name__
        else:
            assert isinstance(name, str)
            self.__name = name
        self.__modulepath = None

    def __enter__(self):
        self.__ensure_exists()
        if self.__is_native:
            logging.debug("loading native library in a temp dir")
        else:
            if not sys.modules.has_key(self.__name):
                pass
                logging.debug("First import of python module `%s'." %
                              self.__name)
                return __import__(self.__name)
            else:
                logging.debug("Module `%s' is already loaded, creating temp directory." %
                              self.__name)

        self.__modulepath = tempfile.mkdtemp(prefix='py_module' + self.__name)

        if self.__is_native:
            mod2load = 'loader_' + self.__name
            nativemod = self.__name
            dest = osp.join(self.__modulepath, mod2load + '.py')
            logging.debug("Generate %s from %s" %
                          (dest, load_native_module.__NATIVE_LOADER))
            with open(dest, 'w') as sw, \
                 open(load_native_module.__NATIVE_LOADER, 'r') as sr:
                sw.write(sr.read() % {'nativemod': nativemod})
        else:
            # probably a swig module, copy the .py in temp dir
            mod2load = self.__name
            self.__copy(sys.modules[self.__name].__file__)
            nativemod = '_' + self.__name

        # get path to native module and copy it in temp dir
        fp = None
        try:
            fp, path, desc = imp.find_module(nativemod)
            self.__copy(path)
        except ImportError:
            logging.debug("It seems there is not shared library named `%s'." %
                          nativename)
            raise
        finally:
            if fp:
                fp.close()

        # Now import the loader copied in temp dir
        fp, path, desc  = imp.find_module(mod2load, [self.__modulepath])
        try:
            finalmodname = osp.basename(self.__modulepath)
            logging.debug("Loading module `%s' as `%s'" %
                          (mod2load, finalmodname))
            return imp.load_module(finalmodname, fp, path, desc)
        finally:
            if fp:
                fp.close()


    def __exit__(self, type, value, traceback):
        if self.__modulepath and osp.isdir(self.__modulepath):
            logging.debug("Deleting directory: " + self.__modulepath)
            shutil.rmtree(self.__modulepath)
            # FIXME: the module should be properly dereferenced


    def __ensure_exists(self):
        fp, path, desc = imp.find_module(self.__name)
        if fp is not None:
            fp.close()
            self.__is_native = desc[2] == imp.C_EXTENSION
        else:
            raise ImportError("No such module " + self.__name)


    def __copy(self, src, name=None):
        import os.path
        if name is not None:
            dest = os.path.join(self.__modulepath, name)
        else:
            dest = self.__modulepath
        logging.debug("Copy %s %s " % (src, dest))
        shutil.copy(src, dest)


    """A template of native module loader."""
    __NATIVE_LOADER = osp.join(osp.dirname(__file__),
                               '__native_loader.py')
