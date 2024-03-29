import random
from scipy.stats import truncnorm
import numpy as np
from sys import exit
import plotly
import plotly.graph_objs as go



##the simulation environment parameters
rounds = 100 #number of rounds per session
runs = 10 #number of sessions
I = 2 # 2 subjects
J=100  #number of alternatives in the remembered strategy set
pex=0.01 #experimentation probability
theta=0.01 #experimentation sd

#define r to be the recommendation
#note: is this program, 0 is defined to be D(efect), and 1 is C(operate)
#note: the expression for calculating payoff: 9b_2 + 3b_1 - 5b_1*b_2
#note: for the chicken game, mixed-strat Nash yield (5.4, 5.4)
#note: the NASH RECCOMENDATION correlated eqm yield (6,6)
#note: in this program, the NASH RECOMMENDATION is used, i.e. (D,C) and (C,D) are recommended w/p 1/2 each










## IEL PROCEDURES
############################################################################################################################
#initialization of remembered strategy set
def randominitialize(I, J):
    W=[] #initial utility
    St=[] #initial remembered strategy set 
    
    for i in range(I): #for each firm
        temp=[2]*len(range(J)) #as J is the length of the set #choice of 2 is arbitrary
        W.append(temp)
        
        
    for i in range(I):
        Sit=[]
        
        for j in range(J):
            Sit.append([random.uniform(0,1),random.randint(0,1)]) # Sit contains J elements draw form the strategy set [S_lower,S_upper]
        St.append(Sit)  #St contains I elements, each belongs to a firm
        
    return St, W  #W=[[Wi],..,[WI]], similar for St

#strategy selection in a strategy set
def selectionfori(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities): #this zip() return a pair of tuples where 1st element in each are paired and so on
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item

#ASSIGN PROBABILITY CORRESPONDING TO PROFIT
def choiceprobabilitiesfori(profits):  #choiceprobabilitiesfori(W[i])
    choicepiti=[]
    sumw=sum(profits)
    for j in range(J):
        if sumw == 0:
            choicepiti.append(1/J)
        else:
            choicepiti.append(profits[j]/float(sumw))
    return choicepiti

##EXPERIMENTATION
def Vexperimentationfori(strategyset):
    for j in range(J):
        if random.uniform(0, 1) < pex:
            centers = strategyset[j][0]
            strategyset[j][0] = np.random.normal(centers, theta)

            strategyset[j][1] = (strategyset[j][1] + 1)%2
    return strategyset

##CALCULATING FOReGONE PROFIT ##UNFINISHED
def foregoneprofit(strategy, past_actions, i, reccomendation):
    past_actions=list(past_actions) #element a[len(a)-1] contains decision of 2 players at time t-1
    payoff=strategy[0]*(9*past_actions[(i+1)%2] + 3*reccomendation[i]-5*reccomendation[i]*past_actions[(i+1)%2]) + (1-strategy[0])*(9*past_actions[(i+1)%2] + 3*strategy[1]-5*strategy[1]*past_actions[(i+1)%2])           
    return payoff                                  #9b_2 + 3b_1 - 5b_1*b_2



def updateWfori(Set,past_actions, i, reccomendation): #update utility set #updateWfori(St[i], a[len(a)-1], i, r)
    W=[]  #note: Set is the remembered strategy set of i
          #note: thus Set[j] is a particular strategy
    for j in range(J):
        W.append(foregoneprofit(Set[j],past_actions, i, reccomendation))
        #W.append(10-Set[j])
    return W


#after experimentation for St[i] and corresponding W[i],
def replicatefori(strategyset, utilities):  #(St[i], W[i]) = replicatefori(St[i], W[i])
    newS=[0]*J
    newW=[0]*J
    for j in range(J):
        j1=random.randrange(J)
        j2=random.randrange(J)
        newS[j]=strategyset[j2]
        newW[j]=utilities[j2]
        if utilities[j1]>utilities[j2]:
            newS[j]=strategyset[j1]
            newW[j]=utilities[j1]
    return newS, newW


############################################################################################################################











##SIMULATION FUNCTION
############################################################################################################################
def simulation_NashReccommendation(rounds, runs, I, J, pex, theta):

    SelectedStrategy = []
    ave_SelectedStrategy_allrun_i0 = []
    payoff_allrun_i0 = []
    payoff_allrun_i1 = []

    Nash_outcome_frequency_allrun = []
    folo_frequency_i0_allrun = []
    folo_frequency_i1_allrun = []
    both_folo_frequency_allrun = []
    
    for sims in range(runs):
        print("RUN", sims, "--------------------------------------------------------------------------")
        random.seed()
        S = []  # stores strategy sets for each run
        a = []  # stores all actions for a run
        a_folo_ornot = [] # stores all actions (folo or not folo) for a run
            
    
    
        [St, W] = randominitialize(I, J)
    
        for t in range(rounds):
            R = ([0,1],[1,0]) # create a list for possible Recommendations r
            r = R[random.randint(0,1)]  #now the recommendation is randomly chosen from R
            
            at = []  #  store pair of actions (e.g. 0 or 1) at round t
            at_folo_ornot = [] # store pair of actions (e.g. folo or not folo) at round t
            st = []  #  store pair of strategies at round t
            #print("time t =", t)
            #print("remembered strategy set of i=0:", St[0])
            #print("remembered strategy set of i=1:", St[1])
            

        
            if t==0:
                for i in range(I):
                    p = choiceprobabilitiesfori(W[i])
                    if random.uniform(0,1) < selectionfori(St[i],p)[0]:
                        decision = r[i]
                        folo_ornot = "folo"
                    else:
                        decision = selectionfori(St[i],p)[1] #[1] here since nf is the second element
                        folo_ornot = "not"             #note: selectionfori() yield an element in the strategy set
                    at.append(decision) #note: at is a pair-of-decision at time t
                    at_folo_ornot.append(folo_ornot)
                    st.append(selectionfori(St[i],p))
                #print(selection_probability)
                S.append(st)
                a.append(at) #note: a is a list of pair-of-decision of 2 players
                a_folo_ornot.append(at_folo_ornot)
            else:
                for i in range(I):
                    St[i] = Vexperimentationfori(St[i])

                    W[i] = updateWfori(St[i], a[len(a)-1], i, r) #(strategy, past_actions, player_name)
                    (St[i], W[i]) = replicatefori(St[i], W[i])
                for i in range(I):
                    p = choiceprobabilitiesfori(W[i])
                    if random.uniform(0,1) < selectionfori(St[i],p)[0]:
                        decision = r[i]
                        folo_ornot = "folo"
                    else:
                        decision = selectionfori(St[i],p)[1]
                        folo_ornot = "not"

                    at.append(decision)
                    at_folo_ornot.append(folo_ornot)
                    st.append(selectionfori(St[i],p))
                   
                S.append(st)
                a.append(at)
                a_folo_ornot.append(at_folo_ornot)
        #print("The game play of RUN", sims, "is",a)
        #print("Alternatively, the game play of RUN", sims, "is", a_folo_ornot)
        

        #count the folo or not of each player
        folo_frequency_i0 = 0
        folo_frequency_i1 = 0
        both_folo_frequency = 0
        for t in range(49,len(a_folo_ornot)):
            if a_folo_ornot[t][0] == "folo":
                folo_frequency_i0 += 1
            if a_folo_ornot[t][1] == "folo":
                folo_frequency_i1 += 1
            if a_folo_ornot[t] == ["folo", "folo"]:
                both_folo_frequency += 1
        folo_frequency_i0_allrun.append(folo_frequency_i0)   
        folo_frequency_i1_allrun.append(folo_frequency_i1)
        both_folo_frequency_allrun.append(both_folo_frequency)   

                
        
            
    

        
        #count the Nash outcome frequency
        Nash_frequency = 0
        for t in range(len(a)):
            if a[t] == [0,1] or a[t] == [1,0]:
                Nash_frequency += 1
        #print("Nash outcome frequency out of", rounds, "round s", Nash_frequency)
        Nash_outcome_frequency_allrun.append(Nash_frequency)

        #calculating payoff for each player
        payoff_i0 = []
        for  t in range(len(a)):
            payoff_i0_roundt = 9*a[t][1] + 3*a[t][0] - 5*a[t][0]*a[t][1]
                        #9b_2 + 3b_1 - 5b_1*b_2
            payoff_i0.append(payoff_i0_roundt)
        #print("agent i=0 payoff of this RUN over", rounds, "rounds is", payoff_i0)
        #print("agent i=0 average payoff of this RUN is", np.mean(payoff_i0), end="\n")
        #print()
        #print()
        
        payoff_allrun_i0.append(payoff_i0)

        payoff_i1 = []
        for z in range(len(a)):
            payoff_i1_roundt = 9*a[z][0] + 3*a[z][1] - 5*a[z][1]*a[z][0]
                        #9b_2 + 3b_1 - 5b_1*b_2
            payoff_i1.append(payoff_i1_roundt)
        #print("agent i=1 payoff of this RUN over", rounds, "rounds is", payoff_i1)
        #print("agent i=1 average payoff of this RUN is", np.mean(payoff_i1), end="\n")
        #print()
        #print()
        
        payoff_allrun_i1.append(payoff_i1)

        

            
        
        SelectedStrategy.append(S)
        #print(SelectedStrategy)
    for t in range(rounds):
        round_ave_allrun_i0 = np.mean(list(x[t][0][0] for x in SelectedStrategy))
        ave_SelectedStrategy_allrun_i0.append(round_ave_allrun_i0)
    #print("the round average following probability of all run is:", ave_SelectedStrategy_allrun_i0)

    print("SUMMARY ________________________________________________________________")
    print("CORRELATED EQM IN CHICKEN GAME (NASH RECOMMENDATION TREATMENT)")
    print("")
    print("rounds=", rounds)
    print("runs=", runs)
    print("# of agent =", I)
    print("#number of alternatives in the remembered strategy set=", J)
    print("#experimentation probability=", pex)
    print("#experimentation std=", theta)

    #calculating average payoff of all round over all runs    
    ave_payoff_allrun_i0 = np.mean(payoff_allrun_i0)
    ave_payoff_allrun_i1 = np.mean(payoff_allrun_i1)
    sd0 = np.std(payoff_allrun_i0)
    sd1 = np.std(payoff_allrun_i1)
    print("-----------------------------------------------------------------------------\n","THE AVERAGE PAYOFF OF AGENT i=0 OVER", runs, "runs is", ave_payoff_allrun_i0, "with std", sd0)        
    print("THE AVERAGE PAYOFF OF AGENT i=1 OVER", runs, "runs is", ave_payoff_allrun_i1, "with std", sd1)        

    #calculating average payoff of last 50% rounds over all runs 
    ave_payoff_lasthalfround_i0 = np.mean(payoff_allrun_i0[int(round(0.5*len(payoff_allrun_i0))):len(payoff_allrun_i0)])
    ave_payoff_lasthalfround_i1 = np.mean(payoff_allrun_i1[int(round(0.5*len(payoff_allrun_i1))):len(payoff_allrun_i1)])
    sd00 = np.std(payoff_allrun_i0[int(round(0.5*len(payoff_allrun_i0))):len(payoff_allrun_i0)])
    sd11 = np.std(payoff_allrun_i1[int(round(0.5*len(payoff_allrun_i1))):len(payoff_allrun_i1)])

    print("-----------------------------------------------------------------------------\n","THE AVERAGE PAYOFF OF AGENT i=0 OVER last 50% round of all", runs, "runs is", ave_payoff_lasthalfround_i0, "with std", sd00)        
    print("THE AVERAGE PAYOFF OF AGENT i=1 OVER last 50% round of all", runs, "runs is", ave_payoff_lasthalfround_i1, "with std", sd11)        

    print("-----------------------------------------------------------------------------")  
    print("Nash outcome frequency over", runs ,"runs (out of",rounds, "rounds) is",Nash_outcome_frequency_allrun)
    print("with mean", np.mean(Nash_outcome_frequency_allrun), "(note: Duffy, Feltovich (2010)'s number is 57.1%)")

    print("-----------------------------------------------------------------------------")  
    print("FOLLOW frequency of i=0 over", runs, "runs(out of last 50% round =",0.5*rounds, "rounds) is", folo_frequency_i0_allrun, "mean:", np.mean(folo_frequency_i0_allrun))
    print("FOLLOW frequency of i=1 over", runs, "runs(out of last 50% round =",0.5*rounds, "rounds) is", folo_frequency_i1_allrun, "mean:", np.mean(folo_frequency_i1_allrun))
    print("BOTH FOLLOWING over", runs, "runs(out of last 50% round =",0.5*rounds, "rounds) is", both_folo_frequency_allrun, "mean:", np.mean(both_folo_frequency_allrun))




    print("")
    print("")
    print("END OF SUMMARY_______________________________________________________________")
                
    trace0 = go.Scatter(
        x = list(range(rounds)),
        y = list(ave_SelectedStrategy_allrun_i0),
        mode = 'lines+markers',
        name = 'lines'
    )
    layout = go.Layout(
        title="",
        width=800,
        height=600,
        xaxis=dict(
            title='period',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='round average probability of following the reccommendation of agent i=0',
            nticks=10,
            range=[0,1],
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    data = [trace0]
    figure = go.Figure(data=data,layout=layout)
    #plotly.offline.plot(figure, filename='line-mode.html')

#########################################################################################################

#########################################################################################################

#########################################################################################################

#######################################################################################################################

def simulation_GoodReccommendation(rounds, runs, I, J, pex, theta):

    SelectedStrategy = []
    ave_SelectedStrategy_allrun_i0 = []
    payoff_allrun_i0 = []
    payoff_allrun_i1 = []

    Nash_outcome_frequency_allrun = []
    folo_frequency_i0_allrun = []
    folo_frequency_i1_allrun = []
    both_folo_frequency_allrun = []
    
    for sims in range(runs):
        #print("RUN", sims, "--------------------------------------------------------------------------")
        random.seed()
        S = []  # stores strategy sets for each run
        a = []  # stores all actions for a run
        a_folo_ornot = [] # stores all actions (folo or not folo) for a run
            
    
    
        [St, W] = randominitialize(I, J)
    
        for t in range(rounds):
            R = ([0,1],[1,0],[1,1]) # create a list for possible Recommendations r
            r = R[random.randint(0,2)]  #now the recommendation is randomly chosen from R
            
            at = []  #  store pair of actions (e.g. 0 or 1) at round t
            at_folo_ornot = [] # store pair of actions (e.g. folo or not folo) at round t
            st = []  #  store pair of strategies at round t
            #print("time t =", t)
            #print("remembered strategy set of i=0:", St[0])
            #print("remembered strategy set of i=1:", St[1])
            

        
            if t==0:
                for i in range(I):
                    p = choiceprobabilitiesfori(W[i])
                    if random.uniform(0,1) < selectionfori(St[i],p)[0]:
                        decision = r[i]
                        folo_ornot = "folo"
                    else:
                        decision = selectionfori(St[i],p)[1] #[1] here since nf is the second element
                        folo_ornot = "not"             #note: selectionfori() yield an element in the strategy set
                    at.append(decision) #note: at is a pair-of-decision at time t
                    at_folo_ornot.append(folo_ornot)
                    st.append(selectionfori(St[i],p))
                #print(selection_probability)
                S.append(st)
                a.append(at) #note: a is a list of pair-of-decision of 2 players
                a_folo_ornot.append(at_folo_ornot)
            else:
                for i in range(I):
                    St[i] = Vexperimentationfori(St[i])

                    W[i] = updateWfori(St[i], a[len(a)-1], i, r) #(strategy, past_actions, player_name)
                    (St[i], W[i]) = replicatefori(St[i], W[i])
                for i in range(I):
                    p = choiceprobabilitiesfori(W[i])
                    if random.uniform(0,1) < selectionfori(St[i],p)[0]:
                        decision = r[i]
                        folo_ornot = "folo"
                    else:
                        decision = selectionfori(St[i],p)[1]
                        folo_ornot = "not"

                    at.append(decision)
                    at_folo_ornot.append(folo_ornot)
                    st.append(selectionfori(St[i],p))
                   
                S.append(st)
                a.append(at)
                a_folo_ornot.append(at_folo_ornot)
        #print("The game play of RUN", sims, "is",a)
        #print("Alternatively, the game play of RUN", sims, "is", a_folo_ornot)
        

        #count the folo or not of each player
        folo_frequency_i0 = 0
        folo_frequency_i1 = 0
        both_folo_frequency = 0
        for t in range(49,len(a_folo_ornot)):
            if a_folo_ornot[t][0] == "folo":
                folo_frequency_i0 += 1
            if a_folo_ornot[t][1] == "folo":
                folo_frequency_i1 += 1
            if a_folo_ornot[t] == ["folo", "folo"]:
                both_folo_frequency += 1
        folo_frequency_i0_allrun.append(folo_frequency_i0)   
        folo_frequency_i1_allrun.append(folo_frequency_i1)
        both_folo_frequency_allrun.append(both_folo_frequency)   

                
        
            
    

        
        #count the Nash outcome frequency
        Nash_frequency = 0
        for t in range(len(a)):
            if a[t] == [0,1] or a[t] == [1,0]:
                Nash_frequency += 1
        #print("Nash outcome frequency out of", rounds, "round s", Nash_frequency)
        Nash_outcome_frequency_allrun.append(Nash_frequency)

        #calculating payoff for each player
        payoff_i0 = []
        for  t in range(len(a)):
            payoff_i0_roundt = 9*a[t][1] + 3*a[t][0] - 5*a[t][0]*a[t][1]
                        #9b_2 + 3b_1 - 5b_1*b_2
            payoff_i0.append(payoff_i0_roundt)
        #print("agent i=0 payoff of this RUN over", rounds, "rounds is", payoff_i0)
        #print("agent i=0 average payoff of this RUN is", np.mean(payoff_i0), end="\n")
        #print()
        #print()
        
        payoff_allrun_i0.append(payoff_i0)

        payoff_i1 = []
        for z in range(len(a)):
            payoff_i1_roundt = 9*a[z][0] + 3*a[z][1] - 5*a[z][1]*a[z][0]
                        #9b_2 + 3b_1 - 5b_1*b_2
            payoff_i1.append(payoff_i1_roundt)
        #print("agent i=1 payoff of this RUN over", rounds, "rounds is", payoff_i1)
        #print("agent i=1 average payoff of this RUN is", np.mean(payoff_i1), end="\n")
        #print()
        #print()
        
        payoff_allrun_i1.append(payoff_i1)

        

            
        
        SelectedStrategy.append(S)
        #print(SelectedStrategy)
    for t in range(rounds):
        round_ave_allrun_i0 = np.mean(list(x[t][0][0] for x in SelectedStrategy))
        ave_SelectedStrategy_allrun_i0.append(round_ave_allrun_i0)
    #print("the round average following probability of all run is:", ave_SelectedStrategy_allrun_i0)

    print("")
    print("")
    print("")
    print("")


    print("SUMMARY 2 ________________________________________________________________")
    print("CORRELATED EQM IN CHICKEN GAME (GOOD RECOMMENDATION TREATMENT)")
    print("(C,D), (D,C), (C,C) are reccomended w/p 1/3 each")
    print("")
    print("rounds=", rounds)
    print("runs=", runs)
    print("# of agent =", I)
    print("#number of alternatives in the remembered strategy set=", J)
    print("#experimentation probability=", pex)
    print("#experimentation std=", theta)

    #calculating average payoff of all round over all runs    
    ave_payoff_allrun_i0 = np.mean(payoff_allrun_i0)
    ave_payoff_allrun_i1 = np.mean(payoff_allrun_i1)
    sd0 = np.std(payoff_allrun_i0)
    sd1 = np.std(payoff_allrun_i1)
    print("-----------------------------------------------------------------------------\n","THE AVERAGE PAYOFF OF AGENT i=0 OVER", runs, "runs is", ave_payoff_allrun_i0, "with std", sd0)        
    print("THE AVERAGE PAYOFF OF AGENT i=1 OVER", runs, "runs is", ave_payoff_allrun_i1, "with std", sd1)        

    #calculating average payoff of last 50% rounds over all runs 
    ave_payoff_lasthalfround_i0 = np.mean(payoff_allrun_i0[int(round(0.5*len(payoff_allrun_i0))):len(payoff_allrun_i0)])
    ave_payoff_lasthalfround_i1 = np.mean(payoff_allrun_i1[int(round(0.5*len(payoff_allrun_i1))):len(payoff_allrun_i1)])
    sd00 = np.std(payoff_allrun_i0[int(round(0.5*len(payoff_allrun_i0))):len(payoff_allrun_i0)])
    sd11 = np.std(payoff_allrun_i1[int(round(0.5*len(payoff_allrun_i1))):len(payoff_allrun_i1)])

    print("-----------------------------------------------------------------------------\n","THE AVERAGE PAYOFF OF AGENT i=0 OVER last 50% round of all", runs, "runs is", ave_payoff_lasthalfround_i0, "with std", sd00)        
    print("THE AVERAGE PAYOFF OF AGENT i=1 OVER last 50% round of all", runs, "runs is", ave_payoff_lasthalfround_i1, "with std", sd11)        

    print("-----------------------------------------------------------------------------")  
    print("Nash outcome frequency over", runs ,"runs (out of",rounds, "rounds) is",Nash_outcome_frequency_allrun)
    print("with mean", np.mean(Nash_outcome_frequency_allrun), "(note: Duffy, Feltovich (2010)'s number is 57.9%)")

    print("-----------------------------------------------------------------------------")  
    print("FOLLOW frequency of i=0 over", runs, "runs(out of last 50% round =",0.5*rounds, "rounds) is", folo_frequency_i0_allrun, "mean:", np.mean(folo_frequency_i0_allrun))
    print("FOLLOW frequency of i=1 over", runs, "runs(out of last 50% round =",0.5*rounds, "rounds) is", folo_frequency_i1_allrun, "mean:", np.mean(folo_frequency_i1_allrun))
    print("BOTH FOLLOWING over", runs, "runs(out of last 50% round =",0.5*rounds, "rounds) is", both_folo_frequency_allrun, "mean:", np.mean(both_folo_frequency_allrun))




    print("")
    print("")
    print("END OF SUMMARY 2_______________________________________________________________")
                
    trace0 = go.Scatter(
        x = list(range(rounds)),
        y = list(ave_SelectedStrategy_allrun_i0),
        mode = 'lines+markers',
        name = 'lines'
    )
    layout = go.Layout(
        title="",
        width=800,
        height=600,
        xaxis=dict(
            title='period',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='round average probability of following the reccommendation of agent i=0',
            nticks=10,
            range=[0,1],
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    data = [trace0]
    figure = go.Figure(data=data,layout=layout)
    #plotly.offline.plot(figure, filename='line-mode.html')

#########################################################################################################


simulation_NashReccommendation(rounds, runs, I, J, pex, theta)
simulation_GoodReccommendation(rounds, runs, I, J, pex, theta)


