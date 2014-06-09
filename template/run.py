import os

x = os.walk("./testcases/")
(a, b, filenames) = x.next()
x.close()

for filename in filenames:
	if os.system("python " + a + filename):
		print "Failed on " + filename
		break

