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
    S = []  # can do it as a list too but counters are nice and make things easier
    # S = Counter()
    for i in range(len(df['Station Name'])):
        S.append(df.iloc[i, 1])
        # S[i] = df.iloc[i, 1]
        # print(S[i])

    ''' gamma '''
    # gamma - num of bikes that can be picked up or dropped off in one time step - (given by data)
    # if timestep is 10 minutes, we can assume that we can pick up all of the bikes for one trailer (13 bikes max)
    gamma = 13

    ''' start(s) '''
    # start(s) = num bikes in station s at time = 1 - (given by data)
    start = Counter()  # keys are station names
    for i in range(len(df['Station Name'])):
        start[S[i]] = df.iloc[i, 4]  # 4 th col in our spreadsheet
        print "Start:", start[S[i]], "| ", S[i], "(Station %s" % i, ")"

    # min(s) = num of bikes at station s that minimizes the number of dissatisfied customers - (given by data)
    # '''****TO DO****'''

    min = Counter()
    for i in range(len(df['Station Name'])):
        min[S[i]] = df.iloc[
                        i, 3] - 1  # min and start are the same on a few stations (PROB WRONG DATA), so we divide by 0
        print "min[%s]" % i, min[S[i]]
        # min[i] = 10  # Just to test
    # just arbitrarily say it's 2 so there's at least

    # max(s) = max number of bikes that fit in a station- (given by data)
    max = Counter()
    for i in range(len(df['Station Name'])):
        max[S[i]] = df.iloc[i, 2]
        print "max[%s]" % i, max[S[i]]
        # min[i] = 10  # Just to test
    # just arbitrarily say it's 2 so there's at least

    ''' F(s) '''
    # F(s) = user dissatisfaction function (depends on the business of station s)  - (given by data)
    '''****TO DO****'''
    # F(s) isn't actually used anywhere except for c which we are giving arbitrary values so it's fine

    # F(s) is bounded by the min(s) < F(s) < max(s)
    # So to approximate why not just take the average
    F = Counter()
    for s in S:
        print max[s]
        print min[s]
        print "avg: ", (min[s] + max[s]) / 2
        print "difference: ", max[s] - min[s]
        #F[s] = (min[s] + max[s]) / 2
        F[s] = max[s] - min[s]

    ''' c(s) '''
    # c(s) = slope of F(s) and provides the improvement per bike moved at station s  (calculate from F(s)
    # How much better it gets when we add one bike to a station
    # c(s) = (F[s][start(s)] - F[s][[min(s)] / abs(start(s) - min(s))
    # F takes the station s, and the number of bikes at the station, and gives the dissatisfaction (if zero bikes)
    # Can simply assume F(s) = arbitrary values

    # Exact c[s] values
    c = Counter()
    for s in S:
        print "F[s]", F[s]
        print "start[s]", start[s]
        print "min[s]", min[s]
        c[s] = ((F[s] * start[s] - F[s] * min[s]) / abs(start[s] - min[s]))
        print "c[s]", c[s]


    ''' N(S) '''
    # N(s) = list of stations a truck can move to from station s in a single time step (adjacent to it) - given by data
    # Could store neighborhood of s as a counter but makes more sense as a list
    N = Counter()

    for i in range(len(df['Station Name'])):
        N[S[i]] = []
        for j in range(len(df['Station Name'])):
            if distances.iloc[i, j + 1] > 0:
                if distances.iloc[i, j + 1] < 1.5:
                    N[S[i]].append(S[j])

        print "Neighborhood of ", S[i], "=", N[S[i]]

    # East Hadley road is farther away but the traffic isn't as bad as on campus
    # so, we manually add it's closest neighbors
    N[S[3]].append(S[0])
    N[S[3]].append(S[1])
    N[S[3]].append(S[4])

    print "New Neighborhood of ", S[3], N[S[3]]  #

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
    # x = [[['#' for s in range(48)] for t in range(48)] for k in range(48)]
    # print x

    for s in S:
        for t in T:
            for k in K:
                x[s, t, k] = m.addVar(vtype=GRB.BINARY, name="x[%s,%s,%s]" % (str(s), str(t), str(k)))
    print "Added x variable"

    ''' y[s, t, k] = 1 number of bikes at station s at time t that truck k has access to '''
    # Add Variable y[s, t, k]
    y = Counter()
    for s in S:
        for t in T:
            for k in K:
                y[s, t, k] = m.addVar(vtype=GRB.INTEGER, name="y[%s,%s,%s]" % (str(s), str(t), str(k)))
    print "Added y variable"

    ''' b[t, k] = number of bikes in truck k at time t '''
    # Add Variable b[t, k]
    b = Counter()
    for t in T:
        for k in K:
            b[t, k] = m.addVar(vtype=GRB.INTEGER, name="b[%s,%s]" % (str(t), str(k)))
    print "Added b variable"

    # Variable T is simply the number of timesteps
    # print len(T)

    #add slack variables for soft constraint
    slack1 = m.addVar(vtype=GRB.INTEGER, lb=0, name="slack variable 1")


    # Set objective
    m.setObjective(quicksum((y[s, 1, k] - y[s, len(T), k]) * c[s] - slack1
                            for s in S for k in K), GRB.MINIMIZE)
    print "Set objective function"

    # This constraint holds for ALL S, ALL t, and ALL K

    # Add Constraint (2)
    for s in S:
        # print s
        # print N[s]
        for t in T:
            for k in K:
                m.addConstr(x[s, t, k] <= x[s, t - 1, k] + quicksum(x[sprime, t - 1, k] for sprime in N[s]), "c2")

    # Add Constraint (3)
    for t in T:
        for k in K:
            #continue
            m.addConstr(quicksum(x[s, t, k] for s in S) == 1, "c3")

    # Add Constraint (4)
    for s in S:
        #continue
        m.addConstr(quicksum(y[s, 1, k] for k in K) == start[s], "c4")

    # Add Constraint (5)
    for s in Sminus:
        for t in T:
            #continue
            m.addConstr(start[s] <= quicksum(y[s, t, k] for k in K) <= min[s], "c5")

    # Add Constraint (6)

    for s in Splus:
        for t in T:
            #continue
            m.addConstr(min[s] <= quicksum(y[s, t, k] for k in K) <= start[s], "c6")

    # Add Constraint (7)
    for t in T:
        for k in K:
            #continue
            m.addConstr(quicksum(y[s, t, k] for s in S) + b[t, k] == quicksum(y[s, 1, k] for s in S) + b[1, k], "c7")
    print "Added Constraint 7"

    # Add Constraint (8)
    for s in S:
        for t in T:
            for k in K:
                # print "t: ", t
                if t != 0:  # t-1 doesn't work if t=0
                    newVar1 = m.addVar(vtype=GRB.INTEGER, name="newVar1")
                    newVar2 = m.addVar(vtype=GRB.INTEGER, name="newVar2")
                    # print "created newVar1 & newVar2"
                    m.addConstr(newVar1 == (y[s, t, k] - y[s, t, k]))  # dummy variable 1
                    m.addGenConstrAbs(newVar2, newVar1)  # newVar2 == abs(newVar1)

                    #continue
                    m.addConstr(newVar2 <= (gamma * x[s, t, k]), "c8")
    print "Added Constraint 8"

    # Add Constraint (9)
    for s in S:
        for t in T:
            for k in K:
                newVar3 = m.addVar(vtype=GRB.INTEGER, name="newVar3")
                newVar4 = m.addVar(vtype=GRB.INTEGER, name="newVar4")
                newVar5 = m.addVar(vtype=GRB.INTEGER, name="newVar5")
                newVar6 = m.addVar(vtype=GRB.INTEGER, name="newVar6")
                m.addConstr(newVar3 == y[s, t, k] - y[s, t - 1, k])  # dummy variable 1
                m.addConstr(newVar4 == x[s, t, k] - x[s, t - 1, k])  # dummy variable 2
                m.addGenConstrAbs(newVar5, newVar3)  # newVar5 == abs(newVar3)
                m.addGenConstrAbs(newVar6, newVar4)  # newVar6 == abs(newVar4)

                #continue
                m.addConstr(newVar5 + gamma * newVar6 <= gamma + slack1, "c9")
    print "Added Constraint 9"

    print "Added all constraints \n"
    # Optimize model
    m.optimize()

    m.write('linearprogram.lp')
    # print "Optimized model"

    # WAY too many vars to print them all (from example code)
    # for v in m.getVars():
    #    print('%s %g' % (v.varName, v.x))

    # Print Objective Model
    # print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')

