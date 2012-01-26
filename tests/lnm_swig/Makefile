PYTHON ?= python
SWIG ?= swig

CFLAGS += -fPIC
export CFLAGS

PYTHONPATH := $(PYTHONPATH):$(shell pwd)/../..
export PYTHONPATH

SWIG_INTERFACE = native_module.i
SWIG_GENERATED_CODE = $(SWIG_INTERFACE:.i=.py) $(SWIG_INTERFACE:.i=_wrap.c)
SHARED_LIBRARY_NAME = _$(SWIG_INTERFACE:.i=.so)
SHARED_LIBRARY_OBJECTS = $(SWIG_INTERFACE:.i=_wrap.o)

CPPFLAGS += -I$(shell $(PYTHON) -c "import distutils.sysconfig as s; print s.get_python_inc()")

all: $(SHARED_LIBRARY_NAME)

$(SHARED_LIBRARY_NAME): $(SHARED_LIBRARY_OBJECTS)
	$(LD) -shared $(SHARED_LIBRARY_OBJECTS) -o $@

$(SWIG_GENERATED_CODE): ${SWIG_INTERFACE}
	$(SWIG) -python ${SWIG_INTERFACE}

.cc.o:
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

clean:
	$(RM) $(SWIG_GENERATED_CODE)		\
	      $(SWIG_INTERFACE:.i=_wrap.o)

distclean: clean
	$(RM) $(SHARED_LIBRARY_NAME) *.pyc

test: all
	$(PYTHON) test.py
