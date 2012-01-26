
PYTHON ?= python
PYTHONPATH := $(PYTHONPATH):$(PWD)/lib
export PYTHONPATH
export PYTHON

DIST_NAME = py_load_native_module_more_than_once
DIST_FILES = $(SUBDIRS) Makefile

SUBDIRS = tests

all:
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)

clean:
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)
	$(RM) $(DIST_NAME).tar.bz2

distclean: clean
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)
	$(RM) $(SHARED_LIBRARY_NAME) *.pyc


test: all
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;	)
	$(RM) -f lib/*.pyc

dist: distclean
	$(RM) -r $(DIST_NAME)
	mkdir $(DIST_NAME)
	cp -r $(DIST_FILES) $(DIST_NAME)
	tar jcf $(DIST_NAME).tar.bz2 $(DIST_NAME)
	$(RM) -r $(DIST_NAME)


# To put in the documentation:
# Tested with swig 2.0.4 and python 2.7.1
