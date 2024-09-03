fpInput='/home/hungphd/Desktop/HelpTu_Links_v1/all.txt'
fpOutput='/home/hungphd/Desktop/HelpTu_Links_v1/all_filter.txt'
f1=open(fpInput,'r')
arrInputs=f1.read().split('\n')
f1.close()
dictInput={}
for item in arrInputs:
    arrTab=item.split('\t')
    key=arrTab[0]
    val='\t'.join(arrTab[1:])
    if key not in dictInput.keys():
        dictInput[key]=item

lstOutputs=[]
for key in dictInput.keys():
    lstOutputs.append(dictInput[key])
f1=open(fpOutput,'w')
f1.write('\n'.join(lstOutputs))
f1.close()