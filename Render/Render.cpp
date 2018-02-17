#include <Python.h>
#include <iostream>
#include <glm\glm.hpp>

#include "Utility.h"
#include "Engine.h"
#include "engine_interface.h"

/////////////////////////////////////////
//Implementation of the Engine Interface.
/////////////////////////////////////////

class EngineInterfaceImpl : public EngineInterface {
public:
    int loadMessage();
    void sendInt(int id);
    int getId();
    ShowArguments getVisible();
    VertexArray getModel();
    IdIdTuple getIdTuple();
    IdVectorTuple getVector();
    IdRotationTuple getRotation();
    IdArrayTuple getIdArray();
    EngineInterfaceImpl(PyObject * givenPyInterface);
    ~EngineInterfaceImpl();
private:
    PyObject * messageInterface;
    PyObject * getMessage();
    VertexArray extractArray(PyObject * list);
};

int EngineInterfaceImpl::loadMessage()
{
    PyObject * messageId = PyObject_CallMethod(messageInterface, "loadMessage", "");
    //PyErr_Print();
    return PyLong_AsLong(messageId);
}

void EngineInterfaceImpl::sendInt(int id)
{
    PyObject * idO = PyLong_FromLong(id);
    PyObject_CallMethod(messageInterface, "sendMessage", "O", idO);
}
int EngineInterfaceImpl::getId() {
    PyObject * msg = getMessage();
    return PyLong_AsLong(msg);
}
ShowArguments EngineInterfaceImpl::getVisible()
{
    ShowArguments args;

    PyObject * msg = getMessage();
    PyArg_ParseTuple(msg, "ip", &args.id, &args.show);

    return args;
}
VertexArray EngineInterfaceImpl::getModel() {
    PyObject * msg = getMessage();
    return extractArray(msg);
}
IdIdTuple EngineInterfaceImpl::getIdTuple()
{
    IdIdTuple tuple;

    PyObject * msg = getMessage();
    PyArg_ParseTuple(msg, "ii", &tuple.id, &tuple.id2);

    return tuple;
}
IdVectorTuple EngineInterfaceImpl::getVector()
{
    IdVectorTuple tuple;
    PyObject * coordinateTuple;
    float x, y, z;

    PyObject * msg = getMessage();
    PyArg_ParseTuple(msg, "iO", &tuple.id, &coordinateTuple);
    PyArg_ParseTuple(coordinateTuple, "fff", &x, &y, &z);

    tuple.change = glm::vec3(x, y, z);

    return tuple;
}
IdRotationTuple EngineInterfaceImpl::getRotation()
{
    IdRotationTuple tuple;
    PyObject * coordinateTuple;
    float x, y, z;

    PyObject * msg = getMessage();
    PyArg_ParseTuple(msg, "iOf", &tuple.id, &coordinateTuple, &tuple.rotation_in_2pi);
    PyArg_ParseTuple(coordinateTuple, "fff", &x, &y, &z);

    tuple.axis = glm::vec3(x, y, z);

    return tuple;
}
IdArrayTuple EngineInterfaceImpl::getIdArray() {
    PyObject * msg = getMessage();
    PyObject * list;
    IdArrayTuple ret;

    PyArg_ParseTuple(msg, "iO", &ret.id, &list);
    ret.arr = extractArray(list);

    return ret;
}

VertexArray EngineInterfaceImpl::extractArray(PyObject * list) {
    VertexArray ret;
    Py_ssize_t max_offset = PyList_Size(list);
    int int_size = PyLong_AsLong(PyLong_FromSsize_t(max_offset));

    float * vertices = (float*)malloc(sizeof(vertices) * int_size);

    for (int i = 0; i < int_size; i++) {
        ssize_t itemPos = i;
        PyObject * item = PyList_GetItem(list, itemPos);
        vertices[i] = PyFloat_AsDouble(item);
        std::cout << vertices[i] << " ";
    }
    std::cout << "\n";

    ret.length = int_size;
    ret.vertex_list = vertices;
    return ret;
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


