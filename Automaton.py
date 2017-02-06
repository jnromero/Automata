import random
import math
import time


class Automaton(object):
  __slots__ = ('currentState','states','actions','start','string')
  def __init__(self,start,states,actions):
    self.start=start
    self.currentState=start
    self.states=states
    self.actions=actions
    self.string="-1"

  def makeChoice(self):
    #these are relatively slow
    return self.states[self.currentState]['action']

  def transition(self,otherAction):
    #these are relatively slow
    self.currentState=self.states[self.currentState][otherAction]

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

    if len(visited)!=len(self.states):
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
    #http://www.cs.engr.uky.edu/~lewis/essays/compilers/min-fa.html?????
    partition={}
    partitionState={}
    j=0
    for k in self.states:
      thisAction=self.states[k]['action']
      if thisAction not in partition:
        partition[thisAction]={}
        partition[thisAction]['states']=[]
        partition[thisAction]['id']=j
        j=j+1
      partition[thisAction]['states'].append(k)
      partitionState[k]=partition[thisAction]['id']
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
    #reorders to unique automaton
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
      self.string+="%s"%(self.states[k]['action'])
      for action in self.actions:
        self.string+="%s"%(self.states[k][action])
    


def generateRandomAutomaton(numberStates,actions):
  start=random.choice(range(numberStates))
  states={}
  for k in range(numberStates):
    states[k]={}
    states[k]['action']=random.choice(actions)
    for a in actions:
      states[k][a]=random.choice(range(numberStates))
  thisA=Automaton(start,states,actions)
  thisA.clean()
  return thisA


def getHistory(A1,A2,periods):
  A1.currentState=A1.start
  A2.currentState=A2.start
  history=[]
  for p in xrange(periods):
    action1=A1.states[A1.currentState]['action']
    action2=A2.states[A2.currentState]['action']
    #tuple is faster
    history.append((action1,action2))

    A1.currentState=A1.states[A1.currentState][action2]
    A2.currentState=A2.states[A2.currentState][action1]

  return history


def getPayoffs(A1,A2,periods,payoffs):
  A1.currentState=A1.start
  A2.currentState=A2.start
  totalPay1=0
  totalPay2=0
  for p in xrange(periods):
    #manual choices are faster
    action1=A1.states[A1.currentState]['action']
    action2=A2.states[A2.currentState]['action']

    totalPay1+=payoffs[action1][action2][0]
    totalPay2+=payoffs[action1][action2][1]

    #manual transitions are faster
    A1.currentState=A1.states[A1.currentState][action2]
    A2.currentState=A2.states[A2.currentState][action1]

  return (float(totalPay1)/periods,float(totalPay2)/periods)


def getPayoffHistory(A1,A2,periods,payoffs):
  A1.currentState=A1.start
  A2.currentState=A2.start
  payoffHistory=[]
  for p in xrange(periods):

    #manual choices are faster
    action1=A1.states[A1.currentState]['action']
    action2=A2.states[A2.currentState]['action']

    payoffHistory.append(payoffs[action1][action2])

    #manual transitions are faster
    A1.currentState=A1.states[A1.currentState][action2]
    A2.currentState=A2.states[A2.currentState][action1]

  return payoffHistory

def testFunctions():
  t=time.time()
  for k in range(100000):
    # getHistory(A1,A2,10)
    getPayoffs(A1,A2,10,pays)
    #generateRandomAutomaton(8,['C',"D"])
  print time.time()-t

