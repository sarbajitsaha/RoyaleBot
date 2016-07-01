f = open("arrows","a")
val1 = 115
val2 = 46
for i in range(1,14):
	f.write("\n\nLvl{0}: {1} {2}".format(i,val1,val2))
	val1 = val1 + (0.1)*val1
	val1 = (int)(val1)
	val2 = val2 + (0.1)*val2
        val2 = (int)(val2)
 
