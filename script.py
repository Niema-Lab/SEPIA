import subprocess
import sys
subprocess.call(['tdcl', '-t', sys.argv[1], '-s', sys.argv[2], '-l', sys.argv[3], '-o', sys.argv[4]])
