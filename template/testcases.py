# for relative import parent dir
import os
import sys
sys.path.append("/".join(os.path.abspath(__file__).split("/")[:-2]))
from SOLUTIONNAME import CLASSNAME
result = CLASSNAME().METHODNAME(PARAMETERLIST)
if result == CORRECTVALUE:
	print "Result: YES"
else:
	print "Result: NO"
	print "Input:"
	print (PARAMETERLIST)
	print "Program output:"
	print result
	print "Answer:"
	print CORRECTVALUE
