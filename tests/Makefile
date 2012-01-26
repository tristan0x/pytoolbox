PYTHON ?= python

SUBDIRS = fortran swig boostpython embeddedpython


all clean distclean test:
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)
