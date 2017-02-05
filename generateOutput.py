# from Automaton import Automaton
import random
import bitarray
import pickle
import itertools
filename="3-states_3-actions.pickle"
file = open(filename,'rb')
data=pickle.load(file)
file.close() 

def binToInt(b):
  if b=="00":
    out=0
  elif b=="01":
    out=1
  elif b=="10":
    out=2
  elif b=="11":
    out=3
  return out

info={}
for k in data:
  thisString="%s"%(k.to01())
  print thisString
  converted=""
  for j in range(len(thisString)/2):
    converted+="%s"%(binToInt(thisString[2*j:2*j+2]))
  print converted
  start=converted[0]
  length=len(converted)
  actions=""
  for n in range((length-1)/4):
    actions+="%s"%(converted[1+4*n])

  state0transitions=converted[2:5]
  this="%s%s%s"%(actions,length,state0transitions)
  if this not in info:
    info[this]=[]
  info[this].append(converted)
print info
allTitles=[]
for k in info:
  filename="output/%s.pickle"%(k)
  file = open(filename,'wb')
  pickle.dump(info[k],file)
  file.close() 
  allTitles.append(k)
filename="output/allTitles.pickle"
file = open(filename,'wb')
pickle.dump(allTitles,file)
file.close() 

# #convert automaton string to bit array
# automatonString=""
# automatonString+=getBin(int(thisA.start))
# minimizedStates=len(thisA.states)
# for s in range(minimizedStates):
#   automatonString+=getBin(thisA.states[s]['action'])
#   for a in range(numberActions):
#     automatonString+=getBin(int(thisA.states[s][a]))
# thisBit=bitarray.bitarray(automatonString)

