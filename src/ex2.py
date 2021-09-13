#!/usr/bin/python3
"""Exercise 2

Assess precision of a suggested solution of fragments coordinates and orientation based on the real solution
Run by providing the following parameters:

ex2 [Dx (px)] [Dy (px)] [Dalpha (deg)]

Authors: Sophie Nguyen <sophie.nguyen@universite-paris-saclay.fr>, Tom Mansion <tom.mansion@universite-paris-saclay.fr>
"""

# TODO: Fragment comparison function: returns true if the difference in x, y and orientation alpha is lower than the set parameters, returns false is not
# TODO: Compute fragment surface function

# TODO: MAIN FUNCTION 

# TODO: Retrieve user parameters and store it in ref object
# TODO: Read suggested solution.txt file, store the fragments data in list
# TODO: Read real solution fragments.txt file, store the solution fragments data in list

# TODO: Filtering: For each solution fragment, find if real solution includes this fragment
# If true, call Fragment comparison function
#   If it returns true, store it in well located fragments list
# If false, store it in not belonging list

# TODO: Compute surface of well located fragments
# TODO: Compute surface of not belonging fragments
# TODO: Compute surface of all fragments of fragments.txt
# TODO: Compute precision p with the computed surfaces

# TODO (enhancement): Show exceeded pixels in red on the fresco