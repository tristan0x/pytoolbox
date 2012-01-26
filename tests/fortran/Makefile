PYTHON ?= python

PYMODULE = _fmodule

all: $(PYMODULE).so

$(PYMODULE).so: test.f90
	f2py -c test.f90 -m $(PYMODULE)


clean:

distclean: clean
	$(RM) $(PYMODULE).so *.pyc

test:
	$(PYTHON) test.py
