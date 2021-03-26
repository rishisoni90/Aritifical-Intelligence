Name: Chaitanya Dandane

UTA ID: 1001625797

Programming Language: Python

Code Structure:
1) Take input from command prompt. The input command includes Filename inputfile sourcecity destinationcity.
2) The input data is read from specified file.
3) The data is then represented in graph.
4) Uniform cost search algorithm is used to find the shortest path between source and destination city.
5) Whenever the node is explored, it is then pass to fringe. Fringe is implemented using dictionary with city name as key and weight as value. Due to fringe, the node with minimum weight is selected, which gives optimum path. This is Uniform cost search algorithm.
6) The output is displayed in expected format.

To run the code:
Type following command to run the program via command prompt:

python find_route.py file_name Bremen Kassel


