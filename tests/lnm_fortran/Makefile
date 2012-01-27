ifeq ($(shell [ -f ../../env.mk ] && echo 1),1)
include ../../env.mk
else
$(error Missing file ../../env.mk, please run command ./bootstrap.sh)
endif

export PYTHONPATH := $(PYTHONPATH):$(shell pwd)/../..

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
