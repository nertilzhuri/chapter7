

def run(**args):
	print "[*] In test_mod"
	
	s = ""
	
	s += "hello World\n"
	s += "Testing trojan\n"
	s += "Args are: %s" % str(args['tm'])
	
	return s
