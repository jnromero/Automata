from __future__ import print_function,division,absolute_import   
from Automaton import Automaton
import bitarray
import pickle
import itertools

class Automaton(object):
  __slots__ = ('currentState','states','actions','start','string')
  def __init__(self,start,states,actions):
    self.start=start
    self.currentState=start
    self.states=states
    self.actions=range(actions)
    self.string="-1"
  def makeChoice(self):
    return self.states[self.currentState]['action']
  def transition(self,input):
    if len(input)==1:
      this=input[0]
    self.currentState=self.states[self.currentState][this]

  def clean(self):
    self.eliminateNonVisited()
    self.minimizeAutomaton()
    self.renameAndReorderStates()
    self.getString()

  def eliminateNonVisited(self):
    #find states that are visited
    visited=[self.start]
    current=[self.start]
    while len(current)>0:
      nextStates=[]
      for j in current:
        for otherAction in self.actions:
          nextState=self.states[j][otherAction]
          if nextState not in nextStates and nextState not in visited:
            nextStates.append(nextState)
            visited.append(nextState)
      current=nextStates[:]

    #find states that are not visited
    notVisited=[]
    for state in self.states:
      if state not in visited:
        notVisited.append(state)

    #delete non visited states
    for state in notVisited:
      del self.states[state]

  def getFitness(self,history,playerIndex):
    #is playerIndex using this automaton based on the history? 
    if len(history)>0:
      fitness={}
      for currentState in self.states:
        if history[-1][playerIndex]==self.states[currentState]['action']:
          fitness[currentState]=0
          nextStates=[currentState]
          k=1
          for k in range(2,len(history)+1):
            myPlay=history[-k][playerIndex]
            #right now this just works for two player automata, have to think about how to change to allow for more general.
            otherPlay=history[-k][1-playerIndex]
            possibleStates=[]
            for state in self.states:
              if self.states[state]['action']==myPlay and self.states[state][otherPlay] in nextStates:
                possibleStates.append(state)
            nextStates=possibleStates[:]
            if len(nextStates)==0:
              out=k-1
              break
          if len(nextStates)>0:
            out=k
          fitness[currentState]=out
        else:
          fitness[currentState]=0
      bestFitness=-1
      bests=[]
      for k in fitness:
        if fitness[k]>bestFitness:
          bestFitness=fitness[k]
          bests=[k]
        elif fitness[k]==bestFitness:
          bests.append(k)
      bestState=random.choice(bests)

      #MAKE SURE TO GET STATE THAT I WILL BE IN NEXT PERIOD, not this period. 
      othersLastChoice=history[-1][1-playerIndex]
      nextPeriodState=self.states[bestState][othersLastChoice]
    else:
      nextPeriodState=random.choice([x for x in self.states])
      bestFitness=0
    bestFitness=min(10000,bestFitness)#maximum fitness
    return nextPeriodState,bestFitness


  def minimizeAutomaton(self):
    partition={}
    partitionState={}
    j=0
    for k in self.states:
      if self.states[k]['action'] not in partition:
        partition[self.states[k]['action']]={}
        partition[self.states[k]['action']]['states']=[]
        partition[self.states[k]['action']]['id']=j
        j=j+1
      partition[self.states[k]['action']]['states'].append(k)
      partitionState[k]=partition[self.states[k]['action']]['id']
    while 3<4:
      j=0
      partitionNew={}
      partitionStateNew={}
      for k in self.states:
        #this=(partitionState[k],partitionState[self.states[k]['C']],partitionState[self.states[k]['D']],partitionState[self.states[k]['E']])
        this=(partitionState[k],)
        for a in self.actions:
          this+=(partitionState[self.states[k][a]],)
        if this not in partitionNew:
          partitionNew[this]={}
          partitionNew[this]['states']=[]
          partitionNew[this]['id']=j
          j=j+1
        partitionNew[this]['states'].append(k)
        partitionStateNew[k]=partitionNew[this]['id']
      if len(partitionNew)==len(partition):
        break
      partition=partitionNew
      partitionState=partitionStateNew

    replacements={}
    for k in partition:
      these=partition[k]['states']
      if len(these)>0:
        for j in these[1:]:
          #replace state j with these[0]
          replacements[j]=these[0]

    #delete redundant states
    for k in replacements:
      del self.states[k]
    #change transitions to cover redundant states. 
    for k in self.states:
      for action in self.actions:
        if self.states[k][action] in replacements:
          self.states[k][action]=replacements[self.states[k][action]]

    #change start state and currentstate
    if self.start in replacements:
      self.start=replacements[self.start]
      self.currentState=self.start

  def renameAndReorderStates(self):
    toCheck=[self.start]
    order=[]
    while len(toCheck)>0:
      thisState=toCheck.pop(0)
      order.append(thisState)
      for action in self.actions:
        nextState=self.states[thisState][action]
        if nextState not in order and nextState not in toCheck:
          toCheck.append(nextState)
    j=0
    reorder={}
    for k in order:
      reorder[k]=j
      j=j+1

    newStates={}
    for oldState in self.states:
      newState=reorder[oldState]
      newStates[newState] = self.states[oldState]
      for action in self.actions:
        newStates[newState][action]=reorder[newStates[newState][action]]
    self.states=newStates
    self.start=reorder[self.start]
    self.currentState=self.start

  def getString(self):
    self.string="%s"%(self.start)
    for k in self.states:
      self.string=self.string+"%s"%(self.states[k]['action'])
      for action in self.actions:
        self.string=self.string+"%s"%(self.states[k][action])
    



def generateRandomAutomaton(numberStates,actions):
  start=random.choice(range(numberStates))
  states={}
  for k in range(numberStates):
    this={}
    this['action']=random.choice(actions)
    for a in actions:
      this[a]=random.choice(range(numberStates))
    states[k]=this
  thisA=Automaton(start,states,actions)
  thisA.clean()
  return thisA


def getBin(number):
  if number==0:
    out='00'
  elif number==1:
    out='01'
  elif number==2:
    out='10'
  elif number==3:
    out='11'
  return out



def getMinimal(numberActions,numberStates):
  #this only works for 4 states or less and 4 actions or less because of the transformation to binary
  totalLength=1+numberStates*(numberActions+1)
  filename="%s-states_%s-actions.pickle"%(numberStates,numberActions)
  allAutomata={}
  #start state - number of states - 1
  # actions - number of actions - number of states
  # transitions - number of states -  (number of actions)*(number of states) 
  lengthOfActionPart=numberStates
  lengthOfStatePart=numberStates*numberActions+1

  count=0
  for j in itertools.product(range(numberActions), repeat=lengthOfActionPart):
    #make sure the actions are increasing to reduce redundancy keep 0012 eliminate 0210
    ordered=1
    for x in range(len(j)-1):
      if j[x]>j[x+1]:
        ordered=0
    allEqual=1
    for x in range(len(j)-1):                             
      if j[x]!=j[x+1]:
        allEqual=0
    if ordered==1 and allEqual==0:
      for k in itertools.product(range(numberStates), repeat=lengthOfStatePart):
        states={}
        start=k[0]
        for state in range(numberStates):
          this={}
          this['action']=j[state]
          for l in range(numberActions):
            this[l]=k[1+l+state*numberActions]
          states[state]=this
        thisA=Automaton(start,states,numberActions)
        thisA.eliminateNonVisited()
        thisA.minimizeAutomaton()
        thisA.renameAndReorderStates()


        #create a string to make seperate lists to make things more effienct for checking if automataon is already there or not.
        thisString=""
        #actions in states
        thisString+="".join(["%s"%(thisA.states[x]['action']) for x in thisA.states])
        #start state
        thisString+="%s"%(thisA.start)
        #transitions for each action from state 0 (this will always be there)
        for a in range(numberActions):
          thisString+="%s"%(thisA.states[0][a])

        #convert automaton string to bit array
        automatonString=""
        automatonString+=getBin(int(thisA.start))
        minimizedStates=len(thisA.states)
        for s in range(minimizedStates):
          automatonString+=getBin(thisA.states[s]['action'])
          for a in range(numberActions):
            automatonString+=getBin(int(thisA.states[s][a]))
        thisBit=bitarray.bitarray(automatonString)

        if thisString not in allAutomata:
          allAutomata[thisString]=[]
        if thisBit not in allAutomata[thisString]:
          allAutomata[thisString].append(thisBit)
          count+=1
          print(count,k)


  data=[]
  for a in allAutomata:
    data+=allAutomata[a]
  file = open(filename,'wb')
  pickle.dump(data,file)
  file.close() 



def timeTest():
  #for testing
  import time
  start=time.time()
  for k in range(100000):
    generateRandomAutomaton(8,['C',"D"])
  print(time.time()-start)

timeTest()

import time
start=time.time()
getMinimal(3,3)
print(time.time()-start)