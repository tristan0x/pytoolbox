import logging
import sys

from pytoolbox import *

def cmp_fortran_array(a1, a2):
    if len(a1) != len(a2):
        return False
    for i in range(len(a1)):
        if a1[i] != a2[i]:
            return False
    return True

def test():
    with load_native_module('_fmodule') as fm1, \
         load_native_module('_fmodule') as fm2:
        if not cmp_fortran_array(fm1.data.test_array, fm2.data.test_array):
            return False
        fm1.data.test_array = [1, 2, 3, 4, 5]
        if cmp_fortran_array(fm1.data.test_array, fm2.data.test_array):
            return False
    return True

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(int(not(test())))

