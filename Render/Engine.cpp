#include <iostream>
#include <cmath>

#include <glew.h>
#include <glfw3.h>
#include <glm\glm.hpp>
#include <glm\gtc\matrix_transform.hpp>

#include "Utility.h"
#include "Engine.h"
#include "engine_interface.h"
#include "shader_loader.h"

/*
constexpr int pow(int a, int b) {
    int result = 1;
    for (int i = 0; i < b; i++) {
        result *= a;
    }
    return result;
}
*/

//const int PRE_ALLOCATE_OBJECTS_BITS = 10;
constexpr int PRE_ALLOCATE_OBJECTS = 1024; //pow(2, PRE_ALLOCATE_OBJECTS_BITS);

//const int PRE_ALLOCATE_MODELS_BITS = 10;
constexpr int PRE_ALLOCATE_MODELS = 128; //pow(2, PRE_ALLOCATE_OBJECTS_BITS);

//const int PRE_ALLOCATE_TEXTURES_BITS = 10;
constexpr int PRE_ALLOCATE_TEXTURES = 32; //pow(2, PRE_ALLOCATE_OBJECTS_BITS);

/*
Keeps track which Ids are available (NOT which are used).
Initialize this with an array containing all allowed Ids, setting the size to the size of that list and not touching the offset.
fetch_id will then always return an unused Id, while return_id will mark that id as usable.
*/
struct IdStack 
{
    unsigned int offset;
    unsigned int max_offset; 
    int * id_list;
};

IdStack create_id_stack(int size) {
    PRINT "Creating stack of size: " << size << "\n";
    IdStack stack;
    int max_offset = size - 1;
    PRINT "Max offset: " << max_offset << "\n";
    stack.max_offset = max_offset;
    stack.offset = 0;

    int * ids = (int*)malloc(size * sizeof(ids));
    for (int i = 0; i < size; i++) {
        ids[i] = i;
    }
    stack.id_list = ids;

    return stack;
}

int fetch_id(IdStack * stack) {
    PRINT "Stack max offset: " << stack->max_offset << "\n";
    if (stack->offset > stack->max_offset) {
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
    int texture = 0;
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

    IdStack texture_ids = create_id_stack(PRE_ALLOCATE_TEXTURES);
    int texture_count = PRE_ALLOCATE_TEXTURES;
    GLuint textures[PRE_ALLOCATE_TEXTURES];
};

int create_texture(Model * model, VertexArray texture) {
    if (texture.length != model->vertex_count) {
        PRINT "Texture point count does not match model size!\n";
        return -1;
    }

    int id = fetch_id(&model->texture_ids);
    glGenBuffers(1, &model->textures[id]);
    glBindBuffer(GL_ARRAY_BUFFER, model->textures[id]);
    glBufferData(GL_ARRAY_BUFFER, texture.length * sizeof(texture.vertex_list), texture.vertex_list, GL_STATIC_DRAW);
    return id;
}

Model create_model(int vertex_count, GLfloat * vertex_data) {
    std::cout << "\n";

    Model model = Model();
    glGenBuffers(1, &model.vertex_buffer);
    glBindBuffer(GL_ARRAY_BUFFER, model.vertex_buffer);
    glBufferData(GL_ARRAY_BUFFER, vertex_count * sizeof(vertex_data), vertex_data, GL_STATIC_DRAW);
    model.vertex_count = vertex_count;

    GLfloat * default_texture_data = (GLfloat*)malloc(vertex_count * sizeof(default_texture_data));
    for (int i = 0; i < vertex_count; i++) {
        default_texture_data[i] = 1;
    }
    VertexArray texture;
    texture.length = vertex_count;
    texture.vertex_list = default_texture_data;
    create_texture(&model, texture);
    free(default_texture_data);

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

void show_object(RenderObject object, Model * models, Shader shader, Camera camera) {
    Model model = models[object.model];

    //Calculate the MVP matrix
    glm::mat4 mvp = camera.projection_matrix * camera.view_matrix * object.model_matrix;

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

    glEnableVertexAttribArray(1);
    glBindBuffer(GL_ARRAY_BUFFER, model.textures[object.texture]);
    glVertexAttribPointer(
        1,                                // attribute. No particular reason for 1, but must match the layout in the shader.
        3,                                // size
        GL_FLOAT,                         // type
        GL_FALSE,                         // normalized?
        0,                                // stride
        (void*)0                          // array buffer offset
    );

    // Draw the triangle !
    glDrawArrays(GL_TRIANGLES, 0, model.vertex_count);

    glDisableVertexAttribArray(0);
    glDisableVertexAttribArray(1);
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
    RenderObject objects[PRE_ALLOCATE_OBJECTS];
    IdStack object_id_stack = create_id_stack(PRE_ALLOCATE_OBJECTS);

    //Initialize the Model list and its Id stack.
    PRINT "Allocating: " << PRE_ALLOCATE_OBJECTS << "\n";
    Model models[PRE_ALLOCATE_OBJECTS];
    IdStack model_id_stack = create_id_stack(PRE_ALLOCATE_OBJECTS);

    //Load shader
    Shader shader = load_shader("SimpleVertexShader.vertexshader", "SimpleFragmentShader.fragmentshader");

    //Initialize default camera.
    //TODO: UI camera
    Camera cams[PRE_ALLOCATE_OBJECTS];
    cams[0].projection_matrix = glm::perspective(glm::radians(45.0f), (float) 4.0f / (float)3.0f, 0.1f, 1000.0f);
    cams[0].view_matrix = glm::lookAt(
        glm::vec3(0, 0, 3), // Camera is at (4,3,3), in World Space
        glm::vec3(0, 0, 0), // and looks at the origin
        glm::vec3(0, 1, 0)  // Head is up (set to 0,-1,0 to look upside-down)
    );

    int msg_id;
    do {

        // Clear the screen
        glClear(GL_COLOR_BUFFER_BIT);

        for (int i = 0; i < PRE_ALLOCATE_OBJECTS; i++) {
            if (objects[i].show) {
                show_object(objects[i], models, shader, cams[0]);
            }
        }

        // Swap buffers
        glfwSwapBuffers(window);
        glfwPollEvents();

        do {
            msg_id = interface->loadMessage();
            //PRINT "Message is: " << msg_id << "\n";
            switch (msg_id) {
            case 1: //Assign OId
            {
                int object_id = fetch_id(&object_id_stack);
                PRINT "Assigning an OID: " << object_id << "\n";
                interface->sendInt(object_id);
                break;
            }
            case 2: //Set Object invisible and set the OId as available (i.e. "destroy" the object)
            {
                int object_id = interface->getId();
                PRINT "Freeing oid: " << object_id << "\n";
                objects[object_id].show = false;
                return_id(&object_id_stack, object_id);
                break;
            }
            case 3: //Set Object Visible/Invisible
            {
                ShowArguments args = interface->getVisible();
                PRINT "Should I show: " << args.id << "? " << args.show << "\n";
                //Check if object is showable.
                if (args.show && objects[args.id].model == -1) {
                    PRINT "To show an Object, it must have a model!\n";
                }
                else {
                    objects[args.id].show = args.show;
                }
                break;
            }
            case 4: //Assign a model to an object
            {
                IdIdTuple args = interface->getIdTuple();
                PRINT "Assigning Model " << args.mid << " to object " << args.id << "\n";
                objects[args.id].model = args.mid;
                break;
            }
            case 5: //Translate an Object
            {
                IdVectorTuple movement = interface->getVector();
                PRINT "Translating " << movement.id << " by " << movement.change.x << " " << movement.change.y << " " << movement.change.z << " " << "!\n";
                objects[movement.id].model_matrix = glm::translate(objects[movement.id].model_matrix, movement.change);
                break;
            }
            case 6: //Rotate an Object
            {
                IdRotationTuple rotation = interface->getRotation();
                PRINT "Rotating " << rotation.id << " around " << rotation.axis.x << " " << rotation.axis.y << " " << rotation.axis.z << " by " << rotation.rotation_in_2pi << "!\n";
                objects[rotation.id].model_matrix = glm::rotate(objects[rotation.id].model_matrix, rotation.rotation_in_2pi, rotation.axis);
                break;
            }
            case 7: //Scale an Object
            {
                IdVectorTuple scaling = interface->getVector();
                PRINT "Scaling " << scaling.id << " by " << scaling.change.x << " " << scaling.change.y << " " << scaling.change.z << " " << "!\n";
                objects[scaling.id].model_matrix = glm::scale(objects[scaling.id].model_matrix, scaling.change);
                break;
            }
            case 11: //Load an Model as an Array
            {
                PRINT "Loading Model!\n";
                int model_id = fetch_id(&model_id_stack);
                PRINT "Fetched id!\n";
                VertexArray model_vertices = interface->getModel();
                models[model_id] = create_model(model_vertices.length, model_vertices.vertex_list);
                interface->sendInt(model_id);
                free(model_vertices.vertex_list);
                break;
            }
            case 25: //Translate an Camera
            {
                IdVectorTuple movement = interface->getVector();
                PRINT "Translating Camera " << movement.id << " by " << movement.change.x << " " << movement.change.y << " " << movement.change.z << " " << "!\n";
                cams[movement.id].view_matrix = glm::translate(cams[movement.id].view_matrix, movement.change);
                break;
            }
            case 26: //Rotate an Camera
            {
                IdRotationTuple rotation = interface->getRotation();
                PRINT "Rotating Camera " << rotation.id << " around " << rotation.axis.x << " " << rotation.axis.y << " " << rotation.axis.z << " by " << rotation.rotation_in_2pi << "!\n";
                cams[rotation.id].view_matrix = glm::rotate(cams[rotation.id].view_matrix, -rotation.rotation_in_2pi, rotation.axis);
                break;
            }
            case 31: //Load an Texture as an Array
            {
                PRINT "Loading Texture!\n";
                IdArrayTuple source = interface->getIdArray();
                VertexArray arr = source.arr;
                Model model = models[source.id];
                interface->sendInt(create_texture(&model, arr));
                break;
            }
            case 0:
                PRINT "Recieved shutdown signal!\n";
                break;
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