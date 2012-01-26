import logging
import sys

from pytoolbox import *

def test():
  with load_native_module('hello') as h1, \
      load_native_module('hello') as h2:
    h1.incrvalue()
    h1.incrvalue()
    assert h1.value() == 2
    assert h2.value() == 0
    h2.incrvalue()
    assert h1.value() == 2
    assert h2.value() == 1
  return True

if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  sys.exit(int(not(test())))
