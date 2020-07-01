# SEPIA - SIMULATION-BASED EVALUATION OF PRIORITIZATION ALGORITHMS

SEPIA is a framework for comparing the accuracies of algorithms that prioritize individuals by risk of transmitting HIV (Human Immunodeficiency Virus).

## Installation Guide
SEPIA was written in Python 3 and is intended to be used through the bash interface.

-___Installation:___- Clone the master git repository

-___Dependencies to install:___-
```
sudo apt-get update
sudo apt-get install python3-pip
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
pip3 install seaborn
```
-___External Packages to install:___- Located in ```efficacy_functions.py```.
```
from gzip inport open as gopen
from sys import stderr
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from itertools import repeat
```

## Methods

### Functions

- ___compute_efficacy.py___ - matches all individuals in the user's ordering along with the number of people each individual infected during a specified period of time. The user's ordering is maintained.

```
usage: [-h] [-m METRIC] [-i INPUT] [-o OUTPUT] [-t TRANMSISSIONHIST] [-c CONTACTNET] [-s START] [-e END]
  
  -h, --help            show this help message and exit
  
  -m METRIC, --metric METRIC
                        Metric of prioritization (1-6) (default: None)
  -i INPUT, --input INPUT
                        Input File - User's Ordering (default: stdin)
  -o OUTPUT, --output OUTPUT
                        Output File (default: stdout)
  -t TRANMSISSIONHIST, --tranmsissionHist TRANMSISSIONHIST
                        Tranmission History File (default: None)
  -c CONTACTNET, --contactNet CONTACTNET
                        Contact History File (default: None)
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

- __make_violinplots.py__ - creates 9 violin plot figures in ```\figs```, each with with 2 violin plots. Each figure represents an experimental condition, and each of the 2 plots represent either ProACT or HIV-TRACE.

-__efficacyFunctions.py__- defines several functions used in the scripts above.

## **Metrics**

We will use four distinct metrics to generate optimal orderings. Each metric defines a unique way of calculating the count values of individuals, such that individuals with higher count values will have higher priority in the ordering.

The six currently proposed metrics are as follows:

### **1. Direct Transmissions**
In this metric, each individual's count is calculated as the number of individuals (**_n_**) they have directly transmitted HIV to, formally represented as: 

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/metric1_formula.PNG)

The below figure illustrates an example transmission network:

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/Slide1.JPG)

In this example, Person A has four outgoing edges, indicating that Person A transmitted HIV to four people and has a direct transmission count of 4. Similarly, Person B has no outgoing edges, so Person B's count is 0.

### **2. Best Fit Graph**
In this metric, each individual's count is calculated as the slope of a best-fit line plotted in a step graph of all of the individual's outgoing transmissions over a specified time period on the horizontal axis. The line of best-fit starts at the event of the individual first transmitting HIV to someone else; this aims to prioritize individuals that transmit HIV to more people over a short time period, as they will have steeper slopes. 

With this metric, we hope to take into account that individuals who transmit HIV to others more recently should have higher priority than individuals who transmitted HIV to others longer ago.  

The following figure shows the resulting lines of best-fit for two cases: 

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/Slide3.JPG)

The graph on the left represents a case in which the individual started transmitting HIV more recently, whereas the graph on the right represents a case in which the individual had multiple outgoing transmissions early in the time period but stopped towards the middle. This design thus gives higher priority to the individual represented by the left side with multiple recent outgoing transmissions, as their slope is greater.

### **3. Indirect Transmissions**
With this metric, we want to extend Metric 1 such that we are now analyzing an individual's greater effect on the community. 

Each individual's count is calculated as the number of individuals they indirectly transmitted HIV to. More specifically, we count the number of individuals directly transmitted HIV to by this individual's partners. If Person _A_ transmitted HIV to Person _B_, Person _B_ transmitted HIV to Person _C_ and Person _D_, and Person _C_ transmitted HIV to Person _E_, Person _A_'s count would be 2, which is calculated by counting Person _C_ and Person _D_.

Let an individual transmit HIV to **_n_** individuals, where each is an individual **_i_** from  1,2,...,**_n_**, and let **_n_**<sub>i</sub> be the number of individuals that individual **_i_** has transmitted. Thus, their count will be formally calculated as: 

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/metric3_formula.PNG)

### **4. Total Transmissions** 
With this metric, we want to merge Metric 1 and Metric 3, such that we take into account both an individual's direct and indirect transmissions. 

Each individual's count is calculated as the number of individuals they directly and indirectly transmitted HIV to. More specifically, we count the number of individuals that directly transmitted HIV by this individual added to the number of individuals directly transmitted by this individual's partner's. If Person _A_ transmitted HIV to Person _B_, Person _B_ transmitted HIV to Person _C_ and Person _D_, and Person _C_ transmitted HIV to Person _E_, Person _A_'s count would be 3, which is calculated by counting Person _B_, Person C_, and Person _D_.

Let an individual transmit HIV to **_n_** individuals, where each is an individual **_i_** from 1,2...**_n_**, and let **_n_**<sub>i</sub> be the number of individuals individual **_i_** has transmitted HIV to. Thus, the count will be formally calculated as:

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/metric4_formula.PNG)

### **5. Number of Contacts**:
With this metric, we find the number of contacts an individual has.

Each individual's count for their number of contacts is found through totaling the number of contacts they have from themselves to another individual. If Person _A_ had Person _B_ and Person _C_ in their contact network, Person _A_ would have a count of 2. 

Let an individual have contact with **_n_** individuals, where each is an individual **_i_** from 1,2...**_n_**. Thus, the count will be formally calculated as:

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/metric1_formula.PNG)

### **6. Number of Contacts and Transmissions**
This metric combines Metrics 1 and 5 in order to take into account both each individual's number of direct transmissions and number of contacts. 

