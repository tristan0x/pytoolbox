PYTHON ?= python
F2PY ?= f2py

PYTHONPATH := $(PYTHONPATH):$(shell pwd)/../../lib
export PYTHONPATH

PYMODULE = _fmodule

all: $(PYMODULE).so

$(PYMODULE).so: test.f90
	$(F2PY) -c test.f90 -m $(PYMODULE)

clean:

distclean: clean
	$(RM) $(PYMODULE).so *.pyc

test:
	@echo PYTHONPATH $(PYTHONPATH)
	$(PYTHON) test.py
