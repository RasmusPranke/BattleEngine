#include <iostream>

#include <glew.h>
#include <glfw3.h>
#include <glm\glm.hpp>
#include <glm\gtc\matrix_transform.hpp>

#include "Utility.h"
#include "Engine.h"
#include "engine_interface.h"
#include "shader_loader.h"

const int PRE_ALLOCATE = 1000;

/*
Keeps track which Ids are available (NOT which are used).
Initialize this with an array containing all allowed Ids, setting the size to the size of that list and not touching the offset.
fetch_id will then always return an unused Id, while return_id will mark that id as usable.
*/
struct IdStack 
{
    int offset = 0;
    int size = 0;
    int * id_list;
};

int fetch_id(IdStack * stack) {
    if (stack->offset >= stack->size) {
        throw "Can't fetch id, idStack is empty!\n";
    }
    int ret = stack->id_list[stack->offset];
    ++stack->offset;
    return ret;
}

void return_id(IdStack * stack, int id) {
    if (stack->offset <= 0) {
        throw "Can't return id, idStack is full!\n";
    }
    --stack->offset;
    stack->id_list[stack->offset] = id;
}

struct Shader {
    GLuint program_id;
    GLuint mvp_handle;
};

Shader load_shader(const char* vertex_shader_file, const char* fragment_shader_file) {
    Shader shader;
    shader.program_id = LoadShaders(vertex_shader_file, fragment_shader_file);
    shader.mvp_handle = glGetUniformLocation(shader.program_id, "MVP");
    return shader;
}

struct RenderObject
{
    bool show = false;
    int model = -1;
    glm::mat4 model_matrix = glm::mat4(1.0f);
};

struct Camera {
    glm::mat4 view_matrix;
    glm::mat4 projection_matrix;
};

struct Model
{
    int vertex_count;
    GLuint vertex_buffer;
};

Model create_model(int vertex_count, GLfloat * vertex_data) {
    PRINT "Creating Model!\n";
    PRINT "Size: " << vertex_count << "\n";
    PRINT "Data: ";
    for (int i = 0; i < vertex_count; i++) {
        std::cout << vertex_data[i] << " ";
    }
    std::cout << "\n";

    Model model = Model();
    glGenBuffers(1, &model.vertex_buffer);
    glBindBuffer(GL_ARRAY_BUFFER, model.vertex_buffer);
    glBufferData(GL_ARRAY_BUFFER, vertex_count * sizeof(vertex_data), vertex_data, GL_STATIC_DRAW);
    model.vertex_count = vertex_count;
    return model;
}

GLFWwindow * init() {
    PRINT "Initializing Engine! \n";
    PRINT "Initializing GLFW! \n";
    if (!glfwInit())
    {
        PRINT "Failed to initialize GLFW\n";
        getchar();
        return NULL;
    }
    glfwWindowHint(GLFW_SAMPLES, 4);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy; should not be needed
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    PRINT "Successfully initialized GLFW! \n";

    PRINT "Initializing Window!\n";
    GLFWwindow * window;

    window = glfwCreateWindow(1024, 768, "Playground", NULL, NULL);
    if (window == NULL) {
        PRINT "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible. Try the 2.1 version of the tutorials.\n";
        getchar();
        glfwTerminate();
        return NULL;
    }
    glfwMakeContextCurrent(window);
    PRINT "Successfully initialized Window!\n";


    PRINT "Initializing GLEW!\n";
    if (glewInit() != GLEW_OK) {
        PRINT "Failed to initialize GLEW\n";
        getchar();
        glfwTerminate();
        return NULL;
    }
    PRINT "Successfully initialized GLEW!\n";

    PRINT "Creating VAO!\n";
    GLuint vertexArrayId;
    glGenVertexArrays(1, &vertexArrayId);
    glBindVertexArray(vertexArrayId);
    PRINT "Successfully created VAO!\n";

    return window;
}

void show_model(Model model, glm::mat4 model_matrix, Shader shader, Camera camera) {
    //Calculate the MVP matrix
    glm::mat4 mvp = camera.projection_matrix * camera.view_matrix * model_matrix;

    // 1rst attribute buffer : vertices

        // Use our shader
    glUseProgram(shader.program_id);
    glUniformMatrix4fv(shader.mvp_handle, 1, GL_FALSE, &mvp[0][0]);
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
    glDrawArrays(GL_TRIANGLES, 0, model.vertex_count); // 3 indices starting at 0 -> 1 triangle

    glDisableVertexAttribArray(0);
}

int render(EngineInterface * interface)
{
    PRINT "Launching Engine! \n";
    GLFWwindow * window = init();
    
    //Enable key capturing.
    glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);

    // Dark blue background
    glClearColor(0.0f, 0.0f, 0.4f, 0.0f);

    //Initialize the Object list and its Id stack.
    RenderObject objects[PRE_ALLOCATE];
    IdStack object_id_stack;
    int oids[PRE_ALLOCATE];
    for (int i = 0; i < PRE_ALLOCATE; i++) {
        oids[i] = i;
    }
    object_id_stack.size = sizeof(oids);
    object_id_stack.id_list = &(*oids);

    //Initialize the Model list and its Id stack.
    Model models[PRE_ALLOCATE];
    IdStack model_id_stack;
    int mids[PRE_ALLOCATE];
    for (int i = 0; i < PRE_ALLOCATE; i++) {
        mids[i] = i;
    }
    model_id_stack.size = sizeof(mids);
    model_id_stack.id_list = &(*mids);

    //Load shader
    Shader shader = load_shader("SimpleVertexShader.vertexshader", "SimpleFragmentShader.fragmentshader");

    //Initialize default camera.
    //TODO: UI camera
    Camera cam;
    cam.projection_matrix = glm::perspective(glm::radians(45.0f), (float) 4.0f / (float)3.0f, 0.1f, 100.0f);
    cam.view_matrix = glm::lookAt(
        glm::vec3(4, 3, 3), // Camera is at (4,3,3), in World Space
        glm::vec3(0, 0, 0), // and looks at the origin
        glm::vec3(0, 1, 0)  // Head is up (set to 0,-1,0 to look upside-down)
    );

    int msg_id;
    do {

        // Clear the screen
        glClear(GL_COLOR_BUFFER_BIT);

        for (int i = 0; i < PRE_ALLOCATE; i++) {
            if (objects[i].show) {
                PRINT "Rendering: " << i << "\n";
                show_model(models[objects[i].model], objects[i].model_matrix, shader, cam);
            }
        }

        // Swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

        do {
            msg_id = interface->loadMessage();
            //PRINT "Message is: " << msg_id << "\n";
            switch (msg_id) {
            case 1:
            {
                int oid = fetch_id(&object_id_stack);
                PRINT "Assigning an OID: " << oid << "\n";
                interface->sendInt(oid);
                break;
            }
            case 2:
            {
                int oid = interface->getId();
                PRINT "Freeing oid: " << oid << "\n";
                objects[oid].show = false;
                return_id(&object_id_stack, oid);
                break;
            }
            case 3:
            {
                ShowArguments args = interface->getVisible();
                PRINT "Should I show: " << args.oid << "? " << args.show << "\n";
                //Check if object is showable.
                if (args.show && objects[args.oid].model == -1) {
                    PRINT "To show an Object, it must have a model!\n";
                }
                else {
                    objects[args.oid].show = args.show;
                }
                break;
            }
            case 4:
            {
                IdIdTuple args = interface->getIdTuple();
                PRINT "Assigning Model " << args.mid << " to object " << args.oid << "\n";
                objects[args.oid].model = args.mid;
                break;
            }
            case 5:
            {
                IdVectorTuple movement = interface->getMovement();
                PRINT "Translating " << movement.oid << " by " << movement.change.x << " " << movement.change.y << " " << movement.change.z << " " << "!\n";
                objects[movement.oid].model_matrix = glm::translate(objects[movement.oid].model_matrix, movement.change);
                break;
            }
            case 11:
            {
                PRINT "Loading Model!\n";
                int model_id = fetch_id(&model_id_stack);
                VertexArray model_vertices = interface->getModel();
                models[model_id] = create_model(model_vertices.length, model_vertices.vertex_list);
                interface->sendInt(model_id);
                break;
            }
            case -2:
                break;
            default:
                PRINT "Unknown message!\n";
                break;
            }
        } while (msg_id != -2 && msg_id); //Stop reading if either no messages remain or the msg is to stop (Id 0).
    } while (msg_id);
    PRINT "Terminating Engine!";
    return 0;
}