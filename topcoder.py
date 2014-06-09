import sys
import os
import re

if len(sys.argv) != 2:
	print "Specify Solution Name in argv"
	sys.exit(1)

SolutionName = sys.argv[1]
S = "[a-zA-Z0-9\'\"\[\]{}()\\\\,.:]"
# Template Directory
TPD = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/template"

class State:
	def __init__(this, state_name, transition=False, action=False):
		this.transitions = []
		if transition: SetTransition(transition[0], transition[1])
		this.actions = []
		if action: SetAction(action[0], action[1])
		this.name = state_name
		this.enterAction = None
		this.endAction = None
	
	def Enter(this):
		if this.enterAction:
			this.enterAction(this)

	def End(this):
		if this.endAction:
			this.endAction(this)

	def Check(this, line):
		return this._Check_transition(line) or this._Check_action(line)

	def SetTransition(this, regex, new_state):
		this.transitions.append([re.compile(regex), new_state])

	def SetAction(this, regex, action):
		this.actions.append([re.compile(regex), action])

	# if condition met goto corresponding state
	def _Check_transition(this, line):
		for [condition, new_state] in this.transitions:
			res = condition.search(line)
			if res:
				return new_state
		return False

	# if condition met called action
	def _Check_action(this, line):
		for [condition, action] in this.actions:
			res = condition.search(line)
			if res:
				next_state = action(this, res)
				if next_state:
					return next_state

os.system("cp -f " + TPD + "/header.py " + SolutionName + ".py")
code = open(SolutionName + ".py", "a")

#### set state 
start = State("Start")
# problem statement
pss = State("Problem Statement")
# Definition
defs = State("Definition")
# Class
ClassName = "ClassName"
classs = State("Class")
# End Class
endClasss = State("End of Class")
# Method
MethodName = "MethodName"
methods = State("Method:")
# End Method
endMethods = State("End of Method")
# Parameters
params = State("Parameters")
Param_type_list = []
Param_list = []
# End Parameters
endParams = State("End of Parameters")
# Return
returns = State("Return")
# End Return
endReturns = State("End of Return")
# Method Signature
methodss = State("Method Signature")
# End Method
endMethodss = State("End of Method Signature")
# Examples
examples = State("Examples")
# Param type state
cases = State("Case Parameters & Return Value")
CaseNo = "shouldBeANumber"

# SetTransition
start.SetTransition("^\s*Problem Statement\s*$", pss)
pss.SetTransition("^\s*Definition\s*$", defs)
defs.SetTransition("^\s*Class:\s*$", classs)
def classs_action(this, res):
	global ClassName
	ClassName = res.group(1)
	code.write("class "+res.group(1)+":\n")
	return endClasss
classs.SetAction("^\s*("+S+"*)\s*$", classs_action)
endClasss.SetTransition("^\s*Method:\s*$", methods)

def method_action(this, res):
	global MethodName
	MethodName = res.group(1)
	return endMethods
methods.SetAction("^\s*("+S+"*)\s*$", method_action)
endMethods.SetTransition("^\s*Parameters:\s*$", params)
def params_action(this, res):
	# read a line and goto end
	global Param_type_list
	Param_type_list = [s.strip(" ") for s in res.group(1).split(",")]
	code.write("\t# Params: "+res.group(1)+"\n")
	return endParams
params.SetAction("^\s*(.*"+S+")\s*$", params_action)
endParams.SetTransition("^\s*Returns:\s*$", returns)

def returns_action(this, res):
	# read a line and goto end
	code.write("\t# Return: "+res.group(1)+"\n")
	return endReturns
returns.SetAction("^\s*(.*"+S+")\s*$", returns_action)
endReturns.SetTransition("^\s*Method signature:\s*$", methodss)

def methods_action(this, res):
	# read a line and goto end
	code.write("\t"+res.group(1)+"\n")
	return endMethodss
methodss.SetAction("^\s*(def.*"+S+")\s*$", methods_action)
endMethodss.SetTransition("^\s*Examples\s*$", examples)

def exampleAction(this, res):
	global CaseNo
	CaseNo = res.group(1)
	return cases

examples.SetAction("^\s*([0-9]+)\)\s*$", exampleAction)

def paramEnterAction(this):
	this.param_idx = 0

def paramAction(this, res):
	global Param_list, Param_type_list
	if this.param_idx >= len(Param_type_list):
		# or just return directly?
		print "[Error] more parsed param than needed"
		sys.exit(1)
	p = Param_type_list[this.param_idx]
	if p.startswith("tuple"):
		# bnum -> bracket number
		if not hasattr(this, "bnum"):
			# first enter tuple state
			this.tupStr = ""
			this.bnum = 0
		this.tupStr += res.group(1)
		this.bnum += res.group(1).count("{") - res.group(1).count("}")
		if this.bnum == 0:
			# end of tuple state
			Param_list.append(this.tupStr.replace("{", "(").replace("}",")"))
			del this.tupStr, this.bnum
			this.param_idx += 1
	elif p == "integer" or p == "string" or p == "long integer" or p == "float":
		Param_list.append(res.group(1))
		this.param_idx += 1
	else:
		print "Unsupport Param Type " + p
		sys.exit(1)

def returnValueAction(this, res):
	# Returns: res.group(1)
	global Param_list, CaseNo, ClassName
	correctValue = res.group(1)
	# gen test code
	os.system("cp -f " + TPD + "/run.py .")
	os.system("mkdir -p testcases")
	os.system("cp -f " + TPD + "/testcases.py testcases/tmp")
	os.system("sed 's/CLASSNAME/"+ClassName+"/;" + \
				"s/SOLUTIONNAME/"+SolutionName+"/;" + \
				"s/METHODNAME/"+MethodName+"/;" + \
				"s/CORRECTVALUE/"+correctValue+"/;" + \
				"s/PARAMETERLIST/"+(",".join(Param_list)).replace("\'", "\"")+"/;' " + \
		   		"testcases/tmp > testcases/test" + CaseNo + ".py")
	os.system("rm -f testcases/tmp")
	
#	testFile = open("testcases/test" + CaseNo + ".py", "w")
#	# for relative import parent dir
#	testFile.write("import os\n")
#	testFile.write("import sys\n")
#	testFile.write("sys.path.append(\"/\".join(os.path.abspath(__file__).split(\"/\")[:-2]))\n")
#	testFile.write("from " + SolutionName + " import " + ClassName + "\n")
#	testFile.write("result = " + ClassName + "()." + MethodName + "(" + ",".join(Param_list) + ")\n")
#	testFile.write("if result == " + correctValue + ":\n")
#	testFile.write("\tprint \"Yes\"\n")
#	testFile.write("else:\n")
#	testFile.write("\tprint \"No\"\n")
	#testFile.write("\tprint \"your result: \" + result\n")
	# exit with error code 0

	Param_list = []
	return examples

cases.enterAction = paramEnterAction
# check if return first
cases.SetAction("^\s*Returns:\s*(.*"+S+")\s*$", returnValueAction)
# then catch param
cases.SetAction("^\s*(.*"+S+")\s*$", paramAction)

cur_state = start
for line in sys.stdin:
	x = cur_state.Check(line)
	if x:
		cur_state.End()
		cur_state = x
		cur_state.Enter()
print cur_state.name
print Param_type_list
code.close()
# tuple (string), tuple (integer), long integer, integer, float, string
