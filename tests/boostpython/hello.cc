
#include <string>
#include <sstream>

#include <boost/python.hpp>
#include <boost/lambda/lambda.hpp>

static int value = 0;

int getvalue() {
  return value;
}

void incrvalue()
{
  ++value;
}

BOOST_PYTHON_MODULE(_hello)
{
  boost::python::def("incrvalue", incrvalue);
  boost::python::def("value", getvalue);
}
