#!/usr/bin/env python
#
#Robert Russell 12/17/18
#
#A python example using the 7 dwarves.

#These import commands add specific python libraries to the program and make their functions available for use
import sys #This library interacts with the underlying system that the python interpreter is running on
import re  #This library makes regular experssions available

#The suits variable is a python dictionary. It stores key value pairs of each dwarf's name and the color of their "suit"
suits = {
        'Bashful':'yellow', 'Sneezy':'brown', 'Doc':'orange', 'Grumpy':'red', 'Dopey':'green', 'Happy':'blue', 'Sleepy':'taupe'
        }

#The pattern variable is set here using both the regex and sys libraries imported earlier. The script takes the first command line
#argument and executes a regex search for the pattern in each dwarf and suit name.
pattern = re.compile("(%s)" % sys.argv[1])

#This for loop iterates over each key value pair in the suits dictionary. If either the dwarf or the suit color matches the regex
#search complied in the pattern variable, it will perform substitution to highligh the matching letters with underscores.
#The break on line 26 ends the script after the first match. The else statement on line after it displays text if no matches are found.

for dwarf, color in suits.items():
    if pattern.search(dwarf) or pattern.search(color):
        print("%s's dwarf suit is %s." %
                (pattern.sub(r"_\1_", dwarf), pattern.sub(r"_\1_", color)))
        break
else:
    print("No dwarves or dwarf suits matched the pattern.")

