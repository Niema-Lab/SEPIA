from collections import OrderedDict
# Open this file. specify a file from user args
f = open("01.practiceTransmission.txt", "r")

infectedPersons=[]
people = []

num_infected = dict()
# Loop over each line in the file.
for line in f.readlines():
    u,v,t = line.split('\t')
    u = u.strip()
    v = v.strip()
    lower_bound = 0
    upper_bound = 9

    # why does this not work?
    #if lower_bound <= float(t) <= upper_bound:

    if u not in num_infected:
        num_infected[u] = 0
    num_infected[u] += 1
    

num_infected = OrderedDict(sorted(num_infected.items(), key=lambda x: x[1]))
print(num_infected)
