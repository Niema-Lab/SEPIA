#!/usr/bin/env python3
"""
File implements several methods used in compute_efficiency.py and compute_taub.py
"""
from gzip import open as gopen
from sys import stderr
import scipy
import scipy.stats as stats # run 'pip install scipy' in your terminal


def pairCounts(transmissionHist, lowerBound: int, upperBound: int, metric: int) -> dict:
        """
        Pairs each individual with a count value, where a higher count value indicates
        that an individual has a higher priority. Count values are calculated based
        on the corresponding chosen metric.

        There are currently four metrics to choose from:
        Metric 1 - TODO , short summaries of each metric
        Metric 2 - 
        Metric 3 - 
        Metric 4 - 
        
        Returns a dictionary where each key is an individual and their value
        is their corresponding count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the 
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        metric - int, specifies the chosen metric
        """

        # call the function corresponding to the chosen metric
        if (metric == 1):
            return directTransmissions(transmissionHist, lowerBound, upperBound)
        elif (metric == 2):
            return bestfitGraph(transmissionHist, lowerBound, upperBound)
        elif (metric == 3):
            return indirectTransmissions(transmissionHist, lowerBound, upperBound)
        elif (metric == 4):
            return totalTransmissions(transmissionHist, lowerBound, upperBound)


    
def directTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        Counts the number of times each individual infected someone else in a file.     
        
        Returns a dictionary where each key is an individual and their value
        is their corresponding infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the 
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """
        
        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1
            
        """
        # Print the output of all individuals, unsorted
        for u in numInfected:
                print("%s\t%d" % (u, numInfected[u]))
        """

        return numInfected


def bestfitGraph(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        TODO metric 2 - Titan  
        
        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the 
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """
        
        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1

        return numInfected


def indirectTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        TODO metric 3 - Mckenna   
        
        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the 
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """
        
        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1

        return numInfected


def totalTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        TODO metric 4 - Tyler/Kim, after Mckenna is done with metric 3   
        
        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the 
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """
        
        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1

        return numInfected


def matchInfectorCounts(infectionsDict: dict, inputOrder, outfile) -> None:
        """
        Matches the infectors in a user inputted file to their corresponding
        infection count. Returns void.

        Outputs lines with the format: "<individual> <count>", 
        maintaing the original order of individuals in input.

        Parameters
        ----------
        infectionsDict - a dict with keys as infectors and values as
                                         their infection counts
        infile - a file with the user's ordering of individuals
        outfile - a file where each line of output is written
        """

        for line in inputOrder:

                p = line.strip()

                if p not in infectionsDict.keys():
                        outfile.write("%s\t0\n" % p)

                else:
                        outfile.write("%s\t%d\n" % (p, infectionsDict[p]))


def calculateTauB(userOrder, outfile, reverse: bool) -> None:
        """
        Calculates the Kendall Tau B correlation coefficient between user ordering
        and most optimal ordering, assuming that the counts of individuals in 
        infile sorted is the most optimal. 
        Outputs coefficient and pvalue in the following format: "<tau> <pvalue>".
        Returns void.

        Parameters
        ----------
        infile- a file containing an ordering of infectors and their counts - 
                        generated by the user's algorithm
        outfile - the file the tau and pvalue are outputted
        reverse - bool, true if user's ordering is compared to order sorted descending,
                                        false if comparing to order sorted ascending
        """
        optimalOrder = sorted(userOrder, reverse=reverse)
        #print(userOrder, "\n")
        tau, pvalue = stats.kendalltau([e[0] for e in optimalOrder], [e[0] for e in userOrder])

        outfile.write("%s\t%s\n" % (tau, pvalue))

