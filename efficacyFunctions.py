#!/usr/bin/env python3
"""
File implements several methods used in compute_efficiency.py.
"""

# EXTERNAL MODULES
from gzip import open as gopen
from sys import stderr
import numpy as np
import scipy.stats as stats # run 'pip install scipy' in your terminal
import scipy
import matplotlib.pyplot as plt
from itertools import repeat

# CONSTANTS
NUM_POINTS_PER_STEP = 10
METRIC1 = 1; METRIC2 = 2; METRIC3 = 3; METRIC4 = 4
TAB_CHAR = '\t'


def pairCounts(transmissionHist, lowerBound: int, upperBound: int, metric: int) -> dict:
        """
        Pairs each individual with a count value, where a higher count value indicates
        that an individual has a higher priority. Count values are calculated based
        on the corresponding chosen metric.

        There are currently four metrics to choose from.

        Returns a dictionary where each key is an individual and their value
        is their corresponding count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of time range
        upperBound - upper bound of timerange
        metric - int, specifies the chosen metric
        """

        # call the function corresponding to the chosen metric
        if (metric == METRIC1):
            return directTransmissions(transmissionHist, lowerBound, upperBound)
        elif (metric == METRIC2):
            return bestfitGraph(transmissionHist, lowerBound, upperBound)
        elif (metric == METRIC3):
            return indirectTransmissions(transmissionHist, lowerBound, upperBound)
        elif (metric == METRIC4):
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

        infectedPersons= []; people = []; numInfected = dict()
        lines = opengzip(transmissionHist)

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split(TAB_CHAR)
            u = u.strip(); v = v.strip()

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
        Returns a dictionary where each key is an individual and their value
        is their corresponding count as calculated by the slope linear regression
        of their transmissions over time.

        If the upperBound was not specified when running the script, it defaults
        to being the time of the latest transmission.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of time range
        upperBound - upper bound of time range
        """

        infectedPersons= []; people = []
        # build timesInfected, a dict where each person is
        # matched up with a list of times at which they transmitted
        timesInfected = dict() 
        lines = opengzip(transmissionHist)

        # Deal with upper bound setting
        isUpperBoundSet = True; latestInfectionTime = -1;
        # Check if an upper bound for time was set
        if upperBound == float('inf'):
            isUpperBoundSet = False
        else:
            latestInfectionTime = upperBound

        # Loop over each line in the transmissions file to build timesInfected
        for line in lines:
            u,v,t = line.split(TAB_CHAR)
            u = u.strip(); v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in timesInfected:
                timesInfected[u] = []

            # Append this time to u's list
            timesInfected[u].append(float(t))

            # Keep iterating to get the globally latest infection time
            if not isUpperBoundSet and float(t) > latestInfectionTime:
                latestInfectionTime = float(t)

        # Build a dict with users as keys paired with their slopes
        slopesDict = dict()

        # Loop over all transmitters
        for u in timesInfected:
            # Build two lists, one with xCoordinates and 
            # one with yCoordinates, for linear regression
            x = np.empty(1); y = np.empty(1)

            # Gets times of transmissions for transmitter u
            times = timesInfected[u] 

            # Plot up to the first transmission time, step 0
            step = np.linspace(lowerBound, times[0], NUM_POINTS_PER_STEP, endpoint=True)
            x = np.append(x, step)
            y = np.append(y, list(repeat(0, NUM_POINTS_PER_STEP)))

            # Loop over all the transmission times of u
            for i in range(len(times)):

                # At the last step (to the upperBound), 
                # only plot the start point and then up to the latest time of 
                # infection globally OR plot up to upperBound if its set
                if (i == len(times) - 1):
                    step = np.linspace(times[i], latestInfectionTime, 
                                       NUM_POINTS_PER_STEP, endpoint=True)
                    x = np.append(x, step)
                    y = np.append(y, list(repeat(i + 1, NUM_POINTS_PER_STEP)))
                    break

                # plot the xcoords of this step
                step = np.linspace(times[i], times[i+1], NUM_POINTS_PER_STEP, endpoint=True)
                x = np.append(x, step)

                # plot the ycoords of this step
                y = np.append(y, list(repeat(i + 1, NUM_POINTS_PER_STEP)))

            linregress = stats.linregress(x, y)
            slopesDict[u] = linregress.slope

            # TESTING - Plot the points and the best fit
            # if (u == 'CNG0-COM1-4332'):
                # plt.plot(x, y, 'o')
                # plt.plot(x, float(linregress.intercept) + linregress.slope*x, 'r')
                # plt.show()

        return slopesDict


def indirectTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """

        infectedPersons= []; people = []; numInfected = dict()
        lines = opengzip(transmissionHist)

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split(TAB_CHAR)
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

        numIndirect = dict()

        for line in lines:
            u,v,t = line.split(TAB_CHAR)
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numIndirect:
                numIndirect[u] = 0

            # should get the number of people that were indirectly impacted
            if v in numInfected:
                numIndirect[u] += numInfected.get(v)

        return numIndirect


def totalTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """

        infectedPersons= []; people = []; numInfected = dict()
        lines = opengzip(transmissionHist)

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split(TAB_CHAR)
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

        numIndirect = dict()

        for line in lines:
            u,v,t = line.split(TAB_CHAR)
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numIndirect:
                numIndirect[u] = 0

            # should get the number of people that were indirected impacted
            if v in numInfected:
                numIndirect[u] += numInfected.get(v)

        numTotal = dict()

        # go through loop
        for person in numInfected:

            if person not in numTotal:
                numTotal[person] = 0

            if person in numInfected:
                numTotal[person] += numInfected[person]
            if person in numIndirect:
                numIndirect[person]

        return numTotal


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
                        outfile.write("%s\t%f\n" % (p, infectionsDict[p]))


def opengzip(transmissionHist):
        """
        Helper method - Opens a gzip and returns the lines of the file.

        Parameters
        ----------
        transmissionHist - the gzip to open. the file object with data on 
                           tranmissions.
        """
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        return lines