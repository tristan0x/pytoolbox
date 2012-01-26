PYTHON ?= python
F2PY ?= f2py

PYMODULE = _fmodule

all: $(PYMODULE).so

$(PYMODULE).so: test.f90
	$(F2PY) -c test.f90 -m $(PYMODULE)

clean:

distclean: clean
	$(RM) $(PYMODULE).so *.pyc

test:
	$(PYTHON) test.py
