# -*- coding: utf-8 -*-
import geo_ocr
import subprocess
from Levenshtein import ratio

textfiles=["160.txt",  "cxoveli.txt", "logikuri.txt", "logikuri-mcdaria.txt", "mqsoveli.txt", "mtacebeli.txt", "nika.txt", "procenti.txt", "proporciuli.txt" , "datom.txt" , "gafrinda.txt" , "miigos.txt" , "220.txt"]

b=["160.jpg","cxoveli.jpg","logikuri.jpg","logikuri-mcdaria.jpg","mqsoveli.jpg","mtacebeli.jpg","nika.jpg","procenti.jpg","proporciuli.jpg" , "datom.jpg" , "gafrinda.jpg" , "miigos.jpg" ,"220.jpg"]

i=0
y=0
total =0
testresults = []
while i < (len(textfiles)):
	txt = open("tests/automate/level1/"+textfiles[i], "r+")
	data = txt.read()
	print textfiles[i] , b[i]
	try:
		pic =open("tests/automate/level1/output.txt" , "wr")
		pic.write(geo_ocr.read("tests/automate/level1/"+b[i], False, False).decode('utf-8').encode('utf-8'))
		pic = open("tests/automate/level1/output.txt" , "r")
		result = pic.read()
		testresults.append(ratio(data , result))

		print "data" , data
		print  "result" , result
		print  b[i], ratio(data , result)

		total += ratio(data , result)
	except Exception as e:
		print "error ocured with ", textfiles[i] , b[i], e
		testresults.append(0)
		total +=0
	finally:
		i+=1
average = total/len(textfiles)
#green = ( '\033[92m'%round(testresults[y] *100, 1) + '\033[0m')
#red = ( '\033[91m' %round(testresults[y] *100, 1) + '\033[0m')
for y in range(len(testresults)):
	if testresults[y] > 0.7:
		print ( '\033[92m' + b[y]+ '\033[0m') , round(testresults[y] *100, 1) , "%"
	else:
		print ( '\033[91m'+ b[y]+ '\033[0m') , round(testresults[y] *100, 1), "%"
	y+=1
if average > 0.7:
	print  ( '\033[92m' + "LEVEL 1 AVERAGE "+ '\033[0m') , round(total/len(textfiles) *100 , 1) , "%"
else:
	print ( '\033[91m' +  "LEVEL 1 AVERAGE " + '\033[0m') , round(total/len(textfiles) *100 , 1) , "%"