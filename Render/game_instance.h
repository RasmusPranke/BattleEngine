#pragma once

class Game
{
public:
    Game();
    ~Game();
    int load_instruction();
    long get_instruction_args(long (*parser)(PyObject* obj));
};