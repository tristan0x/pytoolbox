
PYTHON ?= python
PYTHONPATH := $(PYTHONPATH):$(shell pwd)/../..
export PYTHONPATH

CPPFLAGS += -DBOOST_PYTHON_DYNAMIC_LIB -fPIC
CPPFLAGS += -I$(shell $(PYTHON) -c "import distutils.sysconfig as s; print s.get_python_inc()")

ifdef BOOST_INCLUDE_PATH
CPPFLAGS += -I$(BOOST_INCLUDE_PATH)
endif

ifdef BOOST_LIBRARY_PATH
LDFLAGS += -Wl,-rpath=$(BOOST_LIBRARY_PATH) \
	   -L$(BOOST_LIBRARY_PATH)
endif

TARGET=hello.so

all: $(TARGET)


$(TARGET): hello.o
	$(CC) -o $@ -shared $(LDFLAGS)  -lboost_python $<

.cc.o:
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@


clean:
	$(RM) hello.o *.pyc

distclean: clean
	$(RM) $(TARGET)

test: all
	$(PYTHON) test.py

poeut:
	@echo $(PYTHONPATH)
