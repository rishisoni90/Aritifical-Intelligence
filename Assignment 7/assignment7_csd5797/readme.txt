Name: Chaitanya Dandane
UTA ID: 1001625797

A. TOWER OF HANOI

Predicates:

small(x1,x2): It is TRUE if x1 is smaller than x2.
disk(x): It is TRUE if x is disk.
peg(x): It is TRUE if x is peg.
clear(x): It is TRUE if x is clear.
on(x1,x2): It is TRUE if x1 is on x2.

Operators:

1. move
This action moves a disk from one disk location to another; if both destination and disk moved are clear.

2. movetopeg
This action moves disk from one location to a peg; if both peg and disk moved are clear.

B. 7-PUZZLE

Predicates:

tile(x): It is TRUE if x is tile.
location(x): It is TRUE if x is valid location.
pos(x,y): It is TRUE if x is at y.
adj(x,y): It is TRUE if x is adjacent to y.
free(x): It is TRUE if x is free.

Operators:

1. move
This action moves tile from one location to destination, if destination is free and adjacent to current location.

 