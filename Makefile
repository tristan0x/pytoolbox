
CFLAGS ?= -fPIC
export CFLAGS

SUBDIRS = tests

DIST_NAME = py_load_native_module_more_than_once
DIST_FILES = $(SUBDIRS) Makefile

all:
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)

clean:
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)
	$(RM) $(DIST_NAME).tar.bz2

distclean: clean
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;)
	$(RM) $(SHARED_LIBRARY_NAME) *.pyc 	pytoolbox/*.pyc


test: all
	$(foreach subdir, $(SUBDIRS), $(MAKE) -C $(subdir) $@ ;	)

dist: distclean
	$(RM) -r $(DIST_NAME)
	mkdir $(DIST_NAME)
	cp -r $(DIST_FILES) $(DIST_NAME)
	tar jcf $(DIST_NAME).tar.bz2 $(DIST_NAME)
	$(RM) -r $(DIST_NAME)
