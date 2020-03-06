import csv
import copy
import random
import pandas as pd

def readFile(filename):
	with open(filename) as fp:
		return fp.read().splitlines()

def readCSV(filename):
	#reader = csv.reader(open(filename, 'r'))
	reader = pd.read_csv(filename)
	count = 0
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
		bidderQueries[(row[0], row[1])] = row[2]
	return bidderQueries

def getOptimalMatching(bidderBudget):
	total = 0
	for key in bidderBudget:
		total += int(bidderBudget[key])
	return total

def greedyAlgo(queriesData, bidderBudget, bidderQueries):
	totalRevenue = 0
	for query in queriesData:
		for key in bidderQueries:
			tempMax = 0
			tempId = -1
			if key[1] == query:
				value = bidderQueries[key]
				if value > bidderBudget[key[0]]:
					continue
				elif value > tempMax:
					break
					tempMax = value
					tempId = key[0]
					
		print(tempMax)
		print(tempId)
		totalRevenue += tempMax
		bidderBudget[key[0]] -= tempMax
	return totalRevenue

def getALTGreedyAlgo(queriesData, bidderBudget, bidderQueries):
	totalBidValue = 0
	random.seed(0)
	for i in range(0, 1):
		random.shuffle(queriesData)
		tempBidderBudget = copy.deepcopy(bidderBudget)
		tempBidValue = greedyAlgo(queriesData, tempBidderBudget, bidderQueries)
		print(tempBidValue)
		totalBidValue += tempBidValue
	return totalBidValue/100

def main():
	queriesData = readFile('queries.txt')
	bidderData = readCSV('bidder_dataset.csv')
	bidderBudget = getBidderBudget(bidderData)
	bidderQueries = getBidderQueries(bidderData)
	oPT = getOptimalMatching(bidderBudget)
	print(oPT)
	aLT = getALTGreedyAlgo(queriesData, bidderBudget, bidderQueries)
	print(aLT)

main()
