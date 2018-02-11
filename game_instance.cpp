//This file is responsible for interfacing between the rendering and the game instance.
//As such, it has full responsibility for the python embedding as well as shipping instructions between the renderer and the game instance.

#include <Python.h>
#include <string.h>
#include <utility>

class Game
{
public:
    Game();
    ~Game();
    int load_instruction();
    long get_instruction_args(long (*parser)(PyObject* obj));

private:
    PyObject * load_message;
    PyObject * get_message;
    PyObject * launcher;

};

Game::Game()
{
    //Initialize the interpreter and import the Launch module.
    //Importing the module imediately runs all necessary code for launching the python side of the game.
    //Additionally, fetch the PyObjects used to retrieve messages from the game.
    Py_Initialize();
    /*const char * argv[1];
    argv[0] = "Launch";
    PySys_SetArgv(0, argv);*/
    PyObject *game_module = PyImport_ImportModule("Launch");
    if (game_module == NULL) {
        PyErr_Print();
        throw "Could not load Module \"Launch\"!";
    }
    else {
        launcher = game_module;
        PyObject * launchFunction = PyObject_GetAttr(launcher, Py_BuildValue("s", "launch"));
        PyObject * getMessageObject = PyObject_GetAttr(launcher, Py_BuildValue("s", "getMessage"));
        PyObject * loadMessageObject = PyObject_GetAttr(launcher, Py_BuildValue("s", "loadMessage"));
        if (loadMessageObject == NULL || getMessageObject == NULL) {
            throw "Could not load hasMessage or getMessage!";
        }
        else {
            load_message = loadMessageObject;
            get_message = getMessageObject;
            PyObject_Call(launchFunction, PyTuple_New(0), NULL);
        }
    }
}

Game::~Game()
{
    PyObject * shutdown_function = PyObject_GetAttr(launcher, Py_BuildValue("s", "exit"));
    PyObject_Call(shutdown_function, PyTuple_New(0), NULL);
    Py_DECREF(load_message);
    Py_DECREF(get_message);
    Py_DECREF(launcher);
    Py_Finalize();
}

/**
  Checks whether an instruction is currently waiting in queue.
  If there is, this returns its instruction ID, otherwise this returns 0.
  Additionally, the arguments are loaded to be gotten by get_instruction_args().
*/
int Game::load_instruction() {
    PyObject * instruction = PyObject_Call(load_message, PyTuple_New(0), NULL);
    PyObject * err = PyErr_Occurred();
    if (NULL != err) {
        PyObject * str = PyObject_GetAttr(err, Py_BuildValue("s", "__str__"));
        PyErr_Print();
        PyObject * res = PyObject_Call(str, PyTuple_New(0), NULL);
    }
    long messageId = PyLong_AsLong(instruction); 
    return messageId;
}

/**
Takes a parser and runs the PyObject message through said parser to return a c-readable form of the message.
This means that the caller itself doesn't need to know anything about Python whatsoever and merely needs some funtion that parses Python to retrieve messages.
*/
//template <typename return_type>
//return_type Game::get_instruction_args(return_type(*parser)(PyObject* obj))
long Game::get_instruction_args(long (*parser)(PyObject* obj))
{
    PyObject * pyArgs = PyObject_Call(get_message, PyTuple_New(0), NULL);
    return (*parser)(pyArgs);
}
