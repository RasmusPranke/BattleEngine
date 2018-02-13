#include <Python.h>
#include <iostream>
#include <chrono>
#include <thread>
#include <Python.h>
#include "py_parse.h"
#include "game_instance.h"

/*
This is the launch file for BattleDotZombie.
It first creates a game instance which launches the actual game in a new process.
Then it renders the game using said game instance.
*/
/*
int main(int argc, char *argv[])
{
    for (int i = 0; i < argc; i++) {
        std::cout << argv[i] << "\n";
    }
	Game g = Game();
    int runs = 0;
    int i = 0;// g.load_instruction();
    std::cout << "First instruction:" << i << "\n";
    while (i != -1 && runs < 10) {
        switch (i)
        {
        case 1:
            //std::cout << "Creating OID:" << g.get_instruction_args(parse_number) << "\n";
            break;
        case 99:
            std::cout << "Initializing!" << "\n";
            break;
        default:
            std::cout << "Unhandled instruction: " << i << "\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(1000));
            break;
        }
        runs++;
        std::cout << "Runs: " << runs << "\n";
        //i = g.load_instruction();
    }
    std::cout << "Shutting down!" << "\n";
	char c;
	std::cin >> c;
    g.load_instruction();
	return 0;
}*/