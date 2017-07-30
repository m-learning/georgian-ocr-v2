# -*- coding: utf-8 -*-
import geo_ocr
import subprocess
import os
import sys
from Levenshtein import ratio

counter = 0
photos = []
textfiles = []

print 'testing directory:\t' , sys.argv[1]
location = "tests/automate/" + sys.argv[1] + "/"

for file in os.listdir(location):
   try:
	if file.startswith("output"):
	   print "output file found" , file  
	elif file.endswith(".txt"):
           print "text file found:\t", file
           textfiles.append(str(file))  
	else:
           photos.append(file)
	   print "input files found:\t", file
           counter = counter+1
   except Exception as e:
       raise e
       print "No files found here! " "print ""Total files found:\t", counter

textfiles.sort()
photos.sort()

print "textfiles " , textfiles 
print "photos" , photos
print counter


i=0
testresults = []
total=0
while i < counter:
	txt = open(location+textfiles[i], "r+")
	data = txt.read()
	print textfiles[i] , photos[i]
	try:
		pic =open("tests/automate/output.txt" , "wr")
		pic.write(geo_ocr.read(location+photos[i], False, False).decode('utf-8').encode('utf-8'))
		pic = open("tests/automate/output.txt"  , "r")
		result = pic.read()
		testresults.append(ratio(data , result))

		print "data" , data
		print  "result" , result
		print  photos[i], ratio(data , result)
		total += ratio(data , result)
	except Exception as e:
		print "error ocured with ", textfiles[i] , photos[i], e
		testresults.append(0)
		total +=0
	finally:	
		i+=1
average = total/len(textfiles)
for y in range(len(testresults)):
	if testresults[y] > 0.7:
		print ( '\033[92m' + photos[y]+ '\033[0m') , round(testresults[y] *100, 1) , "%"
	else:
		print ( '\033[91m'+ photos[y]+ '\033[0m') , round(testresults[y] *100, 1), "%"
	y+=1
if average > 0.7:
	print  ( '\033[92m' +"LEVEL 2 AVERAGE " + '\033[0m') , round(total/len(textfiles) *100 , 1) , "%"
else:
	print ( '\033[91m' +  "LEVEL 2 AVERAGE "+ '\033[0m') , round(total/len(textfiles) *100 , 1) , "%"









