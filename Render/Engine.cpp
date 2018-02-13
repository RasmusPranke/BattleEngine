#include <iostream>

#include <glew.h>
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

GLFWwindow * init() {
    std::cout << "Initializing Engine! \n";
    std::cout << "Initializing GLFW! \n";
    if (!glfwInit())
    {
        fprintf(stderr, "Failed to initialize GLFW\n");
        getchar();
        return NULL;
    }
    glfwWindowHint(GLFW_SAMPLES, 4);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy; should not be needed
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    std::cout << "Successfully initialized GLFW! \n";

    std::cout << "Initializing Window!\n";
    GLFWwindow * window;

    window = glfwCreateWindow(1024, 768, "Playground", NULL, NULL);
    if (window == NULL) {
        fprintf(stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n");
        getchar();
        glfwTerminate();
        return NULL;
    }
    glfwMakeContextCurrent(window);
    std::cout << "Successfully initialized Window!\n";
    
    
    std::cout << "Initializing GLEW!\n";
    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Failed to initialize GLEW\n");
        getchar();
        glfwTerminate();
        return NULL;
    }
    std::cout << "Successfully initialized GLEW!\n";
    
    return window;
}

int render(EngineInterface * interface)
{
    std::cout << "Launching Engine! \n";
    GLFWwindow * window = init();
    
    //Enable key capturing.
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);

    // Dark blue background
    glClearColor(0.0f, 0.0f, 0.4f, 0.0f);

    RenderObject objects[pre_allocate];
    int msgId;
    do {
        glClear(GL_COLOR_BUFFER_BIT);

        // Draw nothing, see you in tutorial 2 !

        // Swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

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
            ShowArguments args = interface->getVisible();
            objects[args.oid].show = args.show;
            std::cout << "Should I show: " << args.oid << "? " << args.show << "\n";
            break;
        default:
            break;
        }
    } while (msgId);
    for (int i = 0; i < pre_allocate; i++) {
        std::cout << objects[i].show;
    }
    std::cout << "Terminating Engine!";
    return 0;
}