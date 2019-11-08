#!/usr/bin/env python3
from collections import OrderedDict
import scipy
import scipy.stats as stats # run 'pip install scipy' in your terminal


def countInfections(filename: str, lowerBound: int, upperBound: int) -> dict:
	"""
	Counts the number of times each individual infected someone else.	
	
	Returns a dictionary where each key is an individual and their value
	is their corresponding infection count.

	Parameters
	----------
	filename - the name of the file to be read
	lowerBound - lower bound of years range
	upperBound - upper bound of years range
	"""

	# Open the specified file
	f = open(filename, "r")

	infectedPersons= []
	people = []

	numInfected = dict()

	# Loop over each line in the file.
	for line in f.readlines():
	    u,v,t = line.split('\t')
	    u = u.strip()
	    v = v.strip()

	    # Only considers infections within a given range of years
	    if (lowerBound > float(t)) | (float(t) > upperBound):
	    	continue

	    if u not in numInfected:
	    	numInfected[u] = 0

	    numInfected[u] += 1
	    
	# Print the output of all individuals, unsorted
	for u in numInfected:
		print("%s\t%d" % (u, numInfected[u]))

	return numInfected


def matchInfectorCounts(infectionsDict: dict, infectorsList: list) -> list:
	"""
	Matches the infectors in a user inputted list to their corresponding
	infection count.

	Returns the list with these counts, maintaing the original order.

	Parameters
	----------
	infectionsDict - a dict with keys as infectors and values as
					 their infection counts
	infectorsList - a list of infectors ordered by the user's algorithm
	"""

	infectorsCount = []

	for infector in infectorsList:
		infectorsCount.append(infectionsDict[infector])

	return infectorsCount


def calculateTauB(unsortedList: list, userList: list) -> (int, int):
	"""
	Calculates the Kendall Tau B correlation coefficient between two 
	lists, assuming that the first one, after being sorted in reverse
	order, is the most optimal list. 

	Returns a tuple (calculated tau coefficient, p-value)

	Parameters
	----------
	unsortedList - the first list to be compared to, with
			      assumed 100% accuracy after being sorted
	userList - a list ordering infection counts - generated by the 
			   user's algorithm

	The two lists MUST be the same size.
	"""

	correctList = sorted(unsortedList, reverse=True)

	tau, pValue = stats.kendalltau(correctList, userList)

	print("The correlation coefficient is:", tau)
	print("The pvalue for this is:", pValue)

	return (tau, pValue)

