import os, sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--samples", dest="samples", help="List of samples info <sampleID>\T<population> format", metavar="FILE")
parser.add_option("-i", "--input", dest="input", help="A file with a list of samples", metavar="FILE")
(options, args) = parser.parse_args()
samplesFile=options.samples
inputFile=options.input

file = open(samplesFile, "r")

samplesDB={}
#Reading samples info file in order to create our initial statistics
for line in file:
    newlinesplit=line.split("\n");
    words = newlinesplit[0].split("\t")
    lineSampleID=words[0]
    linePopulatioName = words[1]
    # check if population exists
    if ((linePopulatioName in samplesDB) == True):
        samplesDB[linePopulatioName].append(lineSampleID)
    else:
        samplesDB[linePopulatioName] = []
        samplesDB[linePopulatioName].append(lineSampleID)

file.close()

samples={}
#lets parse files
file = open(inputFile, "r")
for line in file:
    words = line.split("\n")
    lineSampleIDD=words[0]
    for item in samplesDB:
        if(lineSampleIDD in samplesDB[item]):
            if ((item in samples) == True):
                samples[item].append(lineSampleIDD)
            else:
                samples[item] = []
                samples[item].append(lineSampleIDD)
            samplesDB[item].remove(lineSampleIDD)
file.close()

#Writing results to a new folder
foldername=str(inputFile)+".samples/"
os.mkdir( foldername, 0755 );
for item in samples:
    out = foldername + str(inputFile)+"."+ str(item) + ".list"
    file = open(out, "w")
    for iitem in samples[item]:
        file.write(str(iitem)+"\n")
    file.close()