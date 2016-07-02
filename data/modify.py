import os

files = os.listdir("../data")
i = 0
for a in files:
	i+=1
	f = a.strip()
	data = open(f,"r+")
	d = data.read()
	d = d.replace("","").replace("","")
	data.seek(0)
	data.write(d)
	data.close()
print (i)
 
