#include <Python.h>
#include <iostream>
#include "Engine.h"

/////////////////////////////////////////
//Implementation of the Engine Interface.
/////////////////////////////////////////

class EngineInterfaceImpl : public EngineInterface {
public:
    int loadMessage();
    int getId();
    ShowArguments getVisible();
    EngineInterfaceImpl(PyObject * givenPyInterface);
    ~EngineInterfaceImpl();
private:
    PyObject * messageInterface;
    PyObject * getMessage();
};

int EngineInterfaceImpl::loadMessage()
{
    PyObject * messageId = PyObject_CallMethod(messageInterface, "loadMessage", "");
    PyErr_Print();
    return PyLong_AsLong(messageId);
}

int EngineInterfaceImpl::getId()
{
    PyObject * msg = getMessage();
    return PyLong_AsLong(msg);
}
ShowArguments EngineInterfaceImpl::getVisible()
{
    ShowArguments args;
    PyObject * msg = getMessage();
    PyArg_ParseTuple(msg, "ip", &args.oid, &args.show);
    return args;
}
EngineInterfaceImpl::EngineInterfaceImpl(PyObject * pyInterface)
{
    messageInterface = pyInterface;
}
EngineInterfaceImpl::~EngineInterfaceImpl()
{
    Py_DECREF(messageInterface);
}
PyObject * EngineInterfaceImpl::getMessage()
{
    return PyObject_CallMethod(messageInterface, "getMessage", "");
}

/////////////////////////////////////////
//Python library Implementation.
/////////////////////////////////////////
PyDoc_STRVAR(Render_example_doc, "start(interface)\n\
Kicks off the Rendering using the interface to load instructions and get instruction arguments.\n\
The interface must provide a loadMessage, a getMessage and a sendMessage method.");//TODO: Better documentation of what interface must look like.

PyObject *start(PyObject *self, PyObject *args) {
    /* Shared references that do not need Py_DECREF before returning. */
    PyObject *messageInterface = NULL;

    /* Parse positional and keyword arguments */
    //Extract from args an Object and put it at callable.
    if (!PyArg_ParseTuple(args, "O", &messageInterface)) {
        return NULL;
    }

    /*Instantiate the interface implementation with the recieved loader and getter.*/
    EngineInterface * interface = new EngineInterfaceImpl(messageInterface);
    render(interface);

    Py_RETURN_NONE;
}

/*
 * List of functions to add to Render in exec_Render().
 */
static PyMethodDef Render_functions[] = {
    { "start", (PyCFunction)start, METH_VARARGS, Render_example_doc },
    { NULL, NULL, 0, NULL } /* marks end of array */
};

static PyModuleDef Render_module = {
    PyModuleDef_HEAD_INIT,
    "Render",                        // Module name to use with Python import statements
    "An Rendering Engine written in CPP, used via Python.",  // Module description
    0,
    Render_functions // Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_Render() {
    return PyModule_Create(&Render_module);
}


