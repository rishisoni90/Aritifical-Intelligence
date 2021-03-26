Name: Chaitanya Dandane

UTA ID: 1001625797

Programming language: Python

Code Structure:
1) Program take input from command line as specified input format. There are two modes i.e.; onemove or interactive out of which one has to specified in input for respective mode. The output file is generated for onemove or computernext or humannext.
2) The input is passed to program through text file.
3) The input data is represented as tree.
4) In onemove mode, the present game state is taken from input file and the present state is printed with it's respective scores. Then the present board state is passed to onemovegame() function with depth given in cmd argument. The onemovegame function calls aiplay function which implements the depthlimited version of minimax.
5) In interactive mode, the present board state is set from input specified in input file. In case the input file is missing, an empty board game is created. Then the present game state is passed to interactivegame() function with it's depth.
6) The interactivegame function will call aiplay_interactive function with the present board game state and pass it further to function based on move (human-next/computer-next) from cmd argument. If the input given is human-next, then program will ask user to make a move and the output is logged in human.txt file and then computer will make it's move. When it's computer turn to make a move; the minimax function is called and then it's corresponding output is logged in computer.txt file.
7) These all steps repeats until the game board is full(i.e.; piecount = 42).
8) Utility values are computed from terminal_test function and the evaluation function eval_fn.

To run the code:
For one-move game, execute following command in cmd:
python maxconnect4.py one-move input_file_name output_file_name depth

For interactive game, execute following command in cmd:
python maxconnect4.py interactive input_file_name (computer-next/human-next) depth


# REFERENCES: Github, Stackoverflow and other online forums