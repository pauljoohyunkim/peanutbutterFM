testgen:
	mkdir TEST1
	mkdir TEST2
	mkdir TEST3
	touch testfile1
	touch testfile2
	touch testfile3
	touch testfile4

testclean:
	rmdir TEST*
	rm testfile*