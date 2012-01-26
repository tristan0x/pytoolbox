PYTHON ?= python

SUBDIRS = lnm_fortran lnm_swig lnm_boostpython # embeddedpython


all clean distclean test:
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)
