#Written and tested with python 2.7.3

import os
import handbrakeBatchFuntions

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
#Location of HandbrakeCLI.exe
handBrake = ""
		
if(os.path.exists(inputDir) == False):
	print "Input directory doesn't exist"
	exit()
if(os.path.exists(outputDir) == False):
	print "Output directory doesn't exist"
	exit()

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
				os.system(handBrake + ' -i "' + inputDir + oldFile + '"' + ' -o "' + outputDir + newFile +'" ' + preset)
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