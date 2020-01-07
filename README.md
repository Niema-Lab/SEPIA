# erspMeasure

A tool to evaluate the accuracy of a list that prioritizes infectors from greatest to least.

### Important files

- ___compute_efficacy.py___ - matches all individuals in the user's ordering along with the number of people each individual infected during a specified period of time. The user's ordering is maintained.

```
usage: [-h] [-i INPUT] [-o OUTPUT] [-t TRANMSISSIONHIST] [-s START] [-e END]
  -h, --help            Show the help message and exit
  -i INPUT, --input INPUT
                        Input File (User ordering of individuals)
                        (default: stdin)
  -o OUTPUT, --output OUTPUT
                        Output File (User ordering of individuals paired with their counts)
                        (default: stdout)
  -t TRANSMISSIONHIST
                        Transmission History File 
                        (Logs every infection between every pair of individuals)            
  -s START
                        Start time
  -e END
                        End time 
                        (default: infinity)
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

- _orderCheck.py_ defines several functions used in the scripts above.
