# from Automaton import Automaton
import random
import pickle
import itertools

class Automaton(object):
  __slots__ = ('states','start')
  def __init__(self,start,states):
    self.start=start
    self.states=states




def compareTwoAutomata(A1,A2,actions,totalSequences):
  currentDist={}
  #sames={}
  diffs={}
  tC={}
  tD={}
  tE={}
  start="%s%s"%(A1.start,A2.start)
  for s1 in A1.states:
    for s2 in A2.states:
      stateName="%s%s"%(s1,s2)
      # sames[stateName]=int(A1.states[s1]['action']==A2.states[s2]['action'])
      diffs[stateName]=int(A1.states[s1]['action']!=A2.states[s2]['action'])
      tC[stateName]="%s%s"%(A1.states[s1]["C"],A2.states[s2]["C"])
      tD[stateName]="%s%s"%(A1.states[s1]["D"],A2.states[s2]["D"])
      tE[stateName]="%s%s"%(A1.states[s1]["E"],A2.states[s2]["E"])
      currentDist[stateName]=0
  dif=0
  total=0
  currentDist[start]=totalSequences
  for j in range(10):
    newDist={}
    for k in currentDist:
      newDist[k]=0
    for k in currentDist:
      if currentDist[k]>0:
        dif+=currentDist[k]*diffs[k]
        newDist[tC[k]]+=currentDist[k]/len(actions)
        newDist[tD[k]]+=currentDist[k]/len(actions)
        newDist[tE[k]]+=currentDist[k]/len(actions)
    currentDist=newDist
    # if dif>10000:
    #   break
  return dif







# # import itertools
# # sim=0
# # tot=0
# # for k in range(1000):
# #   for seq in itertools.product('CDE', repeat=9):
# #     if A1.currentState==A2.currentState:
# #       sim+=1
# #     tot+=1
# #     for a in seq:
# #       A1.transition(a)
# #       A2.transition(a)
# #       if A1.currentState==A2.currentState:
# #         sim+=1
# #       tot+=1
# #   print sim
# #   print tot
# # raw_input() 
import time
startTime=time.time()
sequenceLength=3*3*3*3*3*3*3*3*3
start=0
states1={0:{"action":"C","C":0,"D":2,"E":0},1:{"action":"D","C":1,"D":1,"E":0},2:{"action":"E","C":0,"D":2,"E":1}}
states2={0:{"action":"C","C":2,"D":0,"E":1},1:{"action":"D","C":2,"D":0,"E":1},2:{"action":"E","C":1,"D":2,"E":0}}
states1={0:{"action":"C","C":2,"D":0,"E":1},1:{"action":"C","C":2,"D":0,"E":1},2:{"action":"C","C":1,"D":2,"E":0}}
states2={0:{"action":"D","C":2,"D":0,"E":1},1:{"action":"D","C":2,"D":0,"E":1},2:{"action":"D","C":1,"D":2,"E":0}}
for k in range(100):
  A1=Automaton(start,states1)
  A2=Automaton(start,states2)
  x=compareTwoAutomata(A1,A2,["C","D","E"],sequenceLength)
print x
print time.time()-startTime