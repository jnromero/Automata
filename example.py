import Automaton

#TFT
start=0
states={0: {'action': 'C', 'C': 0, 'D': 1},
1: {'action': 'D', 'C': 0, 'D': 1}}
actions=["C","D"]
A1=Automaton.Automaton(start,states,actions)

#Alternator
start=0
states={0: {'action': 'C', 'C': 1, 'D': 1},
1: {'action': 'D', 'C': 0, 'D': 0}}
actions=["C","D"]
A2=Automaton.Automaton(start,states,actions)

#payoffs
#{"player1Action1":{"player2Action1":[pay1_11,pay2_11],"player2Action2":[pay1_12,pay2_12]}....}
pays={"C":{"C":[3,3],"D":[1,4]},"D":{"C":[4,1],"D":[2,2]}}


print "Show the actions from this automaton pair"
print Automaton.getHistory(A1,A2,10)
print
print "Show the payoff history from this pair"
print Automaton.getPayoffHistory(A1,A2,10,pays)
print 
print "Show the average payoffs"
print Automaton.getPayoffs(A1,A2,10,pays)


