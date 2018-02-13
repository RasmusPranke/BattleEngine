#include <Python.h>
#include <string>

long parse_number(PyObject * message) {
    return PyLong_AsLong(message);
}

bool parse_bool(PyObject* message) {
    long result = PyLong_AsLong(message);
    return result;
}