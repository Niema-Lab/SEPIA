# erspMeasure

A tool to evaluate the accuracy of a list that prioritizes individuals with HIV from greatest to least based on their likelihood to spread HIV.

### Important files

- ___compute_efficacy.py___ - matches all individuals in the user's ordering along with the number of people each individual infected during a specified period of time. The user's ordering is maintained.

```
usage: [-h] -m METRIC [-i INPUT] [-o OUTPUT] [-t TRANMSISSIONHIST] [-c CONTACTNET] -s START [-e END]
    -h, --help            show this help message and exit
  -m METRIC, --metric METRIC
                        Metric of prioritization (1-6) (default: None)
  -i INPUT, --input INPUT
                        Input File - User's Ordering (default: stdin)
  -o OUTPUT, --output OUTPUT
                        Output File (default: stdout)
  -t TRANMSISSIONHIST, --tranmsissionHist TRANMSISSIONHIST
                        Tranmission History File (default: )
  -c CONTACTNET, --contactNet CONTACTNET
                        Contact History File (default: )
  -s START, --start START
                        Time Start (default: None)
  -e END, --end END     Time End (default: inf)

```

- ___compute_taub.py___ - computes the Kendall Tau-b correlation coefficient between the user's ordering and the optimal ordering (which is sorted in descending order).

```
usage: [-h] [-i INPUT] [-o OUTPUT] [-r]
  -h, --help            Show the help message and exit
  -i INPUT, --input INPUT
                        Input File (User ordering of individuals paired with their counts) 
                        (default: stdin)
  -o OUTPUT, --output OUTPUT
                        Output File (Tau-b correlation coefficient, along with calculated p-value)
                        (default: stdout)

  -r 
                        Reverses the optimal ordering if flag set. (Optimal ordering is sorted in 
                        ascending order).
```

- __make_violinplots.py__ - creates 9 violin plot figures in figures/, each with with 2 violin plots. Each figure represents an experimental condition, and each of the 2 plots represent either ProACT or HIV-TRACE.

- _efficacyFunctions.py_ - defines several functions used in the scripts above.
