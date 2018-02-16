#pragma once
/*
Communication takes the following form :
Each Object first accquires an ObjectId using Create (OpId 1).
 This ObjectId (OId) is returned via getId() and identifies the thing to modify to the rendering.
Then, to have something to render, a ModelId must be accquired by using CreateM (11).
 This MId is also returned via getId().
SetModel (4) attaches the Model identified by MId to the Object identified by OId.
Finally, passing Visible (3) with true enables rendering for the given object, but only if it has a valid model. 

Operations are encoded as follows :
(OpId, Argument)
OpId is the operation id, as described in the table below.
Argument is all information required by the renderer, encoded as a list of list of floating point values.

Operation  | OpId | Argument            | Comment
 RESERVED  |  -1  |                     | Reserved for Engine internals.Don't use this as a message ID.
 Stop      |   0  | None                | Tells the rendering engine to terminate.
 Create    |   1  | None                | Returns an unused ObjectId and marks it as used.
 Destroy   |   2  | OId                 | Frees the given OId to be reassigned later.
 Visible   |   3  | (OId, True / False) |
 SetModel  |   4  | (OId, MId)          | Assigns the given Model to the given Object. Multiple Objects may share a Model.
 Move      |   5  | (OId, Vector3)      | Translates the given Object by the given Vector.
 
 Model Operations
 CreateM   |  11  | [Model Points...]   | Takes a list of vertices and sends back the ID of the Model.
 CreateM   |  12  | FileName            | Loads a model from the given file and sends back the ID of that Model.
*/

struct ShowArguments {
    int oid;
    bool show;
};

struct VertexArray {
    int length;
    float * vertex_list;
};

struct IdIdTuple {
    int oid;
    int mid;
};

struct IdVectorTuple {
    int oid;
    glm::vec3 change;
};

class EngineInterface {
public:
    virtual int loadMessage() = 0;
    virtual void sendInt(int) = 0;
    virtual int getId() = 0;
    virtual ShowArguments getVisible() = 0;
    virtual VertexArray getModel() = 0;
    virtual IdIdTuple getIdTuple() = 0;
    virtual IdVectorTuple getMovement() = 0;
};