#!/usr/bin/python

from collections import Counter
import pandas as pd
import random
import math

# Import stations spreadsheet
df = pd.read_csv("AmherstBikeStations.csv",
                 sep=",",
                 header=0)

''' S = Set of Stations '''
S = []  # can do it as a list too but counters are nice and make things easier
# S = Counter()
for i in range(len(df['Station Name'])): # should be
    S.append(df.iloc[i, 1])
    # S[i] = df.iloc[i, 1]
    #print(S[i])

# max(s) = max number of bikes that fit in a station- (given by data)
max = Counter()
for i in range(len(df['Station Name'])):
    max[S[i]] = df.iloc[i, 2]
    #print "max[%s]" % S[i], max[S[i]]
    # min[i] = 10  # Just to test
# just arbitrarily say it's 2 so there's at least

# Import rental/return demand spreadsheet
    routes11 = pd.read_csv("Valley_Routes_Report_September_2019_UMass_9_11.csv",
                      sep=",",
                      header=0)

    routes19 = pd.read_csv("Valley_Routes_Report_September_2019_UMass_9_19.csv",
                      sep=",",
                      header=0)

    routes30 = pd.read_csv("Valley_Routes_Report_September_2019_UMass_9_30.csv",
                      sep=",",
                      header=0)

    days = [routes11, routes19, routes30]


# Calculate rental demand

def computeRentalDemand(station): #using lists
    demand = [0] * 24 # start out at zero for every hour of the day
    for day in days:  # for all 3 days
        for j in range(24): # loop through every hour of the day
            for i in range(len(day['Start'])):  # loop through all the lines in the spreadsheet
                demand_time = day.iloc[i, 1]  # column number 1 (2nd col)
                if demand_time == j:
                    if day.iloc[i, 10] == station:
                        demand[j] += 1
    newDemand = [float(x) / len(days) for x in demand]
    demand = newDemand
    return demand


def computeReturnDemand(station): #using lists
    demand = [0] * 24 # start out at zero for every hour of the day
    for day in days:  # for all 3 days
        for j in range(24): # loop through every hour of the day
            for i in range(len(day['Start'])):  # loop through all the lines in the spreadsheet
                demand_time = day.iloc[i, 3]  # column number 1 (2nd col)
                if demand_time == j:
                    if day.iloc[i, 11] == station:
                        demand[j] += 1
    newDemand = [float(x) / len(days) for x in demand]
    demand = newDemand
    return demand

def computeUDF(station, rental_demand, return_demand, interval_length):
    number_iterations = 30
    solution = [0] * (max[station] + 1)
    for repetition in range(number_iterations):  # repeat 30 times, 30 simulations
        bikes_present = range(max[station]+1)
        arrivals = []
        k = 0
        while k < len(rental_demand):
            next_arrival = 0
            while next_arrival < interval_length[k]:
                current_rental_demand = rental_demand[k]
                current_return_demand = return_demand[k]
                next_arrival += math.exp(1/(current_rental_demand + current_return_demand + 0.01))
                #print "k: ", k
                #print "rental_demand[k]", rental_demand[k]
                #print "interval_length[k]", interval_length[k]
                if next_arrival < interval_length[k]:
                    arrivals.append(flip(current_rental_demand / (current_rental_demand + current_return_demand)))
                else:
                    k += 1
                    break

                ### At this point, arrivals should have the list of arrivals over the course of the
                ### time horizon and we compute the expected number of stock-outs
            for initial_bikes in bikes_present:
                bikes = initial_bikes  # bikes tracks the number of bikes after each arrival
                for x in arrivals:
                    #print "x: ", x
                    #print "bikes: ", bikes
                    # - 1 indicates someone taking out a bike (rental demand)
                    # 1 indicates returning a bike
                    if (x == -1 and bikes == 0) or (x == 1 and bikes == max[station]):
                        solution[initial_bikes] += 1.0 / number_iterations
                        #print "stockout occurred: ", solution[initial_bikes]
                        # if a stock-out occurs, we count but number of bikes remains same
                    else:
                        bikes += x  # else, number of bikes changes
    return solution


def flip(p):
    if random.random() < p:
        return 1
    else:
        return -1


# Driver that computes UDF for each station
def getUDF():
    UDF = Counter()
    INTERVAL_LENGTH = 60  # 60 minute

    for station in S:
        rental_demand = computeRentalDemand(station)
        return_demand = computeReturnDemand(station)
        interval_length = [INTERVAL_LENGTH] * len(return_demand)  # needs to be tuples
        #print len(return_demand)
        #print len(interval_length)
        #demand = [rental_demand, return_demand, interval_length]
        UDF[station] = computeUDF(station, rental_demand, return_demand, interval_length)

    return UDF

def test():
    UDF = getUDF()
    for s in S:
        print "Station: ", s, UDF[s]
        print "UDF[s][1]", UDF[s][1]







