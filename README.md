# SEPIA - SIMULATION-BASED EVALUATION OF PRIORITIZATION ALGORITHMS

SEPIA is a framework for comparing the accuracies of algorithms that prioritize individuals by risk of transmitting HIV (Human Immunodeficiency Virus).

## Software Dependencies
SEPIA is written in Python 3 and requires modules **numpy**, **scipy**, and **matplotlib**, all of which are easily installed using Python package installer **pip**.

## Installation


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

### Installation Guide
SEPIA was made with Python 3.6.9 on Ubuntu.

-___Installation:___- Clone the master git repository

-___Dependencies to install:___-
```
sudo apt-get update
sudo apt-get install python3-pip
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
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
=======

## **Metrics**

We will use four distinct metrics to generate optimal orderings. Each metric defines a unique way of calculating the count values of individuals, such that individuals with higher count values will have higher priority in the ordering.

The six currently proposed metrics are as follows:

### **1. Direct Transmissions**
Each individual's count is calculated as the number of individuals they have directly transmitted HIV to. For example, if Person _A_ transmitted HIV to 4 people, Person _A_'s count would be 4.

Let an individual transmit HIV to **_n_**. Thus, their count will be formally calculated as:

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/metric1_formula.PNG)

The below figure illustrates Metrics 1, 3, and 4.

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/metric134_figure.PNG)

### **2. Best Fit Graph**
With this metric, we hope to take into account that individuals who transmit HIV to others more recently should have higher priority than individuals who transmitted HIV to others longer ago. 

Each individual's count is calculated as the slope of a best-fit line. This line is plotted as the best-fit to a step graph that includes all of this individual's outgoing transmissions plotted over time on the horizontal axis. The line of best-fit for an individual starts at the time the individual first transmitted HIV to someone else. People that transmit HIV to the most individuals over a short time period from the time of their first transmission will have the steepest slopes. Therefore, we generate an ordering that puts individuals with steeper slopes closer to the front of the list. 

The figure is not accurate in terms of how the line of best-fit will be drawn relative to the step graph.

![](https://github.com/ERSP-HIV-Phylogenetics-and-Transmission/SEPIA/blob/master/assets/images/metric2_figure.PNG)

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

![](https://github.com/Moshiri-Lab/SEPIA/blob/master/transmission_network.JPG)
