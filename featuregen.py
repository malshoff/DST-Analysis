# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 18:20:25 2018

@author: Malachis
"""

import  argparse, json, os
from sluRes import sluResult
import nltk

def sluCounts(cumul):
    
    cfd = nltk.ConditionalFreqDist(cumul)
    cfd.tabulate()
    return cfd
    #with open("part3.py", 'w') as outputfile:
     #    outputfile.write(json.dumps(cfdList))
         
def main():
    cumulative = []
    sluList = []
    lenList = []
    parser = argparse.ArgumentParser(description='Simple hand-crafted dialog state tracker baseline.')
    parser.add_argument('--dataset', dest='dataset', action='store', metavar='DATASET', required=True,
                        help='The dataset to analyze')
    parser.add_argument('--dataroot',dest='dataroot',action='store',required=True,metavar='PATH',
                        help='Will look for corpus in <destroot>/<dataset>/...')
    args = parser.parse_args()

    source = os.getcwd()
    fileListName = os.path.join(os.path.join(os.getcwd(),"scripts/config"),args.dataset+".flist")
    fileList = open(fileListName)  # opens flist file
    
    for fName in fileList :        # iterate through each dialog
        with open("part3.py", 'w') as outputfile:
            print("Dialog:"+ str(fName))
            turnData = []
            fName = fName[0:len(fName)-1]
            call = json.load(open(os.path.join(os.path.join(source,args.dataroot),os.path.join(fName,"log.json"))))
            label = json.load(open(os.path.join(os.path.join(source,args.dataroot),os.path.join(fName,"label.json"))))
            # iterate through each dialog turn; 
            # call is the data from the actual interaction (log.json)
            # label is the data provided by after dialog labeling (label.json)
        
            for turn,turnLabel in zip(call["turns"],label["turns"]) :
                slu = sluResult(turn,turnLabel)
                transcription = turnLabel["transcription"]
                length = len(transcription.split())
                sluList.append(slu)
                lenList.append(length)
                turnData.append((length,slu))
                cumulative.append((length,slu))
            
            sluCounts(cumulative)
            
            print(turnData)
            #outputfile.write(json.dumps(sluCounts(cumulative)))
 
    
if __name__ == '__main__':
    main()
