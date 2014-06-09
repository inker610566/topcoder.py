topcoder.py
===========

Auto generate SRM python test template from problem description

Tested Platform:

	* Mac OS/ bash/ python 2.7.6

Usage:
	
	# template/header.py contains user defined solution header
	# generate template in current directory
	> python topcoder.py source_name
	# it will open a vim buffer in insert mode
	# paste the problem statement to the buffer and save
	# implement source_name.py
	# run test
	> python run.py
	# the result will print on screen

TODO:
	
	* separate sed file from topcoder.py
