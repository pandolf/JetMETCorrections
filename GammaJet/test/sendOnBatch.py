#! /usr/bin/env python
import os
import sys
# set parameters to use cmst3 batch 
#######################################
### usage  cmst3_submit_manyfilesperjob.py dataset njobs applicationName queue 
#######################################
if len(sys.argv) != 6:
    print "usage sendOnBatch.py dataset recoType njobs applicationName queue"
    sys.exit(1)
dataset = sys.argv[1]
recoType = sys.argv[2]
#inputlist = "files_EG_Run2010A_PromptReco_v4.txt"
#inputlist = "files_EG_Run2010A_Jun14thReReco_v1.txt"
inputlist = "files_QCD_Spring10_Pt5to15.txt"
#inputlist = "files_MinimumBias_Commissioning10_SD_EG_Jun14thSkim_v1.txt"
#settingfile = "config/RSZZsettings.txt"
output = dataset
# choose among cmt3 8nm 1nh 8nh 1nd 1nw 
#queue = "cmst3"
#queue = "cms8nht3"
queue = sys.argv[5]
#ijobmax = 40
ijobmax = int(sys.argv[3])
#application = "VecbosApp"
application = sys.argv[4]
# to write on the cmst3 cluster disks
################################################
#castordir = "/castor/cern.ch/user/m/mpierini/CMST3/Vecbos/output/"
#outputmain = castordir+output
# to write on local disks
################################################
#diskoutputdir = "/cmsrm/pc21_2/pandolf/DATA/EG/Run2010A-PromptReco-v4/"
#diskoutputdir = "/cmsrm/pc21_2/pandolf/DATA/MinimumBias/Commissioning10_SD_EG_Jun14thSkim_v1/"
diskoutputdir = "/cmsrm/pc21_2/pandolf/MC/QCD_Spring10/QCDPt5to15/"
castordir = "/castor/cern.ch/user/p/pandolf/MC/QCD_Spring10/QCDPt5to15/"
#castordir = "/castor/cern.ch/user/p/pandolf/DATA/MinimumBias/Commissioning10_SD_EG_Jun14thSkim_v1/"
outputmain = castordir
diskoutputmain = diskoutputdir
# prepare job to write on the cmst3 cluster disks
################################################
os.system("mkdir -p "+dataset+"_"+recoType)
os.system("mkdir -p "+dataset+"_"+recoType+"/log/")
os.system("mkdir -p "+dataset+"_"+recoType+"/input/")
os.system("mkdir -p "+dataset+"_"+recoType+"/src/")
outputroot = outputmain+"/root/"
if castordir != "none": 
    os.system("rfmkdir -p "+outputmain)
    os.system("rfmkdir -p "+outputroot)
    os.system("rfchmod 777 "+outputmain)
    os.system("rfchmod 777 "+outputroot)
else: os.system("mkdir -p "+outputroot)

if diskoutputdir != "none": 
    os.system("ssh -o BatchMode=yes -o StrictHostKeyChecking=no pccmsrm21 mkdir -p "+diskoutputmain)

#look for the current directory
#######################################
pwd = os.environ['PWD']
#######################################
numfiles = reduce(lambda x,y: x+1, file(inputlist).xreadlines(), 0)
filesperjob = numfiles/ijobmax
extrafiles  = numfiles%ijobmax
input = open(inputlist)
######################################

for ijob in range(ijobmax):
    # prepare the list file
    inputfilename = pwd+"/"+dataset+"_"+recoType+"/input/input_"+str(ijob)+".list"
    inputfile = open(inputfilename,'w')
    # if it is a normal job get filesperjob lines
    if ijob != (ijobmax-1):
        for line in range(filesperjob):
            ntpfile = input.readline() 
            inputfile.write(ntpfile)
            continue
    else:
        # if it is the last job get ALL remaining lines
        ntpfile = input.readline()
        while ntpfile != '':
            inputfile.write(ntpfile)
            ntpfile = input.readline()
            continue
    inputfile.close()

    # prepare the script to run
    outputname = dataset+"_"+recoType+"/src/submit_"+str(ijob)+".src"
    outputfile = open(outputname,'w')
    outputfile.write('#!/bin/bash\n')
    outputfile.write('export STAGE_HOST=castorcms\n')
    #    outputfile.write('cd '+pwd)
    outputfile.write('cp '+pwd+'/Cert_132440-139239_7TeV_StreamExpress_Collisions10_CMSSWConfig.txt $WORKDIR\n')
    outputfile.write('cp '+pwd+'/lumi_by_LS_upto139375.csv $WORKDIR\n')
    outputfile.write('cd $WORKDIR\n')
    outputfile.write(pwd+'/'+application+" "+dataset+" "+recoType+" akt5 "+inputfilename+" _"+str(ijob)+"\n")
    outputfile.write('ls *.root | xargs -i rfcp {} '+outputroot+'\n')
    outputfile.write('ls *.root | xargs -i scp -o BatchMode=yes -o StrictHostKeyChecking=no {} pccmsrm21:'+diskoutputmain+'/{}\n') 
    outputfile.close
    os.system("echo bsub -q "+queue+" -o "+dataset+"_"+recoType+"/log/"+dataset+"_"+str(ijob)+".log source "+pwd+"/"+outputname)
    os.system("bsub -q "+queue+" -o "+dataset+"_"+recoType+"/log/"+dataset+"_"+str(ijob)+".log source "+pwd+"/"+outputname+" -copyInput="+dataset+"_"+str(ijob))
    ijob = ijob+1
    continue
