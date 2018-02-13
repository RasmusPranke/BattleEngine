#include <iostream>

#include <GL/glew.h>
#include <glfw3.h>
#include <glm\glm.hpp>

#include "Engine.h"

const int pre_allocate = 1000;

struct RenderObject
{
    bool show = false;
    long vertexCount;
    long * model;
    glm::mat4 scale;
    glm::mat4 rotation;
    glm::mat4 translation;
};

int render(EngineInterface * interface)
{
    std::cout << "Launching Engine! \n";
    RenderObject objects[pre_allocate];
    int msgId;
    do {
       msgId = interface->loadMessage();
       std::cout << "Message is: " << msgId << "\n";
       switch (msgId) {
       case 1:
       {
           int oid = interface->getId();
           if (oid > pre_allocate) {
               throw "OId too large!";
           }
           std::cout << "Found an OID: " << oid << "\n";
           break;
       }
       case 2:
           ShowArguments args = interface->getShow();
           objects[args.oid].show = args.show;
           std::cout << "Should I show: " << args.oid << "? " << args.show << "\n";
           break;
       default:
           break;
       }
    } while (msgId);
    std::cout << "Terminating Engine!";
    return 0;
}