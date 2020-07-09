from optparse import OptionParser

parser = OptionParser( description= "VCF Filter by Sample Quantity -  "
                                    "This tool input is a vcf file and a threshold. It is counting the samples that do have a "
                                    "SNP or whatever the line descripes and the samples that dont have and if this number is over the "
                                    "threshold. It keeps this line to a different file. By the end three files will be created."
                                    "Two of them containing information about the summaries and one containing the filtered vcf file")
parser.add_option("-v", "--vcf", dest="vcffile", help="VCF for statistics", metavar="FILE")
parser.add_option("-t", "--threshold", dest="threshold", help="Threshold for filtering", metavar="FILE")
(options, args) = parser.parse_args()

vcfile=options.vcffile
thresholdC=int(options.threshold)


outputfile=vcfile.split(".vcf")[0]+".all.out"
outputfile2=vcfile.split(".vcf")[0]+".filtered.vcf"
outputfile3=vcfile.split(".vcf")[0]+".filtered.out"
file = open(vcfile, "r")
outFile = open(outputfile, "w")
outFile2 = open(outputfile2, "w")
outFile3 = open(outputfile3, "w")


zerozero="0/0"
oneone="1/1"
zeroone="0/1"
onezero="1|0"
phasedFlag =0;
    
outFile.write("VCFilterbySampleQuan\n");
outFile3.write("VCFilterbySampleQuan\n");
for line in file:
    words = line.split("\t")
    zerozeroCounter = 0;    zerooneCounter = 0;    oneoneCounter = 0;   onezeroCounter = 0;
    if ("#" not in line):
        lineChr = words[0]
        linePos = words[1]
        for word in words:
            #check if it is phased or not
            if("|" in word):
                zerozero = "0|0"
                oneone = "1|1"
                zeroone = "0|1"
                phasedFlag =1;
            
            if(zeroone in word):    #01
                zerooneCounter = zerooneCounter + 1
            elif(oneone in word):   #11
                oneoneCounter = oneoneCounter + 1
            elif(zerozero in word): #00
                zerozeroCounter = zerozeroCounter + 1
            elif(onezero in word): #10
                onezeroCounter = onezeroCounter + 1
        #Filtering
        statistics2write = "chr"+words[0] +'\t'+str(linePos)+ "\t"+zerozero+": "+str(zerozeroCounter)+"\t"+zeroone+": " + str(zerooneCounter)+"\t"+oneone+": " + str(oneoneCounter);
        if(phasedFlag == 1):
            statistics2write+="\t"+onezero+": " + str(onezeroCounter);
        statistics2write+='\n';
        
        if(zerozeroCounter>thresholdC and oneoneCounter>thresholdC):
            outFile2.write(line)
            outFile3.write(statistics2write)
        outFile.write(statistics2write)
    else:
        outFile2.write(line)
outFile.close()
outFile3.close()
outFile2.close()
file.close()
