

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
def jsonItemToCued(i):
    #i = list(i)
    #print(i)
    
    if len(i) > 2:
        return
    if len(i) > 1:
        return ((i[0]),(i[1]))
    elif len(i) == 1:
        return i[0]
    else:
        return     
def removeEmpty(a):
    i = len(a)
    while i > 0:
        if a[i-1]["slots"] == []:
            del a[i-1]
        i -= 1
    return a
def jsonActToCued(a=[],code=None,deleted=None):
    #print(a)
    
    
    finalDict = {'a':[],'d':[],'m':[]}
    if a != []:
        dictList = list(range(len(a)))
    elif a == []:
        print(finalDict)
        return finalDict
    
    if(deleted):
            finalDict["d"] = tuple(jsonItemToCued(deleted))
            
    if not code:
        print(finalDict)
        return finalDict
    
    #print("function result:")
    #print(jsonItemToCued(a))
    dictList = (tuple(jsonItemToCued(a)))
    #print("dictList")
    #print(dictList)
        
    if(len(dictList) != 0):
        if(len(a) > 1):
            [finalDict[code]] = [dictList]
        else:
            finalDict[code] = [dictList]
    print(finalDict)
    return finalDict

def main():
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
        with open("part2.py", 'w') as outputfile:
            print("Session:"+ str(fName))
            outputfile.write("Session:"+ str(fName))
                    # iterate through each dialog
            curCam = []
            prevCam = []
            prevSlots = []
            # iterate through each dialog turn; 
            # call is the data from the actual interaction (log.json)
            # label is the data provided by after dialog labeling (label.json)
            for turn,turnLabel in zip(call["turns"],label["turns"]) :
                
                #print (jsonToCued(turn["output"]["dialog-acts"]))
                curCam = turnLabel["semantics"]["cam"]
                #print("Current: " + str(curCam))
                #print("Previous: " + str(prevCam))
                
                a = turnLabel["semantics"]["json"]
                a = removeEmpty(a)
                #print("Slots: " + str(a) +"\n")
                curSlots = list([] for i in range(len(a)) if a[i]["slots"] != [])
                for i in range(len(a)):
                    #print("Current Slot: ")
                    #print(a[i]["slots"])
                    if a[i]["slots"] != []:
                     #   print("adding")
                        [curSlots[i]] = a[i]["slots"] 
                if(curCam == prevCam):
                    outputfile.write(str(jsonActToCued()))
                    break
                
                dupesRemoved = [slot for slot in curSlots if slot not in prevSlots]
                #print("cur:" + str(curSlots))
                #print("dup:" + str(dupesRemoved))
                if "reqalt" in curCam:
                    outputfile.write(str(jsonActToCued(dupesRemoved,"m")))
                elif "dontcare" in curCam:
                    outputfile.write(str(jsonActToCued(dupesRemoved,"m")))
                elif "inform" in curCam:     
                    outputfile.write(str(jsonActToCued(dupesRemoved,"a")))
                elif "request" in curCam: 
                    if "request" in prevCam: #delete previous request and replace it with new one
                        outputfile.write(str(jsonActToCued(dupesRemoved,"a",prevSlots)))
                    else:
                        outputfile.write(str(jsonActToCued(dupesRemoved,"a")))
                else:
                    outputfile.write(str(jsonActToCued()))
                    
                prevCam = curCam
                prevSlots = curSlots
                #print("+++")
                
               
                
            
            
if __name__ == '__main__':
    main()
