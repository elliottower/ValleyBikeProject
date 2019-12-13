#!/usr/bin/python

from gurobipy import *
from collections import Counter
import pandas as pd
import math
import UDF

# noinspection PyInterpreter,PyInterpreter
try:

    # Create a new model
    m = Model("mip1")

    # Import spreadsheet
    df = pd.read_csv("AmherstBikeStationsTest.csv",
                     sep=",",
                     header=0)
    # Import distances spreadsheet
    distances = pd.read_csv("StationDistancesTest.csv",
                            sep=",",
                            header=0)

    # Create variables

    ''' T = num of time steps '''
    # Each time step is 10 minutes
    # 8 hours work day

    NUM_TIME_STEPS = 4
    T = [i for i in range(NUM_TIME_STEPS)] #should be 48
    print "Timesteps: ", T

    NUM_TRUCKS = 1
    ''' K = num of trucks'''
    K = [i for i in range(NUM_TRUCKS)] # should be 3 but testing with 1

    ''' S = Set of Stations '''
    S = []  # can do it as a list too but counters are nice and make things easier
    # S = Counter()
    for i in range(len(df['Station Name'])): # should be
        S.append(df.iloc[i, 0]) # need to have actual names for UDF to work
        # S[i] = df.iloc[i, 1]
        print "Station %s:" % i, (S[i])

    ''' gamma '''
    # gamma - num of bikes that can be picked up or dropped off in one time step - (given by data)
    # if timestep is 10 minutes, we can assume that we can pick up all of the bikes for one trailer (13 bikes max)
    gamma = 13

    ''' start(s) '''
    # start(s) = num bikes in station s at time = 1 - (given by data)
    start = Counter()  # keys are station names
    for i in range(len(df['Station Name'])):
        start[S[i]] = df.iloc[i, 4]  # 4 th col in our spreadsheet
        print "start[%s]" % S[i], start[S[i]]

    # min(s) = num of bikes at station s that minimizes the number of dissatisfied customers - (given by data)
    # '''****TO DO****'''

    min = Counter()
    for i in range(len(df['Station Name'])):
        min[S[i]] = df.iloc[i, 3]  # min and start are the same on a few stations (PROB WRONG DATA), so we divide by 0
        print "min[%s]" % S[i], min[S[i]]
        # min[i] = 10  # Just to test
    # just arbitrarily say it's 2 so there's at least

    # max(s) = max number of bikes that fit in a station- (given by data)
    max = Counter()
    for i in range(len(df['Station Name'])):
        max[S[i]] = df.iloc[i, 2]
        print "max[%s]" % S[i], max[S[i]]
        # min[i] = 10  # Just to test
    # just arbitrarily say it's 2 so there's at least

    ''' F(s) '''
    # F(s) = user dissatisfaction function (depends on the business of station s)  - (given by data)
    '''****TO DO****'''
    # F(s) isn't actually used anywhere except for c which we are giving arbitrary values so it's fine

    # F(s) is bounded by the min(s) < F(s) < max(s)
    # So to approximate why not just take the average
    F = Counter()
    #for s in S:
        #print max[s]
        #print min[s]
        #print "avg: ", (min[s] + max[s]) / 2
        #print "difference: ", max[s] - min[s]
        #F[s] = (min[s] + max[s]) / 2
        #F[s] = 1.5
        #F[s] = max[s] - min[s]
    #F = UDF.getUDF()
    #print F
    #for s in S:
        #print "F[%s]:" % s, F[s]

    ''' c(s) '''
    # c(s) = slope of F(s) and provides the improvement per bike moved at station s  (calculate from F(s)
    # How much better it gets when we add one bike to a station
    # c(s) = (F[s][start(s)] - F[s][[min(s)] / abs(start(s) - min(s))
    # F takes the station s, and the number of bikes at the station, and gives the dissatisfaction (if zero bikes)
    # Can simply assume F(s) = arbitrary values

    # Exact c[s] values
    c = Counter()

    for s in S:
        #print "F[s]", F[s]
        #print "start[s]", start[s]
        #print "min[s]", min[s]
        #c[s] = ((F[s][start[s]] - F[s][min[s]]) / abs(start[s] - min[s] + 0.01)) #c an divide by zero
        #c[s] = min[s] - start[s]
        print "c[%s]" % s, c[s]


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
    #N[S[3]].append(S[0])
    #N[S[3]].append(S[1])
    #N[S[3]].append(S[4])

    #print "New Neighborhood of ", S[3], N[S[3]]  #

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
                y[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb = 0, name="y[%s,%s,%s]" % (str(s), str(t), str(k)))
    print "Added y variable"

    ''' b[t, k] = number of bikes in truck k at time t '''
    # Add Variable b[t, k]
    b = Counter()
    for t in T:
        for k in K:
            b[t, k] = m.addVar(vtype=GRB.INTEGER, lb=0, name="b[%s,%s]" % (str(t), str(k)))
    print "Added b variable"

    # Variable T is simply the number of timesteps
    # print len(T)

    # This constraint holds for ALL S, ALL t, and ALL K

    # Add Constraint (2) (allows trucks only to move to a station adjacent to current one)
    for s in S:
        for t in T:
            if t > 0:
                for k in K:
                    m.addConstr(x[s, t, k] <= x[s, t - 1, k] + quicksum(x[sprime, t - 1, k] for sprime in N[s]), "c2[%s,%s,%s]" % (s, t, k))

    # Add Constraint (3) (a truck can be in only one station in a given time step)
    for t in T:
        for k in K:
            #continue
            m.addConstr(quicksum(x[s, t, k] for s in S) == 1, "c3[%s,%s]" % (t, k))

    # Add Constraint (4) (initiates the number of bikes at every station)
    for s in S:
        #continue
        m.addConstr(quicksum(y[s, 0, k] for k in K) == start[s], "c4[%s]" % s)


    # Add Constraint (5) (in S- set, makes sure that there are less bikes than originally)
    for s in Sminus:
        for t in T:
            #continue
            m.addConstr(quicksum(y[s, t, k] for k in K) - start[s] >= 0, "c5pt1[%s,%s]" % (s, t))
            m.addConstr(quicksum(y[s, t, k] for k in K) <= min[s], "c5pt2[%s,%s]" % (s, t))

            #m.addConstr(start[s] <= quicksum(y[s, t, k] for k in K), "c5pt1[%s,%s]" % (s, t))
            #m.addConstr(quicksum(y[s, t, k] for k in K) <= min[s], "c5pt2[%s,%s]" % (s, t))


    # Add Constraint (6) (in S+ set, makes sure there are more bikes than originally, or equal)

    for s in Splus:
        for t in T:
            #continue
            m.addConstr(0 <= quicksum(y[s, t, k] for k in K) - min[s], "c6pt1[%s,%s]" % (s,t))
            m.addConstr(quicksum(y[s, t, k] for k in K) <= start[s], "c6pt2[%s,%s]" % (s,t))

    # Add Constraint (7) (total bikes does not change over time)
    for t in T:
        for k in K:
            #continue
            m.addConstr(quicksum(y[s, t, k] for s in S) + b[t, k] == quicksum(y[s, 0, k] for s in S) + b[0, k], "c7[%s,%s]" % (t, k))
    print "Added Constraint 7"

    # We are indexing each newvar & slack so they are different in each for loop, if they're the same it doesn't work
    newVar1 = Counter()
    newVar2 = Counter()
    newVar3 = Counter()
    newVar4 = Counter()
    newVar5 = Counter()
    newVar6 = Counter()
    slack1 = Counter()

    # Add Constraint (8) (constraint that we can only move so many bikes at a time)
    for s in S:
        for t in T:
            for k in K:
                # print "t: ", t
                if t != 0:  # t-1 doesn't work if t=0
                    newVar1[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000, name="newVar1[%s,%s,%s]" % (s,t,k))
                    newVar2[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000,name="newVar2[%s,%s,%s]" % (s,t,k))
                    # print "created newVar1 & newVar2"
                    m.addConstr(newVar1[s, t, k] == (y[s, t, k] - y[s, t-1, k]))  # dummy variable 1
                    m.addGenConstrAbs(newVar2[s, t, k], newVar1[s, t, k])  # newVar2 == abs(newVar1)

                    #continue
                    m.addConstr(newVar2[s, t, k] <= (gamma * x[s, t, k]), "c8[%s,%s,%s]" % (s, t, k))
    print "Added Constraint 8"



    # Add Constraint (9) (truck either moves, or picks up/drops off bikes in one time step NOT both)
    for s in S:
        for t in T:
            for k in K:
                newVar3[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000, name="newVar3[%s,%s,%s]" % (s,t,k))
                newVar4[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000, name="newVar4[%s,%s,%s]" % (s,t,k))
                newVar5[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000, name="newVar5[%s,%s,%s]" % (s,t,k))
                newVar6[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000, name="newVar6[%s,%s,%s]" % (s,t,k))
                m.addConstr(newVar3[s, t, k] == y[s, t, k] - y[s, t - 1, k])  # dummy variable 1
                m.addConstr(newVar4[s, t, k] == x[s, t, k] - x[s, t - 1, k])  # dummy variable 2
                m.addGenConstrAbs(newVar5[s, t, k], newVar3[s, t, k])  # newVar5 == abs(newVar3)
                m.addGenConstrAbs(newVar6[s, t, k], newVar4[s, t, k])  # newVar6 == abs(newVar4)

                #continue
                slack1[s, t, k] = m.addVar(vtype=GRB.INTEGER, lb=0, name="slack1[%s,%s,%s]" % (s,t,k))
                m.addConstr(newVar5[s, t, k] + gamma * newVar6[s, t, k] <= gamma + slack1[s, t, k], "c9[%s,%s,%s]" % (s,t, k))
                #m.addConstr(newVar5[s, t, k] + gamma * newVar6[s, t, k] <= gamma, "c9[%s,%s,%s]" % (s,t, k))

                #print "min[s]: ", min[s]
                #print "y[s, NUM_TIME_STEPS -1, k]:", y[s, NUM_TIME_STEPS -1, k]
                #print "b[t, k]:", b[t, k]

    print "Added Constraint 9"

    # prevent it from taking stuff out in the first time step, needed for c[s] objective func
    for s in S:
        for k in K:
            m.addConstr(y[s, 0, k] == start[s], "c10[%s,%s]" % (s, k))

    print "Added constraint 10"

    # initialize truck to have zero bikes, end with zero too
    for k in K:
        m.addConstr(b[0, k] == 0, "c11[%s]" % k)
        m.addConstr(b[NUM_TIME_STEPS-1, k] == 0, "c12[%s]" % k)

    # Arbitrarily force it to move bikes, not needed now that we can maximize/minimize
    #m.addConstr(y[1, NUM_TIME_STEPS-1, 0] == 7, "c11")
    print "Added constraint 11"

    print "Added all constraints \n"

    # Arbitrarily test out C(s) values
    c[S[0]] = -2
    c[S[1]] = -4

    # Add constraint to give absolute value of y[s,NUM_TIME_STEPS-1, k] - min[s]
    newVar7 = Counter()
    newVar8 = Counter()
    for s in S:
        for k in K:
            newVar7[s, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000, name="newVar7[%s,%s]" % (s, k))
            newVar8[s, k] = m.addVar(vtype=GRB.INTEGER, lb=-1000, name="newVar8[%s,%s]" % (s, k))
            #m.addConstr(newVar7[s, k] == min[s] - y[s, NUM_TIME_STEPS-1, k])
            #m.addConstr(newVar8[s, k] == newVar7[s, k])
            m.addConstr(newVar7[s, k] == y[s, NUM_TIME_STEPS - 1, k] - min[s])
            m.addGenConstrAbs(newVar8[s, k], newVar7[s, k])


            # Optimize model

    # Set objective
    m.setObjective(quicksum(newVar8[s, k] + slack1[s, t, k] for s in S for t in T for k in K), GRB.MINIMIZE)
    #m.setObjective(quicksum(newVar8[s, k] for s in S for k in K), GRB.MINIMIZE)

    #m.setObjective(y[1,NUM_TIME_STEPS-1, 0] - quicksum(slack1[s,t,k] for s in S for t in T for k in K), GRB.MAXIMIZE)
    #m.setObjective(-y[2,NUM_TIME_STEPS-1, 0] - quicksum(slack1[s,t,k] for s in S for t in T for k in K), GRB.MAXIMIZE)


    '''m.setObjective(quicksum((y[s, 0, k] - y[s, NUM_TIME_STEPS, k]) * c[s] - slack1[s, t, k]
                           for s in S for t in T for k in K), GRB.MAXIMIZE)'''

    print "Set objective function"

    m.optimize()
    # print "Optimized model"


    m.write('linearprogram.lp')

    #m.computeIIS()
    #m.write('linearprogram.ilp')

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    # Print Objective Model
    print('Obj: %g' % m.objVal)

    totalError = 0
    for s in S:
        #print "start[%s]: " % s, start[s]
        print "y[%s]: " % s, y[s, NUM_TIME_STEPS - 1, k].X
        print "min[%s]: " % s, min[s]
        totalError += abs(y[s, NUM_TIME_STEPS - 1, k].X - min[s])

    print "b:", b[NUM_TIME_STEPS - 1, 0].X
    print "total error: ", totalError


except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')

