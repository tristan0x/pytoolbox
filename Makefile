PYTHON ?= python

PYMAJORMINOR = $(shell python -c \
  "import sys; v = sys.version_info ; print '%i.%i' % (v[0], v[1])")

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
	tmp=`mktemp -d` && \
	python setup.py install --prefix $$tmp && \
	PYTHONPATH=$$tmp/lib/python$(PYMAJORMINOR)/site-packages \
	  $(MAKE) test && \
	python setup.py sdist

pydoc:
	rm -rf html
	mkdir html
	cd html && PYTHONPATH=.. pydoc -w pytoolbox pytoolbox.multi_imp
