#!/usr/bin/env python3
"""
File implements a script where the user can match their own prioritization ordering of
individuals with their actual infection counts based on tranmission history data.
"""

from efficacyFunctions import *
import argparse


# parse user arguments  [-h] -m METRIC [-i INPUT] [-o OUTPUT] [-t TRANMSISSIONHIST] [-c CONTACTNET] -s START [-e END]
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-m', '--metric', required=True, type=float, help="Metric of prioritization (1-6)")
parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File - User's Ordering")
parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
parser.add_argument('-t', '--tranmsissionHist', required=False, type=str, default='', help='Tranmission History File')
parser.add_argument('-c', '--contactNet', required=False, type=str, default='',  help='Contact History File')
parser.add_argument('-s', '--start', required=True, type=float, help='Time Start')
parser.add_argument('-e', '--end', required=False, type=float, default=float('inf'), help='Time End') # end defaults to infinity

args = parser.parse_args()

# handle input and and output, save into infile and outfile vars
if args.input == 'stdin':
    from sys import stdin; order = [l.strip() for l in stdin]
elif args.input.lower().endswith('.gz'):
    from gzip import open as gopen; order = [l.strip() for l in gopen(args.input).read().decode().strip().splitlines()]
else:
    order = [l.strip() for l in open(args.input).read().strip().splitlines()]
if args.output == 'stdout':
    from sys import stdout; outfile = stdout
else:
    outfile = open(args.output,'w')

# Create a dictionary matching individuals to infection counts using tranmission history data
infectionsDict = pairCounts(args.tranmsissionHist, args.contactNet, args.start, args.end, args.metric)

# Read the user's ordering and print a file with individuals and their counts in the same order
matchInfectorCounts(infectionsDict, order, outfile, args.metric)
outfile.close()