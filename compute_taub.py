#!/usr/bin/env python3
"""
File implements a script where the user can calculate the Kendall Tau B correlation coefficient 
between their ordering and most optimal ordering, assuming that the counts of individuals in 
inputted file sorted is the most optimal. 
"""


from orderCheck import calculateTauB


if __name__ == "__main__":
    # parse user arguments [-h] [-i INPUT] [-o OUTPUT] [-r]
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File - User's Ordering")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    parser.add_argument('-r', '--reverse', action='store_true', help='Sort in Ascending Order')

    args = parser.parse_args()

    # handle input and and output, save into infile and outfile vars
    if args.input == 'stdin':
        from sys import stdin; efficacy = [[v.strip() for v in l.strip().split('\t')] for l in stdin.read().strip().splitlines()]
    elif args.input.lower().endswith('.gz'):
        from gzip import open as gopen; efficacy = [[v.strip() for v in l.strip().split('\t')] for l in gopen(args.input).read().decode().strip().splitlines()]
    else:
        efficacy = [[v.strip() for v in l.strip().split('\t')] for l in open(args.input).read().strip().splitlines()]
    for i in range(len(efficacy)):
        if len(efficacy[i]) != 2:
            raise ValueError("Input must be efficacy file (TSV with 2 columns: PERSON<TAB>EFFICACY")
        efficacy[i] = (float(efficacy[i][1]), efficacy[i][0])
    if args.output == 'stdout':
        from sys import stdout; outfile = stdout
    else:
        outfile = open(args.output,'w')

    descendingSort = True
    # user wants to compare their ordering theirs sorted in ascending order
    if args.reverse:
        descendingSort = False
    
    calculateTauB(efficacy, outfile, descendingSort)
    outfile.close()


