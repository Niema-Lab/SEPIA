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
        from sys import stdin; infile = stdin
    elif args.input.lower().endswith('.gz'):
        from gzip import open as gopen; infile = gopen(args.input)
    else:
        infile = open(args.input)
    if args.output == 'stdout':
        from sys import stdout; outfile = stdout
    else:
        outfile = open(args.output,'w')

    descendingSort = True
    # user wants to compare their ordering theirs sorted in ascending order
    if args.reverse:
        descendingSort = False
    
    calculateTauB(infile, outfile, descendingSort)

    infile.close(); outfile.close()


