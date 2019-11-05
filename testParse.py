from collections import OrderedDict
# Open this file. specify a file from user args
f = open("01.transmissions.txt", "r")

infectedPersons=[]
people = []

num_infected = dict()
# Loop over each line in the file.
for line in f.readlines():
    u,v,t = line.split('\t')
    u = u.strip()
    v = v.strip()
    lower_bound = 0
    upper_bound = 5

    # Only considers infections within a given range of years
    if (lower_bound > float(t)) | (float(t) > upper_bound):
        continue

    if u not in num_infected:
        num_infected[u] = 0
    num_infected[u] += 1
    
# Sort the dictionary
num_infected = OrderedDict(sorted(num_infected.items(), key=lambda x: x[1]))

# Get a list of the dictionary and create a dict to store the most infectious people
top_num_infected = dict()
infected_list = list(num_infected.items())

# Get the top 10 most infectious people in the dict
i = 0
for infected in infected_list:
    # Take only the top 10 elements
    if i == 11:
        break
    
    # Removes the value of none
    if infected_list[len(infected_list) - 1 - i][0] == 'None':
        i = i + 1
        continue

    # Add the top infected to the dictionary
    top_num_infected[i] = infected_list[len(infected_list) - 1 - i]
    i = i + 1
   

# Print the dictionary
print(top_num_infected)
