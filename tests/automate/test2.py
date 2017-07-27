# -*- coding: utf-8 -*-
import geo_ocr
import subprocess
from Levenshtein import ratio

a=["bad-light.txt", "charkviani.txt", "mnatobi.txt", "mnatobi-koshmari.txt", "mnatobi-lines.txt", "mnatobi-mini.txt", "mtavruli.txt", "mtavruli-bold.txt", "phone-1.txt"]
b=["bad-light.jpg", "charkviani.jpg", "mnatobi.png", "mnatobi-koshmari.png", "mnatobi-lines.png", "mnatobi-mini.png", "mtavruli.png", "mtavruli-bold.png", "phone-1.jpg"]
i=0
y=0
total =0
testresults = []
while i < (len(a)):
	txt = open("tests/automate/level2-badlight/"+a[i], "r+")
	data = txt.read()
	print a[i] , b[i]
	pic =open("tests/automate/level2-badlight/output.txt" , "wr")
	pic.write(geo_ocr.read("tests/automate/level2-badlight/"+b[i], False, False).encode('utf-8').strip())
	pic = open("tests/automate/level2-badlight/output.txt" , "r")
	result = pic.read()
	testresults.append(ratio(data , result))

	print "data" , data
	print  "result" , result
	print  b[i], ratio(data , result)
	total += ratio(data , result)
	i+=1
average = total/len(a)
#green = ( '\033[92m'%round(testresults[y] *100, 1) + '\033[0m')
#red = ( '\033[91m' %round(testresults[y] *100, 1) + '\033[0m')
for y in range(len(testresults)):
	if testresults[y] > 0.7:
		print ( '\033[92m' + b[y]+ '\033[0m') , round(testresults[y] *100, 1) , "%"
	else:
		print ( '\033[91m'+ b[y]+ '\033[0m') , round(testresults[y] *100, 1), "%"
	y+=1
if average > 0.7:
	print  ( '\033[92m' +"LEVEL 2 AVERAGE " + '\033[0m') , round(total/len(a) *100 , 1) , "%"
else:
	print ( '\033[91m' +  "LEVEL 2 AVERAGE "+ '\033[0m') , round(total/len(a) *100 , 1) , "%"
