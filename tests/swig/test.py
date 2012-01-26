
from load_native_module import *
import logging
import sys

def test():
    with load_native_module('native_module') as nm1, \
         load_native_module('native_module') as nm2:
        # static variable are initialized with the same value.
        if nm1.cvar.value != nm2.cvar.value:
            return False
        nm1.cvar.value = nm2.cvar.value + 1
        # they are different instance...
        if nm1.cvar.value == nm2.cvar.value:
            return False

        with load_native_module('native_module') as nm3:
            nm3.cvar.value = 42
            # they all have different values
            if len(set(map(lambda m: m.cvar.value,
                           [nm1, nm2, nm3]))) != 3:
                return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(int(not(test())))

