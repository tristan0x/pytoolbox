Here the procedure to follow in order to use your fortran
module with the fonction `load_native_module`:

1.  Use f2py  to  build the  shared  library. The  module  name must  be
prefixed by _
1.  Copy paste file `fmodule.py' in the path of the shared library.
1.  Rename it against the module (without the leading _)
1.  Edit it to declare your fortran modules.

Say your Python module is `foo`, you should have the following files:

    $ ls
    foo.py _foo.so

Now run the following test to make sure you can access your modules:

    $ python
    >>> import foo
    >>> dir(foo.ONE_OF_YOUR_MODULE)

That's it, you are ready to use `load_native_module`.
