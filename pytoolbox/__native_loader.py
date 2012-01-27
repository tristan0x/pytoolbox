# This is file is a template used by `multi_imp.load_native_module`.
# Do not use it directly.
#
# Purpose of this module is to import a native library and put all its symbols
# in the module.
#
# It is meant to be used with function `load_native_module` which
# copy this module and a shared library in a temporary directory
# so that Python believes it does not have loaded this module yet.
#

def __feed_current_module():
    """Load the native module and put its symbols in the current module."""

    # Load the native library located in the same directory than this module
    import os.path as osp
    import sys
    import imp
    native_module_name = '%(nativemod)s'
    fp, pathname, description = imp.find_module(native_module_name,
                                                [osp.dirname(__file__)])
    if fp is not None:
        try:
            _mod = imp.load_module(native_module_name, fp,
                                   pathname, description)
        finally:
            fp.close()
    else:
        raise 'Could not find native module: ' + native_module_name

    # get all symbols of the native module and put them in the current module
    for s in filter(lambda s: s not in set(['__doc__', '__file__',
                                            '__name__', '__package__']),
                    dir(_mod)):
        setattr(sys.modules[__name__], s, getattr(_mod, s))

__feed_current_module()
del __feed_current_module
