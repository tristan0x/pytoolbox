def load_native_module():
    import os.path
    import sys
    import imp
    fp = None
    try:
        print "imp.find_module %s" % os.path.dirname(__file__)
        fp, pathname, description = imp.find_module('_fmodule', [os.path.dirname(__file__)])
        print "pathname: " + pathname
    except ImportError:
        import _fmodule
        return _fmodule
    if fp is not None:
        try:
            _mod = imp.load_module('_fmodule', fp, pathname, description)
        finally:
            fp.close()
        return _mod

_native_module = load_native_module()
del load_native_module

# Declare all modules defined in your Fortan library:
data = _native_module.data
