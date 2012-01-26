Here the procedure to follow in order to use your fortran
module with the fonction `load_native_module`:

### Build the native module and copy the intermediate loader

1.  Use f2py  to  build the  shared  library. The  module  name given
to f2py must  be prefixed by _
1.  Copy paste file `fmodule.py` in the path of the shared library.
1.  Rename it against the module (without the leading _)

Say your Python module is `foo`, you should have the following files:

    $ ls
    foo.py _foo.so
    $

### First test

Now run the this simple test to make sure the loader can import your
native module:

    $ python
    >>> import foo
    >>> dir(foo.ONE_OF_YOUR_MODULE)

### Ready for `load_native_module`

That's it, you are ready to deal with multiple instances of the native
library within the same Python process:

    $ python
    >>> from pytoolbox import *
    >>> with load_native_module('fmodule') as fmodule1, \
    ...      load_native_module('fmodule') as fmodule2:
    ...    # do stuff
    ...    # [...]



