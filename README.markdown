PyToolBox
=========

Purpose is to centralize reusable code.

Here is the list of existing modules:

*   load\_native\_module


How to build the tests?
-----------------------

Simply run the command `make test`. It will build and run all tests.

By default, the following tools and libraries are required:

*    gcc
*    swig
*    a fortran 90 compiler
*    f2py
*    Boost.Python

It assumes everything is located in standard directories a.k.a `/usr` or `/usr/local`. If this is not the case, you can force location of tools / libraries by setting the following environment variables:

*    `CC`: path to gcc
*    `PYTHON`: path to python
*    `SWIG`: path to swig
*    `F2PY`: path to f2py
*    `BOOST_INCLUDE_PATH`: location of Boost headers
*    `BOOST_LIBRARY_PATH`: location of Boost shared libraries.

By default, all tests are built and run. tests suites are located in the `tests` sub-directory. To desactivate a test, set the environment variable: `NO_TEST_<TESTNAME>`, for example `NO_TEST_LNM_FORTRAN`.

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

