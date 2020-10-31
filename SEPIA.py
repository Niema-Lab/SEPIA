#!/usr/bin/env python3
"""
File takes in a priortization ordering and runs through the SEPIA workflow
to output the  Kendall Tau B correlation coefficient between their ordering 
and the most optimal ordering, as generated by the chosen metric.

If verbose flag is specified, intermediate data in the process can be outputted to stderr.
"""


import scipy.stats as stats 
import math
import argparse

from efficacyFunctions import *


def calculateTauB(userOrder) -> None:
        """
        Calculates the Kendall Tau B correlation coefficient between user ordering
        and most optimal ordering.

        Outputs coefficient and pvalue in the following format: "<tau> <pvalue>".
        Returns void.

        Parameters
        ----------
        userOrder- an ordering of infectors and their counts
                   - generated by the user's algorithm
        outfile - the file the tau and pvalue are outputted
        """

        optimalOrder = list(range(len(userOrder), 0, -1))

        tau, pvalue = stats.kendalltau(optimalOrder, userOrder)

        print("%s\t%s\n" % (tau, pvalue))


# parse user arguments  [-h] -m METRIC [-i INPUT] [-t TRANMSISSIONHIST] [-c CONTACTNET] -s START [-e END] [-v]
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-m', '--metric', required=True, type=float, help="Metric of prioritization (1-6)")
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File - User's Ordering")
parser.add_argument('-t', '--tranmsissionHist', required=False, type=str, default='', help='Tranmission History File')
parser.add_argument('-c', '--contactNet', required=False, type=str, default='',  help='Contact History File')
parser.add_argument('-s', '--start', required=True, type=float, help='Time Start')
parser.add_argument('-e', '--end', required=False, type=float, default=float('inf'), help='Time End') # end defaults to infinity
parser.add_argument('-v', '--verbose', required=False, action='store_true', help='Print Intermediate List with Individuals Matched to Counts')
args = parser.parse_args()

# handle input, save into infile var
if args.input == 'stdin':
    from sys import stdin; order = [l.strip() for l in stdin]
elif args.input.lower().endswith('.gz'):
    from gzip import open as gopen; order = [l.strip() for l in gopen(args.input).read().decode().strip().splitlines()]
else:
    order = [l.strip() for l in open(args.input).read().strip().splitlines()]


# Create a dictionary matching individuals to infection counts using tranmission history data
infectionsDict = pairCounts(args.tranmsissionHist, args.contactNet, args.start, args.end, args.metric)

# Read the user's ordering and create a list of tuple pairs with individuals and their respective counts in the same order
countsList = matchInfectorCounts(infectionsDict, order)

# output verbose to sdterr if verbose flag was specified
if args.verbose:
    print(countsList, stderr)

# calculate and output Tau B to stdout
calculateTauB([x[1] for x in countsList])

