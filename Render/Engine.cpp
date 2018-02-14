#include <iostream>

#include <glew.h>
#include <glfw3.h>
#include <glm\glm.hpp>

#include "Engine.h"
#include "shader_loader.h"

const int PRE_ALLOCATE = 1000;

struct RenderObject
{
    bool show = false;
    int model;
    glm::mat4 scale;
    glm::mat4 rotation;
    glm::mat4 translation;
};

struct Model
{
    GLuint vertex_buffer;
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

    std::cout << "Creating VAO!\n";
    GLuint vertexArrayId;
    glGenVertexArrays(1, &vertexArrayId);
    glBindVertexArray(vertexArrayId);
    std::cout << "Successfully created VAO!\n";

    return window;
}

Model createModel(int vertex_count, GLfloat * vertex_data) {
    Model model = Model();
    glGenBuffers(1, &model.vertex_buffer);
    glBindBuffer(GL_ARRAY_BUFFER, model.vertex_buffer);
    glBufferData(GL_ARRAY_BUFFER, vertex_count, vertex_data, GL_STATIC_DRAW);
    return model;
}

void showModel(Model model) {
    // 1rst attribute buffer : vertices
    glEnableVertexAttribArray(0);
    glBindBuffer(GL_ARRAY_BUFFER, model.vertex_buffer);
    glVertexAttribPointer(
        0,                  // attribute 0. No particular reason for 0, but must match the layout in the shader.
        3,                  // size
        GL_FLOAT,           // type
        GL_FALSE,           // normalized?
        0,                  // stride
        (void*)0            // array buffer offset
    );

    // Draw the triangle !
    glDrawArrays(GL_TRIANGLES, 0, 3); // 3 indices starting at 0 -> 1 triangle

    glDisableVertexAttribArray(0);
}

int render(EngineInterface * interface)
{
    std::cout << "Launching Engine! \n";
    GLFWwindow * window = init();
    
    //Enable key capturing.
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);

    // Dark blue background
    glClearColor(0.0f, 0.0f, 0.4f, 0.0f);

    RenderObject objects[PRE_ALLOCATE];
    Model models[PRE_ALLOCATE];

    GLfloat triangle_vertices_1[] = {
        -1.0f, -1.0f, 0.0f,
        -1.0f, 1.0f, 0.0f,
        0.0f,  0.5f, 0.0f,
    };
    models[0] = createModel(sizeof(triangle_vertices_1), triangle_vertices_1);
    GLfloat triangle_vertices_2[] = {
        1.0f, -1.0f, 0.0f,
        1.0f, 1.0f, 0.0f,
        0.0f,  0.0f, 0.0f,
    };
    models[1] = createModel(sizeof(triangle_vertices_2), triangle_vertices_2);

    //Load shader
    GLuint programID = LoadShaders("SimpleVertexShader.vertexshader", "SimpleFragmentShader.fragmentshader");

    int msgId;
    do {

        // Clear the screen
        glClear(GL_COLOR_BUFFER_BIT);

        // Use our shader
        glUseProgram(programID);

        for (int i = 0; i < 2; i++) {
            showModel(models[i]);
        }

        // Swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

        msgId = interface->loadMessage();
        std::cout << "Message is: " << msgId << "\n";
        switch (msgId) {
        case 1:
        {
            int oid = interface->getId();
            if (oid > PRE_ALLOCATE) {
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
    for (int i = 0; i < PRE_ALLOCATE; i++) {
        std::cout << objects[i].show;
    }
    std::cout << "Terminating Engine!";
    return 0;
}