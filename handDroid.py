#!/usr/bin/python
#python 2.7.2

#This script relies on HandBrakeCLI being in your PATH variable
#If you don't want it in your path just go and change it in the conversion string

import os
import time
import datetime

#This is where the script should look for files
inputDir = ""

#It will output files here
outputDir = ""

#Specify the Handbrake preset here
#Example:
# '--preset "Android High"'
preset = ''

#Specify where you want the logfile
# use the \\ syntax
logFile = ""

#What the new extension will be. It probably should be "mkv" or "m4v". Note that
# no period is needed
newExt = "m4v"

#List of video formats. This list is pretty small at the moment.
fileFormats = ["mpg", "mkv", "avi", "wmv", "mp4", "flv", "mt2s", "mpeg", "mov", "f4v" ]

def isVideoFile(ext):
	for f in fileFormats:
		if(str.lower(ext) == f):
			return True
	return False
	
#This function provides for more consistent formatting of the logfile	
def addZero(num):
	if(len(str(num)) == 1):
		return "0" + str(num)
	else:
		return str(num)

def timeString():
	t = time.localtime()
	month = addZero(t.tm_mon)
	day = addZero(t.tm_mday)
	year = addZero(t.tm_year)
	hour = ""
	
	if(t.tm_hour > 12):
		hour = addZero(t.tm_hour - 12)
	elif(t.tm_hour == 0):
		hour = "12"
	else:
		hour = addZero(t.tm_hour)
		
	minutes = addZero(t.tm_min)
	seconds = addZero(t.tm_sec)
	ampm = ""
	
	if(t.tm_hour < 12):
		ampm = "AM"
	else:
		ampm = "PM"
	
	#this is unecessary but provides an easier to read format
	# for the return string
	h = "-"
	s = " "
	c = ":"
		
	return month + h + day + h + year + s + hour + c + minutes + c + seconds + s + ampm

def convertTime(seconds):
 	hours = int(seconds / 3600)
	seconds = seconds - hours * 3600
	minutes = int(seconds / 60)
	seconds = seconds - minutes * 60
	seconds = int(seconds % 60)
	s = addZero(hours) + " hours " + addZero(minutes) + " mins " + addZero(seconds) + " secs"  
	return s
	
def humanSize(bytes):
	gb = 1073741824.0
	mb = 1048576.0
	kb = 1024.0
	if(bytes > gb):
		left = int(bytes/gb)
		bytes = bytes - left * gb
		percent = round((bytes/gb), 2)
		return str(percent + left) + " GB"
	elif(bytes > mb):
		left = int(bytes/mb)
		bytes = bytes - left * mb
		percent = round((bytes/mb), 2)
		return str(percent + left) + " MB"
	elif(bytes > kb):
		left = int(bytes/kb)
		bytes = bytes - left * kb
		percent = round((bytes/kb), 1)
		return str(percent + left) + " KB"
	else:
		return str(bytes) + " B"
	
if(os.path.exists(inputDir) == False):
	print "Input directory doesn't exist"
	exit()
if(os.path.exists(outputDir) == False):
	print "Output directory doesn't exist"
	exit()
	
inFiles = os.listdir(inputDir)
outFiles = os.listdir(outputDir)

#Cycles through files and converts them
for f in inFiles:
	splitName = f.split('.')
	length = len(splitName) - 1
	oldExt = splitName[length]
	if(isVideoFile(oldExt)):
		oldFile = ".".join(splitName)
		splitName[length] = newExt
		newFile = ".".join(splitName)
		if(os.path.exists(outputDir + newFile)):
			print "File already exists"
		else:
			oldSize = os.path.getsize(inputDir+oldFile)
			start = time.time()
			os.system('handBrakeCLI -i "' + inputDir + oldFile + '"' + ' -o "' + outputDir + newFile +'" ' + preset)
			end = time.time()
			total = end - start
			newSize = os.path.getsize(outputDir+newFile)
			comprSize = str(round((float(newSize)/float(oldSize)), 2))
			log = open(logFile, 'a')
			log.write(timeString() + " " + convertTime(total) + "\t" + humanSize(oldSize) + " " + humanSize(newSize) + " " + comprSize + "\n")
			log.close()