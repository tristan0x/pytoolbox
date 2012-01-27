PyToolBox
=========

Purpose is to centralize reusable code.

Here is the list of existing modules:

*   load\_native\_module

How to install?
---------------

PyToolBox is a standard distutils package. To install it:

    $ python setup.py install

How to build the tests?
-----------------------

Use the configure script to reference tools and paths if not defined in standard location:
    $ ./configure

Documentation available via `./configure --help`

Then execute the command `make test` to build and run tests.

### load\_native\_module

Python prevents loading a module more than once. But sometimes, you really
need to deal with several instances of the same module.

with a pure Python module, it's pretty easy:

    def load_module(name):
        assert(isinstance(name, str))
        sys.modules.pop(name, None)
        __import__(name)

But when it comes to import native libraries, it's a different story.
It turns out a Python module's hash key is the absolute path to that module.
So to get n instances of the same module, a workaround is to have n versions
of the files on your filesystem in different locations.

This is what this function is doing : each time a new instance of a module
is asked, it copies both Python module and its shared library in a fresh temporary
directory and load it as a new module.

`load_native_library` can not load directly the shared library. You need to write
an intermediate layer module. If you are using Swig, there is already one.

#### Usage

    from load_native_module import *
    with load_native_module('a_swig_generated_module') as m:
        # do stuff
        # [...]
    # At this point, the temporary directory is deleted.

#### Notes

If a module submitted to `load_native_module` has not been loaded yet,
the function uses the `classic' module load. But things will get dirty
next time :)

#### Tests
On linux only:

*   Swig 1.3 and Python 2.6
*   Swig 2.0.4 and Python 2.7.1
