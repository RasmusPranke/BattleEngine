#pragma once
#include<Python.h>

struct ShowArguments {
    int oid;
    bool show;
};

class EngineInterface {
public:
    virtual int loadMessage() = 0;
    virtual void sendInt(int) = 0;
    virtual int getId() = 0;
    virtual ShowArguments getVisible() = 0;
};

int render(EngineInterface * interface);
