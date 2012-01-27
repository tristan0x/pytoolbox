PYTHON ?= python
F2PY ?= f2py

PYTHONPATH := $(PYTHONPATH):$(shell pwd)/../..
export PYTHONPATH

PYMODULE = fmodule

all: $(PYMODULE).so

$(PYMODULE).so: test.f90
	$(F2PY) -c test.f90 -m $(PYMODULE)

clean:

distclean: clean
	$(RM) $(PYMODULE).so *.pyc

test: all
	@echo PYTHONPATH $(PYTHONPATH)
	$(PYTHON) test.py
