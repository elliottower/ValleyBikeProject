#!/usr/bin/python

from gurobipy import *
from collections import Counter
import pandas as pd

# noinspection PyInterpreter,PyInterpreter
try:

    # Create a new model
    m = Model("mip1")

    # Import spreadsheet
    df = pd.read_csv("AmherstBikeStations.csv",
                     sep=",",
                     header=0)
    # Import distances spreadsheet
    distances = pd.read_csv("StationDistances.csv",
                     sep=",",
                     header=0)

    # Create variables

    ''' T = num of time steps '''
    # Each time step is 10 minutes
    # 8 hours work day
    T = [i for i in range(48)]
    print "Timesteps: ", T

    ''' K = num of trucks'''
    K = [i for i in range(3)]

    ''' S = Set of Stations '''
    S = [] # can do it as a list too but counters are nice and make things easier
    # S = Counter()
    for i in range(len(df['Station Name'])):
        S.append(df.iloc[i, 1])
        #S[i] = df.iloc[i, 1]
        # print(S[i])

    ''' gamma '''
    # gamma - num of bikes that can be picked up or dropped off in one time step - (given by data)
    # if timestep is 10 minutes, we can assume that we can pick up all of the bikes for one trailer (13 bikes max)
    gamma = 13

    ''' start(s) '''
    # start(s) = num bikes in station s at time = 1 - (given by data)
    start = Counter() # keys are station names
    for i in range(len(df['Station Name'])):
        start[S[i]] = df.iloc[i, 3]  # 7 th col in our spreadsheet
        print "Start:", start[S[i]],  "| ", S[i], "(Station %s" % i, ")"

    # min(s) = num of bikes at station s that minimizes the number of dissatisfied customers - (given by data)
    '''****TO DO****'''

    min = Counter()
    for i in range(len(df['Station Name'])):
        min[i] = 10  # Just to test
    # just arbitrarily say it's 2 so there's at least

    ''' F(s) '''
    # F(s) = user dissatisfaction function (depends on the business of station s)  - (given by data)
    '''****TO DO****'''
    # F(s) isn't actually used anywhere except for c which we are giving arbitrary values so it's fine

    ''' c(s) '''
    # c(s) = slope of F(s) and provides the improvement per bike moved at station s  (calculate from F(s)
    # How much better it gets when we add one bike to a station
    # c(s) = (F[s][start(s)] - F[s][[min(s)] / abs(start(s) - min(s))
    # F takes the station s, and the number of bikes at the station, and gives the dissatisfaction (if zero bikes)
    '''****TO DO****'''

    # Can simply assume C(s) = arbitrary values
    c = Counter()
    for s in S:
        c[s] = 1

    ''' N(S) '''
    # N(s) = list of stations a truck can move to from station s in a single time step (adjacent to it) - given by data
    # Could store neighborhood of s as a counter but makes more sense as a list
    N = Counter()

    for i in range(len(df['Station Name'])):
        N[S[i]] = []
        for j in range(len(df['Station Name'])):
            if distances.iloc[i, j+1] > 0:
                if distances.iloc[i, j+1] < 1.5:
                    N[S[i]].append(S[j])

        print "Neighborhood of ", S[i], "=", N[S[i]]

    # East Hadley road is farther away but the traffic isn't as bad as on campus
    # so, we manually add it's closest neighbors
    N[S[3]].append(S[0])
    N[S[3]].append(S[1])
    N[S[3]].append(S[4])

    print "New Neighborhood of ", S[3], N[S[3]] #

    ''' Splus '''
    # Splus = subset of S where start(s) > min(s)
    # for s in S:
    Splus = []
    for s in S:
        if start[s] > min[s]:
            # Could represent subset as a list, or as a dictionary (might be easier later this way, but list simpler)
            Splus.append(s)
            # Splus[s] = 1
    print "Splus: ", Splus

    ''' Sminus '''
    # Sminus = subset of S where start(s) <= min(s)
    Sminus = []
    for s in S:
        if start[s] <= min[s]:
            # Could represent subset as a list, or as a dictionary (might be easier later this way, but list simpler)
            Sminus.append(s)
    print "Sminus: ", Sminus

    # Regular Variables (not given by data):

    ''' x[s, t, k] = 1 if truck k is at station s at time t, 0 else '''
    # Add Variable x[s, t, k]
    x = Counter()
    # Could try to do a 3d vector but that's AWFUL and it works okay just doing a counter it seems at least
    #x = [[['#' for s in range(48)] for t in range(48)] for k in range(48)]
    #print x

    for s in S:
        for t in T:
            for k in K:
                x[s, t, k] = m.addVar(vtype=GRB.BINARY, name="x[%s,%s,%s]" % (str(s), str(t), str(k)))

                #x[s][t][k] = m.addVar(vtype=GRB.BINARY)#, name="x[%s,%s,%s]" % (str(s), str(t), str(k)))

    ''' y[s, t, k] = 1 number of bikes at station s at time t that truck k has access to '''
    # Add Variable y[s, t, k]
    y = Counter()
    for s in S:
        for t in T:
            for k in K:
                y[s, t, k] = m.addVar(vtype=GRB.BINARY, name="y[%s,%s,%s]" % (str(s), str(t), str(k)))

    ''' b[t, k] = number of bikes in truck k at time t '''
    # Add Variable b[t, k]
    b = Counter()
    for t in T:
        for k in K:
            b[t, k] = m.addVar(vtype=GRB.BINARY, name="b[%s,%s]" % (str(t), str(k)))

    # Variable T is simply the number of timesteps
    #print len(T)

    # Set objective
    m.setObjective(quicksum((y[s, 1, k] - y[s, len(T), 1]) * c[s]
                            for s in S), GRB.MINIMIZE)

    #m.setObjective(quicksum((y[s][1][k] - y[s][len(T)][k]) * c[s]
                            #for s in S for k in K), GRB.MINIMIZE)

    # This constraint holds for ALL S, ALL t, and ALL K
    # for s in S, t in T, k in K: #might work this way but more
    #    x[s, t, k] <= x[s, t-1, k] + quicksum(x[sprime, t-1, k] for sprime in N(s))



    # Add Constraint (2)
    for s in S:
        print s
        print N[s]
        for t in T:
            for k in K:
                m.addConstr(x[s, t, k] <= x[s, t - 1, k] + quicksum(x[sprime, t - 1, k] for sprime in N[s]), "c2")

    # Add Constraint (3)
    for t in T:
        for k in K:
            m.addConstr(quicksum(x[s, t, k] for s in S) == 1, "c3")

    # Add Constraint (4)
    for s in S:
        m.addConstr(quicksum(y[s, 1, k] for k in K) == start[s], "c4")

    # Add Constraint (5)
    for s in S:
        for t in T:
            m.addConstr(start[s] <= quicksum(y[s, t, k] for k in K) <= min[s], "c5")

    # Add Constraint (6)

    for s in S:
        for t in T:
            m.addConstr(min[s] <= quicksum(y[s, t, k] for k in K) <= start[s], "c6")

    # Add Constraint (7)
    for t in T:
        for k in K:
            m.addConstr(quicksum(y[s, t, k] for s in S) + b[t, k] == quicksum(y[s, 1, k] for s in S) + b[1, k], "c7")
    print "Added Constraint 7"

    # Add Constraint (8)
    for s in S:
        for t in T:
            for k in K:
                #print "t: ", t
                if t != 0:  # t-1 doesn't work if t=0
                    newVar1 = m.addVar(name="newVar1")
                    newVar2 = m.addVar(name="newVar2")
                    #print "created newVar1 & newVar2"
                    m.addConstr(newVar1 == y[s,t,k] - y[s,t,k]) #dummy variable 1
                    m.addGenConstrAbs(newVar2, newVar1) #newVar2 == abs(newVar1)
                    m.addConstr(newVar2 <= gamma * x[s, t, k], "c8")

                    #m.addConstr(abs_(y[s, t, k] - y[s, t - 1, k]) <= gamma * x[s, t, k], "c8")
    print "Added Constraint 8"

    # Add Constraint (9)
    for s in S:
        for t in T:
            for k in K:
                newVar3 = m.addVar(name="newVar3")
                newVar4 = m.addVar(name="newVar4")
                newVar5 = m.addVar(name="newVar5")
                newVar6 = m.addVar(name="newVar6")
                m.addConstr(newVar3 == y[s, t, k] - y[s, t - 1, k])  # dummy variable 1
                m.addConstr(newVar4 == x[s, t, k] - x[s, t - 1, k])  # dummy variable 2
                m.addGenConstrAbs(newVar5, newVar3)  # newVar5 == abs(newVar3)
                m.addGenConstrAbs(newVar6, newVar4)  # newVar6 == abs(newVar4)


                m.addConstr(newVar5 + gamma * newVar6 <= gamma, "c9")
    print "Added Constraint 9"

    print "Added all constraints"
    # Optimize model
    m.optimize()

    #print "Optimized model"

    # WAY too many vars to print them all (from example code)
    # for v in m.getVars():
    #    print('%s %g' % (v.varName, v.x))

    # Print Objective Model
    #print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')


