
PYTHON ?= python
BOOST_INCLUDE_PATH = /data.2/tcarel/root/stow/boost.1.48.0/include
BOOST_LIBRARY_PATH = /data.2/tcarel/root/stow/boost.1.48.0/lib
PYTHON_INCLUDE_PATH = -I$(shell $(PYTHON) -c "import distutils.sysconfig as s; print s.get_python_inc()")

TARGET=_hello.so

all: $(TARGET)


$(TARGET): hello.o
	gcc -o $@ -shared -Wl,-rpath=$(BOOST_LIBRARY_PATH) -L$(BOOST_LIBRARY_PATH) -lboost_python $<

.cc.o:
	gcc -c -fpic -DBOOST_PYTHON_DYNAMIC_LIB -I $(BOOST_INCLUDE_PATH) $(PYTHON_INCLUDE_PATH) $< -o $@


clean:
	$(RM) hello.o *.pyc

distclean: clean
	$(RM) $(TARGET)

test:
	$(PYTHON) test.py