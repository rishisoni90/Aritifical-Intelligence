Name : Chaitanya Dandane
UTA ID : 1001625797

Programming language : Python

Code Structure :
3 inputs are passed to the program through command prompt viz., wumpus_rules, additional information and statement. A tree is created for knowledge base and additional information. check_true_false takes 3 inputs viz., knowledge base, statement and additional symbols. The check_true_false checks if knowledge base entails statement and returns corresponding true or false value. Also, it checks if knowledge base entalis negation of statement and return corresponding true or false value.
The data in additional file is used to minimize the number of calls to TT_Check_all function. It is then stored in additional_symbol.
Dictionary is used to implement model and additional_symbol where, key is symbol and value is truth values(true or false).
PL_true method determines truth value for sentence in the row of truth table shown by model.
Output of inference is stored in result.txt file.

How to run the code?
Type following command in command prompt:
python check_true_false.py wumpus_rules.txt [additional_knowledge_file] [statement_file]  

NOTE: symbols in file are case sensitive and connectives should be in lower case

Reference:
http://vlm1.uta.edu/~athitsos/courses/cse4308_fall2016/lectures/03a_tt_entails.pdf,
Github, Stackoverflow