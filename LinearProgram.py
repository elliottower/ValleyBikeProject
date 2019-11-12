#!/usr/bin/python

from gurobipy import *

try:

    # Create a new model
    m = Model("mip1")

    # Create variables

    # S = Set of Stations
    # T = num of time steps
    # K = num of trucks

    # gamma - num of bikes that can be picked up or dropped off in one time step - (given by data)

    # start(s) = num bikes in station s at time = 1 - (given by data)
    # min(s) = num of bikes at station s that minimizes the number of disatisfied customers - (given by data)

    # F(s) = user dissatisfaction function (depends on the business of station s)  - (given by data)

    # c(s) = slope of F(s) and provides the improvement per bike moved at station s  - (given by data)

    # Splus = subset of S where start(s) > min(s)
    # Sminus = subset of S where start(s) <= min(s)

    # N(s) = list of stations a truck can move to from station s in a single time step (adjacent to it) - given by data?
    # How do we calculate N(s) - is this given in the data?

    # regular vars, not given by data:
    # x[s][t][k] = 1 if truck k is at station s at time t, 0 else

    # y[s][t][k] = 1 number of bikes at station s at time t that truck k has access to

    # b[t][k] = number of bikes in truck k at time t


    # Add Variable x[s, t, k]
    for s in S:
        for t in T:
            for k in K:
                x[s, t, k] = m.addVar(vtype=GRB.BINARY, name="x[%s,%s,%s]" % (str(s), str(t), str(k)))

    # Add Variable y[s, t, k]
    for s in S:
        for t in T:
            for k in K:
                y[s, t, k] = m.addVar(vtype=GRB.BINARY, name="y[%s,%s,%s]" % (str(s), str(t), str(k)))
    # Add Variable b[t, k]
    for t in T:
        for k in K:
            b[t, k] = m.addVar(vtype=GRB.BINARY, name="b[%s,%s]" % (str(t), str(k)))



    # Create y[j] variables (1 if project j is being done, 0 otherwise)
    for j in range(1, 8):
        y[i] = m.addVar(vtype=GRB.BINARY, name="y%s" % str([i]))

    # Set Variables (from example code)
    # x = m.addVar(vtype=GRB.BINARY, name="x")
    # y = m.addVar(vtype=GRB.BINARY, name="y")
    # z = m.addVar(vtype=GRB.BINARY, name="z")

    # Set objective
    m.setObjective(quicksum((y[s, 1, k] - y[s, t, k]) * c(s)
                            for s in S for k in K), GRB.MINIMIZE)

    # This constraint holds for ALL S, ALL t, and ALL K
    # for s in S, t in T, k in K: #might work this way but more
    #    x[s, t, k] <= x[s, t-1, k] + quicksum(x[sprime, t-1, k] for sprime in N(s))

    # Add Constraint (2)
    for s in S:
        for t in T:
            for k in K:
                m.addConstr(x[s, t, k] <= x[s, t - 1, k] + quicksum(x[sprime, t - 1, k] for sprime in N(s)), "c2")

    # Add Constraint (3)
    for t in T:
        for k in K:
            m.addConstr(quicksum(x[s, t, k] for s in S) == 1, "c3")

    # Add Constraint (4)
    for s in S:
        m.addConstr(quicksum(y[s, 1, k] for k in K) == start(s), "c4")

    # Add Constraint (5)
    for s in S:
        for t in T:
            m.addConstr(start(s) <= quicksum(y[s, t, k] for k in K) <= min(s), "c5")

    # Add Constraint (6)

    for s in S:
        for t in T:
            m.addConstr(min(s) <= quicksum(y[s, t, k] for k in K) <= start(s), "c6")

    # Add Constraint (7)
    for t in T:
        for k in K:
            m.addConstr(quicksum(y[s, t, k] for s in S) + b[t, k] == quicksum(y[s, 1, k] for s in S) + b[1, k], "c7")

    # Add Constraint (8)
    for s in S:
        for t in T:
            for k in K:
                m.addConstr(abs(y[s, t, k] - y[s, t - 1, k]) <= gamma * x[s, t, k], "c8")

    # Add Constraint (8)
    for s in S:
        for t in T:
            for k in K:
                m.addConstr(abs(y[s, t, k] - y[s, t - 1, k]) + gamma * abs(x[s, t, k] - x[s, t - 1, k]) <= gamma, "c9")

    # Optimize model
    m.optimize()

    # WAY too many vars to print them all (from example code)
    # for v in m.getVars():
    #    print('%s %g' % (v.varName, v.x))

    # Print Objective Model
    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')
