
CFLAGS ?= -fPIC
export CFLAGS

SUBDIRS = tests

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

distcheck: distclean all distclean
	python setup.py sdist
