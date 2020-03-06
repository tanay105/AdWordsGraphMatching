import sys
import copy
import math 
import random
import pandas as pd
import numpy as np
def readFile(filename):
	with open(filename) as fp:
		return fp.read().splitlines()

def readCSV(filename):
	reader = pd.read_csv(filename)
	data = []
	n = len(reader)
	for i in range(0, n):
		data.append([reader.iloc[i,0], reader.iloc[i,1], reader.iloc[i,2], reader.iloc[i,3]])
	return data

def getBidderBudget(bidderData):
	bidderBudget = dict()
	bidderId = -1
	for row in bidderData:
		if row[0] != bidderId:
			bidderId = row[0]
			bidderBudget[bidderId] = row[3]
	return bidderBudget

def getBidderQueries(bidderData):
	bidderQueries = dict()
	for row in bidderData:
		bidderQueries[row[1]] = list()
	for row in bidderData:
		bidderQueries[row[1]].append((row[0], row[2]))
	return bidderQueries

def getOptimalMatching(bidderBudget):
	total = 0
	for key in bidderBudget:
		total += bidderBudget[key]
	return total

def greedyAlgo(queriesData, bidderBudget, bidderQueries):
	totalRevenue = 0
	for query in queriesData:
		tempMax = 0
		tempId = -1
		newBids = bidderQueries[query]
		for aId, bidValue in newBids:
			if bidValue > tempMax:
				if bidderBudget[aId] >= bidValue:
					tempMax = bidValue
					tempId = aId
		#for key in bidderQueries:  # (id, query) : valueBid
		#	if key[1] == query:
		#		value = bidderQueries[key]
		#		if value > bidderBudget[key[0]]:
		#			continue
		#		elif value > tempMax:
		#			tempMax = value
		#			tempId = key[0]
		#totalRevenue += tempMax
		if tempId != -1:
			totalRevenue += tempMax
			bidderBudget[tempId] -= tempMax
	return totalRevenue

def balanceAlgo(queriesData, bidderBudget, bidderQueries):
	totalRevenue = 0
	for query in queriesData:
		tempMax = 0
		tempId = -1
		tempBid = 0
		newBids = bidderQueries[query]
		for aId, bidValue in newBids:
			if bidderBudget[aId] > tempMax:
				if bidderBudget[aId] >= bidValue:
					tempMax = bidderBudget[aId]
					tempId = aId
					tempBid = bidValue
		if tempId != -1:
			totalRevenue += tempBid
			bidderBudget[tempId] -= tempBid
	return totalRevenue

def mathCalc(value):
	temp = 1 - math.exp(value - 1)
	return temp

def msvvAlgo(queriesData, bidderBudget1, bidderBudget2, bidderQueries):
	totalRevenue = 0
	for query in queriesData:
		tempMax = 0
		tempId = -1
		tempBid = 0
		newBids = bidderQueries[query]
		for aId, bidValue in newBids:
			new = bidValue * mathCalc((bidderBudget2[aId] - bidderBudget1[aId])/bidderBudget2[aId])
			if new > tempMax:
				if bidderBudget1[aId] >= bidValue:
					tempMax = new
					tempId = aId
					tempBid = bidValue
		if tempId != -1:
			totalRevenue += tempBid
			bidderBudget1[tempId] -= tempBid
	return totalRevenue

def getALTMSSVAlgo(queriesData, bidderBudget, bidderQueries):
	totalBidValue = 0
	random.seed(0)
	tempBidderBudget = copy.deepcopy(bidderBudget)
	tempBidValue = msvvAlgo(queriesData, tempBidderBudget, bidderBudget, bidderQueries)
	print(round(tempBidValue,2))
	for i in range(0, 100):
		random.shuffle(queriesData)
		tempBidderBudget = copy.deepcopy(bidderBudget)
		tempBidValue = msvvAlgo(queriesData, tempBidderBudget, bidderBudget, bidderQueries)
		totalBidValue += tempBidValue
	return totalBidValue/100

def getALTBalanceAlgo(queriesData, bidderBudget, bidderQueries):
	totalBidValue = 0
	random.seed(0)
	tempBidderBudget = copy.deepcopy(bidderBudget)
	tempBidValue = balanceAlgo(queriesData, tempBidderBudget, bidderQueries)
	print(round(tempBidValue,2))
	for i in range(0, 100):
		random.shuffle(queriesData)
		tempBidderBudget = copy.deepcopy(bidderBudget)
		tempBidValue = balanceAlgo(queriesData, tempBidderBudget, bidderQueries)
		totalBidValue += tempBidValue
	return totalBidValue/100

def getALTGreedyAlgo(queriesData, bidderBudget, bidderQueries):
	totalBidValue = 0
	random.seed(0)
	tempBidderBudget = copy.deepcopy(bidderBudget)
	tempBidValue = greedyAlgo(queriesData, tempBidderBudget, bidderQueries)
	print(round(tempBidValue,2))
	for i in range(0, 100):
		random.shuffle(queriesData)
		tempBidderBudget = copy.deepcopy(bidderBudget)
		tempBidValue = greedyAlgo(queriesData, tempBidderBudget, bidderQueries)
		totalBidValue += tempBidValue
	return totalBidValue/100

def main():
	algorithm = str(sys.argv[1])
	queriesData = readFile('queries.txt')
	bidderData = readCSV('bidder_dataset.csv')
	bidderBudget = getBidderBudget(bidderData)
	bidderQueries = getBidderQueries(bidderData)
	oPT = getOptimalMatching(bidderBudget)
	if algorithm == "greedy":
		aLT = getALTGreedyAlgo(queriesData, bidderBudget, bidderQueries)
		print(round(aLT/oPT,2))
	elif algorithm == "balance":
		aLT = getALTBalanceAlgo(queriesData, bidderBudget, bidderQueries)
		print(round(aLT/oPT,2))
	elif algorithm == "msvv" or algorithm == "mssv":
		aLT = getALTMSSVAlgo(queriesData, bidderBudget, bidderQueries)
		print(round(aLT/oPT,2))

main()
