#!/usr/bin/python
#python 2.7.2

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
preset = ""

#Specify where you want the logfile
# use the \\ syntax
logFile = ""

#What the new extension will be. It probably should be "mkv" or "m4v". Note that
# no period is needed
newExt = ""

#List of video formats. This list is pretty small at the moment.
fileFormats = ["mpg", "mkv", "avi", "wmv", "mp4", "flv", "mt2s", "mpeg", "mov", "f4v" ]

def isVideoFile(ext):
	for f in fileFormats:
		if(str.lower(ext) == f):
			return True
	return False
	
def isValidDir(directory):
	if(os.path.exists(directory) and os.path.isdir(directory)):
		return True
	else:
		return False
		
def makeDirs(directory):
	os.makedirs(directory)
	return

#Formats the directory string to how I want it (to have a trailing '\')
def trailingSlash(directory):
	directory = directory.replace("\n", "")
	if(directory[len(directory) - 1] != "\\"):
		return directory + "\\"
	else:
		return directory

def menu():
	x = True
	while(x):
		print "Where is the input directory?"
		console = raw_input()
		if(isValidDir(trailingSlash(console))):
			inputDir = trailingSlash(console)
			x = False
	x = True
	while(x):
		print "Where is the output directory?"
		console = raw_input()
		if(isValidDir(trailingSlash(console))):
			inputDir = trailingSlash(console)
			x = False
	x = True
	print "Where would you like the log file?"
	console = raw_input()
	logFile = console
	print "Where would you like the log file?"
	console = raw_input()
	newExt = console
	print "What is the preset?"
	console = raw_input()
	preset = console
	return		
		
def buildSettings(settings):
	for s in settings:
		if(s[0] == "InputDirectory"):
			if(isValidDir(trailingSlash(s[1])) == True):
				global inputDir
				inputDir = trailingSlash(s[1])
			else:
				None
		elif(s[0] == "OutputDirectory"):
			if(isValidDir(trailingSlash(s[1])) == True):
				global outputDir
				outputDir = trailingSlash(s[1])
			else:
				None
		elif(s[0] == "LogFile"):
			global logFile
			logFile = s[1].replace("\n", "")
		elif(s[0] == "Preset"):
			global preset
			preset = s[1].replace("\n", "")
		elif(s[0] == "Extension"):
			global newExt
			newExt = s[1].replace("\n", "")
		else:
			None

	return
	
#Read from settings file, if wrong or non existent builds new settings file	
#Implement menu via if-elif-else statements
def readSettingsFile():
	if(os.path.exists(os.path.dirname(__file__) + "\\handdroid.settings")):
		f = open(os.path.dirname(__file__) + "\\handdroid.settings")
		settings = []
		for line in f:
			if(len(line.split("=")) == 2):
				settings.append(line.split("="))
		buildSettings(settings)
	else:
		menu()
	return
	
def writeSettingsFile():
	global inputDir
	global outputDir
	global preset
	global logFile
	global newExt
	f = open(os.path.dirname(__file__) + "\\handdroid.settings", 'w')
	f.write("InputDirectory=" + inputDir + "\n")
	f.write("OutputDirectory=" + outputDir + "\n")
	f.write("Preset=" + preset + "\n")
	f.write("LogFile=" + logFile + "\n")
	f.write("Extension=" + newExt + "\n")
	return
	
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
	#Old
	#s = addZero(hours) + " hours " + addZero(minutes) + " mins " + addZero(seconds) + " secs"
	s = addZero(hours) + "." + addZero(minutes) + "." + addZero(seconds) 
	return s
	
def humanSize(bytes):
	gb = 1073741824.0
	mb = 1048576.0
	kb = 1024.0
	if(bytes > gb):
		left = int(bytes/gb)
		bytes = bytes - left * gb
		percent = round((bytes/gb), 2)
		return "%6s GB" % str(percent + left)
	elif(bytes > mb):
		left = int(bytes/mb)
		bytes = bytes - left * mb
		percent = round((bytes/mb), 2)
		return "%6s MB" % str(percent + left)
	elif(bytes > kb):
		left = int(bytes/kb)
		bytes = bytes - left * kb
		percent = round((bytes/kb), 1)
		return "%6s KB" % str(percent + left)
	else:
		return "%6s B" % str(bytes)

###############################
##Start of program logic here##
###############################
		
readSettingsFile()
		
if(os.path.exists(inputDir) == False):
	print "Input directory doesn't exist"
	exit()
if(os.path.exists(outputDir) == False):
	print "Output directory doesn't exist"
	exit()
	
writeSettingsFile()

#Cycles through files and converts them
totalConverted = 0
while(True):
	inFiles = os.listdir(inputDir)
	outFiles = os.listdir(outputDir)
	currentConverted = 0
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
				comprSize = "%3s%%" % str(round((float(newSize)/float(oldSize)), 3) * 100)
				log = open(logFile, 'a')
				log.write("%s  %s %s %s %s\n" % (timeString(), convertTime(total), humanSize(oldSize), humanSize(newSize), comprSize))
				log.close()
				currentConverted = currentConverted + 1
				totalConverted = totalConverted + 1
	if(currentConverted == 0):
		break

if(totalConverted == 1):
	print "Converted 1 file"
	log = open(logFile, 'a')
	log.write("Converted 1 file\n\n")
	log.close()
else:
	print "Converted " + str(totalConverted) + " files"
	if(totalConverted != 0):
		log = open(logFile, 'a')
		log.write("Converted " + str(totalConverted) + " files\n\n")
		log.close()