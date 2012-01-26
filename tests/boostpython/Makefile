
PYTHON ?= python

CPPFLAGS += -DBOOST_PYTHON_DYNAMIC_LIB
CPPFLAGS += -I$(shell $(PYTHON) -c "import distutils.sysconfig as s; print s.get_python_inc()")

ifdef BOOST_INCLUDE_PATH
CPPFLAGS += -I$(BOOST_INCLUDE_PATH)
endif

ifdef BOOST_LIBRARY_PATH
LDFLAGS += -Wl,-rpath=$(BOOST_LIBRARY_PATH) \
	   -L$(BOOST_LIBRARY_PATH)
endif BOOST_LIBRARY_PATH

TARGET=_hello.so

all: $(TARGET)


$(TARGET): hello.o
	$(CC) -o $@ -shared $(LDFLAGS)  -lboost_python $<

.cc.o:
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $< -o $@


clean:
	$(RM) hello.o *.pyc

distclean: clean
	$(RM) $(TARGET)

test:
	$(PYTHON) test.py
