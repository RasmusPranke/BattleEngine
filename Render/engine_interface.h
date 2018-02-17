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

Operation  | OpId | Argument                 | Comment
 RESERVED  |  -1  |                          | Reserved for Engine internals.Don't use this as a message ID.
 Stop      |   0  | None                     | Tells the rendering engine to terminate.

 Create    |   1  | None                     | Returns an unused ObjectId and marks it as used.
 Destroy   |   2  | OId                      | Frees the given OId to be reassigned later.
 Visible   |   3  | (OId, True / False)      |

 SetModel  |   4  | (OId, MId)               | Assigns the given Model to the given Object. Multiple Objects may share a Model.
 SetTexture|   8  | (OId, TId)               | Assigns the given Texture to the given Object.

 Move      |   5  | (OId, Vector3)           | Translates the given Object by the given Vector.
 Rotate    |   6  | (OId,Vector3,radian)     | Rotates the Object radians around the axis given by the vector 
 Scale     |   7  | (OId, Vector3)           | Scales the Object by the given amount along each of the axis.
 
 Model Operations
 CreateM   |  11  | [Model Points...]        | Takes a list of vertices and sends back the ID of the Model.
 MISSING:
 CreateM   |  12  | FileName                 | Loads a model from the given file and sends back the ID of that Model.

 Texture Operations
 CreateT   |  31  |(MId, [Texture Points...])| Takes a list of colors for a model and sends back the ID of the Texture.
 MISSING:
 CreateM   |  32  | FileName                 | Loads a model from the given file and sends back the ID of that Model.

 Camera Operations
 MoveCam   |   25  | (CId, Vector3)      | Translates the given Camera by the given Vector.
 RotateCam |   26  | (CId,Vector3,radian)| Rotates the Camera radians around the axis given by the vector 
*/

struct ShowArguments {
    int id;
    bool show;
};

struct VertexArray {
    int length;
    float * vertex_list;
};

struct IdIdTuple {
    int id;
    int id2;
};

struct IdVectorTuple {
    int id;
    glm::vec3 change;
};

struct IdRotationTuple {
    int id;
    glm::vec3 axis;
    float rotation_in_2pi;
};

struct IdArrayTuple{
    int id;
    VertexArray arr;
};

class EngineInterface {
public:
    virtual int loadMessage() = 0;
    virtual void sendInt(int) = 0;
    virtual int getId() = 0;
    virtual ShowArguments getVisible() = 0;
    virtual VertexArray getModel() = 0;
    virtual IdIdTuple getIdTuple() = 0;
    virtual IdVectorTuple getVector() = 0;
    virtual IdRotationTuple getRotation() = 0;
    virtual IdArrayTuple getIdArray() = 0;
};