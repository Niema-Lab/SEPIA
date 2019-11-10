#!/usr/bin/env python3
"""
File implements a script where the user can match their own prioritization ordering of 
individuals with their actual infection counts based on tranmission history data. 
"""


from orderCheck import countInfections, matchInfectorCounts


if __name__ == "__main__":
    # parse user arguments [-h] [-i INPUT] [-o OUTPUT] -t TRANMSISSIONHIST -s START [-e END]
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File - User's Ordering")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    parser.add_argument('-t', '--tranmsissionHist', required=True, type=str, help='Tranmission History File')
    parser.add_argument('-s', '--start', required=True, type=float, help='Time Start')  
    parser.add_argument('-e', '--end', required=False, type=float, default=float('inf'), help='Time End') # end defaults to infinity

    args = parser.parse_args()

    # handle input and and output, save into infile and outfile vars
    if args.input == 'stdin':
        from sys import stdin; infile = stdin
    elif args.input.lower().endswith('.gz'):
        from gzip import open as gopen; infile = gopen(args.input)
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout; outfile = stdout
    else:
        outfile = open(args.output,'w')

    # Create a dictionary matching individuals to infection counts using tranmission history data
    infectionsDict = countInfections(open(args.tranmsissionHist, "r"), args.start, args.end)

    # Read the user's ordering and print a file with individuals and their counts in the same order
    matchInfectorCounts(infectionsDict, infile, outfile)

    infile.close(); outfile.close()