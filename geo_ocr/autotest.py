# -*- coding: utf-8 -*-
import subprocess
import os
import sys
import read
from Levenshtein import ratio

amount = 0
photos = []
textfiles = []
resultarray = []
print 'testing directory:\t' , sys.argv[1]
argument = sys.argv[1]
location = "tests/automate/" + argument + "/"

for file in os.listdir(location):
    try:
        if file.startswith("output"):
            print "output file found" , file  
        elif file.endswith(".txt"):
            print "text file foufnd:\t", file
            textfiles.append(str(file))
            resultarray.append(str(file)) 
            amount +=1 
        else:
            photos.append(file)
            print "input files found:\t", file
    except Exception as e:
        raise e
        print "No files found here! " "print ""Total files found:\t", amount


print "textfiles " , textfiles 
print "photos" , photos
print amount


i=0
testresults = {}
total = 0

def compare(text , photo):
    global total
    txt = open(location+text, "r+")
    data = txt.read()
    print text , photo
    try:
        pic =open("tests/automate/output.txt" , "wr")
        pic.write(read.read(location+photo, False, False ).encode('utf-8'))
        pic = open("tests/automate/output.txt"  , "r")
        result = pic.read()
        testresults.update({photo : ratio(data , result)})
        print "data" , data
        print  "result" , result
        print  photo, ratio(data , result)
        total += ratio(data , result)
    except Exception as e:
        print "error ocured with ", text , photo, e
        testresults.update({photo:0})
    return total 
for txt in textfiles:
    for pic in photos:
        if os.path.splitext(os.path.basename(txt))[0] == os.path.splitext(os.path.basename(pic))[0]:			
            total = compare(txt , pic)


average = total / amount


for name, value in testresults.items():
    if value > 0.7:
        print ( '\033[92m' + name + '\033[0m') , round(value *100, 1) , "%"
    else:
        print ( '\033[91m'+ name+ '\033[0m') , round(value *100, 1), "%"
if average > 0.7:
    print  ( '\033[92m' + argument+ '\033[0m') , round(total/amount *100 , 1) , "%"
else:
    print ( '\033[91m' +  argument+ '\033[0m') , round(total/amount *100 , 1) , "%"





