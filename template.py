# template.py
# A template for iterating through the sequence of dialogs in an flist
# and accessing the data from both the log.json and label.json files
# Demonstration Code dumps information about the dialog acts of both 
#   the system and user
#
# Usage:  python3 scripts/template.py --dataroot data --dataset <flist>
#
# <flist> is the prefix name of a list of file id's: located in scripts/config
#
# e.g. python3 scripts/template.py --dataroot data --dataset all.
#
# Also compatible with python version 2

import  argparse, json, os
from collections import defaultdict

def jsonItemToCued(i):
    if len(i) > 2:
        print ("Unsure what to do about " + str(i))
    if len(i) > 1:
        return str(i[0]) + "=" + str(i[1])
    elif len(i) == 1:
        return i[0]
    else:
        return ""    

def jsonActToCued(a):
    return a["act"] + "(" + ",".join(jsonItemToCued(i) for i in a["slots"]) + ")"

#Converts a json format utterance to a CUED-style string
def jsonToCued(d):
    ans = "|".join(jsonActToCued(a) for a in d)
    return ans

def main() :
    
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
       fName = fName[0:len(fName)-1]
       call = json.load(open(os.path.join(os.path.join(source,args.dataroot),os.path.join(fName,"log.json"))))
       label = json.load(open(os.path.join(os.path.join(source,args.dataroot),os.path.join(fName,"label.json"))))
       # iterate through each dialog turn; 
       # call is the data from the actual interaction (log.json)
       # label is the data provided by after dialog labeling (label.json)
       for turn,turnLabel in zip(call["turns"],label["turns"]) :
          print (jsonToCued(turn["output"]["dialog-acts"]))
          print ("   ", jsonToCued(turnLabel["semantics"]["json"]))
       print ("**************************************************************")

if __name__ == '__main__':
    main()
