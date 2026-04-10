# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:17:41 2026

@author: Dirk Held
"""

# This is a project about the U.S Medical Insurance Data.
# The data given is a csv file with:
    # age - the age of the person
    # sex - the gender of the person (male/female)
    # bmi - the bmi of the person
    # children - how many children the person has
    # smoker - if the person smokes
    # region - the region the person is from (northeast, southeast, southwest,
    # northwest)
    # charges - how much the person is paying for the insurance

# Setting goals:
    # 1: I want to get some key information from the data.
    # The range of each data.
    # Which entry has the lowest and highest charges.
    # How many people are in a certain group, average costs,
    # minimum and maximum costs.
    # 2: I want to find out, what has the most influence on the insurance costs
    # and how this factor influences other key factors.

# import the data and transform it in a list of dictionaries
import csv

with open("insurance.csv") as insurance_data:
    data_list = list(csv.DictReader(insurance_data))

# To find out how many datasets are there, we print the length of the data_list
print("There are " + str(len(data_list)) + " datasets in the file.")
# There are 1338 datasets in the file.

# generate for each key a list
age = []
sex = []
bmi = []
children = []
smoker = []
region = []
charges = []
for entry in data_list:
    age.append(entry["age"])
    sex.append(entry["sex"])
    bmi.append(entry["bmi"])
    children.append(entry["children"])
    smoker.append(entry["smoker"])
    region.append(entry["region"])
    charges.append(entry["charges"])

# find the minimum and maximum and average for age, bmi and children
# later I can use age-groups, bmi-groups and children-groups

# define a function to find the minimum, maximum and average
# and return them in a list
def find_min_max_avg(category):
    """input: a list (e.g. age, sex, ...).
    return the min, max, average and the middle of the range in a list"""
    minimum = float("inf")
    maximum = 0.0
    total = 0
    for entry in category:
        if float(entry) < float(minimum):
            minimum = float(entry)
        if float(entry) > float(maximum):
            maximum = float(entry)
        total += float(entry)
    average = round(total / len(category), 2)
    middle = round((minimum + maximum)/2,2)
    min_max = [minimum, maximum, average, middle]
    return min_max

# find the minimum, maximum and average from age, bmi, children and charges
# and printing the result
min_max_age = find_min_max_avg(age)
print("\nThe age has a range from " + str(min_max_age[0]) +
      " to " + str(min_max_age[1]) + "\nThe average age is " +
      str(min_max_age[2]) + ". And the middle is "+ str(min_max_age[3]))
# The age has a range from 18.0 to 64.0
# The average age is 39.21. And the middle is 41.0
min_max_bmi = find_min_max_avg(bmi)
print("The BMI has a range from " + str(min_max_bmi[0]) +
      " to " + str(min_max_bmi[1]) + "\nThe average bmi is " +
      str(min_max_bmi[2]) + ". And the middle is "+ str(min_max_bmi[3]))
# The BMI has a range from 15.96 to 53.13
# The average bmi is 30.66. And the middle is 34.55
min_max_children = find_min_max_avg(children)
print("The amount of children has a range from " +
      str(min_max_children[0]) + " to " + str(min_max_children[1]) +
      "\nThe average amount of children is " +
      str(min_max_children[2]) + ". And the middle is " +
      str(min_max_children[3]))
# The amount of children has a range from 0.0 to 5
# The average amount of children is 1.09. And the middle is 2.5
min_max_charges = find_min_max_avg(charges)
print("The charges have a range from " +
      str(min_max_charges[0]) + " to " + str(min_max_charges[1]) +
      "\nThe average charge " +
      str(min_max_charges[2]) + ". And the middle is " +
      str(min_max_charges[3]))
# The charges have a range from 1121.8739 to 63770.42801
# The average charge 13270.42. And the middle is 32446.15

# To find out more, I will look to the min and max value for costs.
# Which values create the min and max cost entry?
# I iterate through the charges to find the position of the min and max entry.
# then I print the other keys with that position
counter = 0
print("\n")
for entry in charges:
    if float(entry) == min_max_charges[0]:
        print("The entry with the lowest cost has the following values:\n" +
              "age, sex, bmi, children smoker, region, charges:\n" +
              age[counter], sex[counter], bmi[counter], children[counter],
              smoker[counter], region[counter], charges[counter])
    if float(entry) == min_max_charges[1]:
        print("The entry with the highest cost has the following values:\n" +
              "age, sex, bmi, children smoker, region, charges:\n" +
              age[counter], sex[counter], bmi[counter], children[counter],
              smoker[0], region[counter], charges[counter])
    counter += 1
# The entry with the highest cost has the following values:
# age, sex, bmi, children smoker, region, charges:
# 54 female 47.41 0 yes southeast 63770.42801
# The entry with the lowest cost has the following values:
# age, sex, bmi, children smoker, region, charges:
# 18 male 23.21 0 no southeast 1121.8739
# In this both extreme costs the region and number of children are the same.

# I will divide each key in smaller groups to see how they influence the costs.

# age groups: 18-24, 25-44, 45-54, >= 55
AGE1 = 0
AGE2 = 25
AGE3 = 45
AGE4 = 55
AGE5 = float("inf")

# bmi groups according to common classification of:
    # underweight <18.5
    # normal weight 18.5 - 24.9
    # overweight 25.0 - 29.9
    # obesity class 1 30.0 - 34.9
    # obesity class 2+3 >= 35
BMI1 = 0
BMI2 = 18.5
BMI3 = 25
BMI4 = 30
BMI5 = 35
BMI6 = float("inf")

# I calculate the average costs for each group
# I define a function to find the amount of people and the average
# cost in a range of a group with numeric values
# like age, bmi and number of children.

def group_costs_num(low_limit, up_limit, category, charge):
    """input: the lower and upper limit for the tange of age, bmi
    or amount of children, a list with numerical values (age, bmi, ...)
    and a list with the charges.
    returning: the people count, the avgerage cost for group 
    and the percentage this group has of the total"""
    people = 0
    total_cost = 0
    counter = 0
    for entry in category:
        if float(entry) >= low_limit and float(entry) < up_limit:
            people += 1
            total_cost += float(charge[counter])
        counter += 1
    avg_cost = round(total_cost / people, 2)
    people_avgcost = [people, avg_cost, round(people/len(category)*100,2)]
    return people_avgcost

# find the average cost and amount of people for each age-group
age_1 = group_costs_num(AGE1, AGE2, age, charges)
age_2 = group_costs_num(AGE2, AGE3, age, charges)
age_3 = group_costs_num(AGE3, AGE4, age, charges)
age_4 = group_costs_num(AGE4, AGE5, age, charges)

# printing the results
print("\nThere are " + str(age_1[0]) + " people between " + str(AGE1) +
      " and " + str(AGE2-1) + 
      ". This are " + str(age_1[2]) + "% of people in the dataset." + 
      "\nThey have an average cost of " + str(age_1[1]) + " Dollar.")
# There are 278 people between 0 and 24.
# This are 20.78% of people in the dataset.
# They have an average cost of 9011.34 Dollar.
print("There are " + str(age_2[0]) + " people between " + str(AGE2) +
      " and " + str(AGE3-1) + 
      ". This are " + str(age_2[2]) + "% of people in the dataset." + 
      "They have an average cost of " + str(age_2[1]) + " Dollar.")
# There are 531 people between 25 and 44.
# This are 39.69% of people in the dataset.
# They have an average cost of 11714.47 Dollar.
print("There are " + str(age_3[0]) + " people between " + str(AGE3) +
      " and " + str(AGE4-1) + 
      ". This are " + str(age_3[2]) + "% of people in the dataset." + 
      "They have an average cost of " + str(age_3[1]) + " Dollar.")
# There are 287 people between 45 and 54.
# This are 21.45% of people in the dataset.
# They have an average cost of 15853.93 Dollar.
print("There are " + str(age_4[0]) + " people between " + str(AGE4) +
      " and " + str(AGE5-1) + 
      ". This are " + str(age_4[2]) + "% of people in the dataset." + 
      "\nThey have an average cost of " + str(age_4[1]) + " Dollar.")
# There are 242 people between 55 and inf.
# This are 18.09% of people in the dataset.
# They have an average cost of 18513.28 Dollar.

# average costs for female and male
# I am not changeing the sex-list in a numerical list
# because for this I need to iterate through the list
# but with iterating through the list I can already receive the
# results I want to have.

count_female = 0
cost_female = 0
count_male = 0
cost_male = 0
counter = 0
# Iterating through the list and counting the amount of femal/male and adding
# the charges for both genders.
for entry in sex:
    if entry == "female":
        count_female += 1
        cost_female += float(charges[counter])
    if entry == "male":
        count_male += 1
        cost_male += float(charges[counter])
    counter += 1

# calculate the average costs for female and printing the results
avg_cost_female = round(cost_female / count_female, 2)
print("\nThere are " + str(count_female) +
      " female in the dataset. This are " + 
      str(round(count_female/len(sex)*100)) + "% of people in the dataset.\n" +
      "They have an average cost of " + str(avg_cost_female) + " Dollar.")
# There are 662 female in the dataset.
# This are 49% of people in the dataset.
# They have an average cost of 12569.58 Dollar.

# calculate the average costs for male and printing the results
avg_cost_male = round(cost_male / count_male, 2)
print("There are " + str(count_male) +
      " male in the dataset. This are " + 
      str(round(count_male/len(sex)*100)) + "% of people in the dataset.\n" +
      "They have an average cost of " + str(avg_cost_male) + " Dollar.")
# There are 676 male in the dataset.
# This are 51% of people in the dataset.
# They have an average cost of 13956.75 Dollar.

# average cost for each bmi-group
bmi_1 = group_costs_num(BMI1, BMI2, bmi, charges)
bmi_2 = group_costs_num(BMI2, BMI3, bmi, charges)
bmi_3 = group_costs_num(BMI3, BMI4, bmi, charges)
bmi_4 = group_costs_num(BMI4, BMI5, bmi, charges)
bmi_5 = group_costs_num(BMI5, BMI6, bmi, charges)

# printing the results
print("\nThere are " + str(bmi_1[0]) +
      " people with under weight. This is " + str(bmi_1[2]) + 
      "% of people in the dataset"
      ".\nThey have an average cost of " + str(bmi_1[1]) + " Dollar.")
# There are 20 people with under weight.
# This is 1.49% of people in the dataset.
# They have an average cost of 8852.2 Dollar.
print("There are " + str(bmi_2[0]) +
      " people with normal weight. This is " + str(bmi_2[2]) + 
      "% of people in the dataset"
      ".\nThey have an average cost of " + str(bmi_2[1]) + " Dollar.")
# There are 225 people with normal weight.
# This is 16.82% of people in the dataset.
# They have an average cost of 10409.34 Dollar.
print("There are " + str(bmi_3[0]) +
      " people with overweight. This is " + str(bmi_3[2]) + 
      "% of people in the dataset"
      ".\nThey have an average cost of " + str(bmi_3[1]) + " Dollar.")
# There are 386 people with overweight.
# This is 28.85% of people in the dataset.
# They have an average cost of 10987.51 Dollar.
print("There are " + str(bmi_4[0]) +
      " people with obesity. This is " + str(bmi_4[2]) + 
      "% of people in the dataset"
      ".\nThey have an average cost of " + str(bmi_4[1]) + " Dollar.")
# There are 391 people with obesity.
# This is 29.22% of people in the dataset.
# They have an average cost of 14419.67 Dollar.
print("There are " + str(bmi_5[0]) +
      " people with extreme obesity. This is " + str(bmi_5[2]) + 
      "% of people in the dataset"
      ".\nThey have an average cost of " + str(bmi_5[1]) + " Dollar.")
# There are 316 people with extreme obesity.
# This is 23.62% of people in the dataset.
# They have an average cost of 16953.82 Dollar.

# average cost for differnent number of children
children_0 = group_costs_num(0, 1, children, charges)
children_1 = group_costs_num(1, 2, children, charges)
children_2 = group_costs_num(2, 3, children, charges)
children_3 = group_costs_num(3, 4, children, charges)
children_4 = group_costs_num(4, 5, children, charges)
children_5 = group_costs_num(5, float("inf"), children, charges)

# printing the results
print("\nThere are " + str(children_0[0]) +
      " people with 0 children. This is " + str(children_0[2]) + 
      "% of people in the dataset.\nThey have an average cost of " +
      str(children_0[1]) + " Dollar.")
# There are 574 people with 0 children.
# This is 42.9% of people in the dataset.
# They have an average cost of 12365.98 Dollar.
print("There are " + str(children_1[0]) +
      " people with 1 child. This is " + str(children_1[2]) + 
      "% of people in the dataset.\nThey have an average cost of " +
      str(children_1[1]) + " Dollar.")
# There are 324 people with 1 child.
# This is 24.22% of people in the dataset.
# They have an average cost of 12731.17 Dollar.
print("There are " + str(children_2[0]) +
      " people with 2 children. This is " + str(children_2[2]) + 
      "% of people in the dataset.\nThey have an average cost of " +
      str(children_2[1]) + " Dollar.")
# There are 240 people with 2 children.
# This is 17.94% of people in the dataset.
# They have an average cost of 15073.56 Dollar.
print("There are " + str(children_3[0]) +
      " people with 3 children. This is " + str(children_3[2]) + 
      "% of people in the dataset.\nThey have an average cost of " +
      str(children_3[1]) + " Dollar.")
# There are 157 people with 3 children.
# This is 11.73% of people in the dataset.
# They have an average cost of 15355.32 Dollar.
print("There are " + str(children_4[0]) +
      " people with 4 children. This is " + str(children_4[2]) + 
      "% of people in the dataset.\nThey have an average cost of " +
      str(children_4[1]) + " Dollar.")
# There are 25 people with 4 children.
# This is 1.87% of people in the dataset.
# They have an average cost of 13850.66 Dollar.
print("There are " + str(children_5[0]) +
      " people with 5 children. This is " + str(children_5[2]) + 
      "% of people in the dataset.\nThey have an average cost of " +
      str(children_5[1]) + " Dollar.")
# There are 18 people with 5 children.
# This is 1.35% of people in the dataset.
# They have an average cost of 8786.04 Dollar.

# average costs for smoker and non_smoker
count_smoker = 0
cost_smoker = 0
count_non_smoker = 0
cost_non_smoker = 0
counter = 0
# iterate thtough the smoker-list
for entry in smoker:
    # count the amount of smoker and sum their costs
    if entry == "yes":
        count_smoker += 1
        cost_smoker += float(charges[counter])
    # count the amount ofnon-smoker and sum their costs
    if entry == "no":
        count_non_smoker += 1
        cost_non_smoker += float(charges[counter])
    counter += 1
# calculate the average costs for smokers and non-smokers
avg_cost_smoker = round(cost_smoker / count_smoker, 2)
avg_cost_non_smoker = round(cost_non_smoker / count_non_smoker, 2)
# printing the amount of smoker / non-smokers and their average costs
print("\nThere are " + str(count_smoker) +
      " smoker in the dataset. This is " +
      str(round(count_smoker / len(smoker)*100,2)) +
      "% of people in the dataset." +
      "\nThey have an average cost of " + str(avg_cost_smoker) + " Dollar.")
# There are 274 smoker in the dataset.
# This is 20.48% of people in the dataset.
# They have an average cost of 32050.23 Dollar.
print("There are " + str(count_non_smoker) +
      " non-smoker in the dataset This is " +
      str(round(count_non_smoker / len(smoker)*100,2)) +
      "% of people in the dataset." +
      "\nThey have an average cost of " +
      str(avg_cost_non_smoker) + " Dollar.")
# There are 1064 non-smoker in the dataset
# This is 79.52% of people in the dataset.
# They have an average cost of 8434.27 Dollar.

# average cost for each region
count_region_1 = 0
cost_region_1 = 0
count_region_2 = 0
cost_region_2 = 0
count_region_3 = 0
cost_region_3 = 0
cost_region_4 = 0
count_region_4 = 0
counter = 0
# iterating through the region-list and count the amount of people for each
# region and sum the costs.
for entry in region:
    if (entry) == "northeast":
        count_region_1 += 1
        cost_region_1 += float(charges[counter])
        counter += 1
        continue
    if (entry) == "southeast":
        count_region_2 += 1
        cost_region_2 += float(charges[counter])
        counter += 1
        continue
    if (entry) == "southwest":
        count_region_3 += 1
        cost_region_3 += float(charges[counter])
        counter += 1
        continue
    if (entry) == "northwest":
        count_region_4 += 1
        cost_region_4 += float(charges[counter])
        counter += 1
        continue
# calculating the average cost for each region
avg_cost_region_1 = round(cost_region_1 / count_region_1, 2)
avg_cost_region_2 = round(cost_region_2 / count_region_2, 2)
avg_cost_region_3 = round(cost_region_3 / count_region_3, 2)
avg_cost_region_4 = round(cost_region_4 / count_region_4, 2)
# printing the results
print("\nThere are " + str(count_region_1) +
      " people in the northeast. This is " +
      str(round(count_region_1/len(region)*100,2)) +
      "% of people in the dataset." + 
      "\nThey have an average cost of " + str(avg_cost_region_1) + " Dollar.")
# There are 324 people in the northeast.
# This is 24.22% of people in the dataset.
# They have an average cost of 13406.38 Dollar.
print("There are " + str(count_region_2) +
      " people in the southeast. This is " +
      str(round(count_region_2/len(region)*100,2)) +
      "% of people in the dataset." + 
      "\nThey have an average cost of " + str(avg_cost_region_2) + " Dollar.")
# There are 364 people in the southeast.
# This is 27.2% of people in the dataset.
# They have an average cost of 14735.41 Dollar.
print("There are " + str(count_region_3) +
      " people in the southwest. This is " +
      str(round(count_region_3/len(region)*100,2)) +
      "% of people in the dataset." + 
      "\nThey have an average cost of " + str(avg_cost_region_3) + " Dollar.")
# There are 325 people southwest.
# This is 24.29% of people in the dataset.
# They have an average cost of 12346.94 Dollar.
print("There are " + str(count_region_4) +
      " people in the northwest. This is " +
      str(round(count_region_4/len(region)*100,2)) +
      "% of people in the dataset." + 
      "\nThey have an average cost of " + str(avg_cost_region_4) + " Dollar.")
# There are 325 people in the northwest.
# This is 24.29% of people in the dataset.
# They have an average cost of 12417.58 Dollar.

#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
# Smoking seems to have the biggest influence on health costs.
# Therefore, I will have a look how smoking influences the other groups.

# I have look to the smoker and non-smoker
# I divide all data in the two groups: non-smoker, smoker.
# For each category I create a list for non-smokers and smokers
ns_age = []
ns_sex = []
ns_bmi = []
ns_children = []
ns_region = []
ns_charges = []
ns_counter = []
s_age = []
s_sex = []
s_bmi = []
s_children = []
s_region = []
s_charges = []
s_counter = []
# I fill those lists
counter = 0
for entry in data_list:
    if smoker[counter] == "no":
        ns_age.append(entry["age"])
        ns_sex.append(entry["sex"])
        ns_bmi.append(entry["bmi"])
        ns_children.append(entry["children"])
        ns_region.append(entry["region"])
        ns_charges.append(entry["charges"])
        ns_counter.append(counter)
    if smoker[counter] == "yes":
        s_age.append(entry["age"])
        s_sex.append(entry["sex"])
        s_bmi.append(entry["bmi"])
        s_children.append(entry["children"])
        s_region.append(entry["region"])
        s_charges.append(entry["charges"])
        s_counter.append(counter)
    counter +=1

# The second most influential group was the age.
# I will look how smoking influences the costs according to the age.
# Therefore I use the same functions/defintions than before.
ns_age_1 = group_costs_num(AGE1, AGE2, ns_age, ns_charges)
s_age_1 = group_costs_num(AGE1, AGE2, s_age, s_charges)
ns_age_2 = group_costs_num(AGE2, AGE3, ns_age, ns_charges)
s_age_2 = group_costs_num(AGE2, AGE3, s_age, s_charges)
ns_age_3 = group_costs_num(AGE3, AGE4, ns_age, ns_charges)
s_age_3 = group_costs_num(AGE3, AGE4, s_age, s_charges)
ns_age_4 = group_costs_num(AGE4, AGE5, ns_age, ns_charges)
s_age_4 = group_costs_num(AGE4, AGE5, s_age, s_charges)

# printing the results
print("\nThere are " + str(ns_age_1[0]) + " non-smokers between " + str(AGE1) +
      " and " + str(AGE2-1) +
      "\nThey have an average cost of " + str(ns_age_1[1]) + " Dollar.")
print("There are " + str(s_age_1[0]) + " smokers between " + str(AGE1) +
      " and " + str(AGE2-1) +
      "\nThey have an average cost of " + str(s_age_1[1]) + " Dollar.")
print("In this age group are "+
      str(round(ns_age_1[0]/(ns_age_1[0]+s_age_1[0])*100)) +
      "% non-smokers and " + 
      str(round(s_age_1[0]/(ns_age_1[0]+s_age_1[0])*100)) + "% smoker.")
# There are 218 non-smokers between 0 and 24
# They have an average cost of 3841.1 Dollar.
# There are 60 smokers between 0 and 24
# They have an average cost of 27796.54 Dollar.
# In this age group are 78% non-smokers and 22% smoker.
print("\nThere are " + str(ns_age_2[0]) + " non-smokers between " + str(AGE2) +
      " and " + str(AGE3-1) +
      "\nThey have an average cost of " + str(ns_age_2[1]) + " Dollar.")
print("There are " + str(s_age_2[0]) + " smokers between " + str(AGE2) +
      " and " + str(AGE3-1) +
      "\nThey have an average cost of " + str(s_age_2[1]) + " Dollar.")
print("In this age group are "+
      str(round(ns_age_2[0]/(ns_age_2[0]+s_age_2[0])*100)) +
      "% non-smokers and " + 
      str(round(s_age_2[0]/(ns_age_2[0]+s_age_2[0])*100)) + "% smoker.")
# There are 414 non-smokers between 25 and 44
# They have an average cost of 6559.74 Dollar.
# There are 117 smokers between 25 and 44
# They have an average cost of 29954.29 Dollar.
# In this age group are 78% non-smokers and 22% smoker.
print("\nThere are " + str(ns_age_3[0]) + " non-smokers between " + str(AGE3) +
      " and " + str(AGE4-1) +
      "\nThey have an average cost of " + str(ns_age_3[1]) + " Dollar.")
print("There are " + str(s_age_3[0]) + " smokers between " + str(AGE3) +
      " and " + str(AGE4-1) +
      "\nThey have an average cost of " + str(s_age_3[1]) + " Dollar.")
print("In this age group are "+
      str(round(ns_age_3[0]/(ns_age_3[0]+s_age_3[0])*100)) +
      "% non-smokers and " + 
      str(round(s_age_3[0]/(ns_age_3[0]+s_age_3[0])*100)) + "% smoker.")
# There are 232 non-smokers between 45 and 54
# They have an average cost of 11241.4 Dollar.
# There are 55 smokers between 45 and 54
# They have an average cost of 35310.4 Dollar.
# In this age group are 81% non-smokers and 19% smoker.
print("\nThere are " + str(ns_age_4[0]) + " non-smokers between " + str(AGE4) +
      " and " + str(AGE5-1) +
      "\nThey have an average cost of " + str(ns_age_4[1]) + " Dollar.")
print("There are " + str(s_age_4[0]) + " smokers between " + str(AGE4) +
      " and " + str(AGE5-1) +
      "\nThey have an average cost of " + str(s_age_4[1]) + " Dollar.")
print("In this age group are "+
      str(round(ns_age_4[0]/(ns_age_4[0]+s_age_4[0])*100)) +
      "% non-smokers and " + 
      str(round(s_age_4[0]/(ns_age_4[0]+s_age_4[0])*100)) + "% smoker.")
# There are 200 non-smokers between 55 and inf
# They have an average cost of 14064.83 Dollar.
# There are 42 smokers between 55 and inf
# They have an average cost of 39696.37 Dollar.
# In this age group are 83% non-smokers and 17% smoker.

# The third most influence on the costs had the BMI.
# I will do the same with the BMI as I did for the age.
ns_bmi_1 = group_costs_num(BMI1, BMI2, ns_bmi, ns_charges)
s_bmi_1 = group_costs_num(BMI1, BMI2, s_bmi, s_charges)
ns_bmi_2 = group_costs_num(BMI2, BMI3, ns_bmi, ns_charges)
s_bmi_2 = group_costs_num(BMI2, BMI3, s_bmi, s_charges)
ns_bmi_3 = group_costs_num(BMI3, BMI4, ns_bmi, ns_charges)
s_bmi_3 = group_costs_num(BMI3, BMI4, s_bmi, s_charges)
ns_bmi_4 = group_costs_num(BMI4, BMI5, ns_bmi, ns_charges)
s_bmi_4 = group_costs_num(BMI4, BMI5, s_bmi, s_charges)
ns_bmi_5 = group_costs_num(BMI5, BMI6, ns_bmi, ns_charges)
s_bmi_5 = group_costs_num(BMI5, BMI6, s_bmi, s_charges)
# printing the results
print("")
print("\nThere are " + str(ns_bmi_1[0]) + " non-smoker with underweight." +
      "\nThey have an average cost of " + str(ns_bmi_1[1]) + " Dollar.")
print("There are " + str(s_bmi_1[0]) + " smoker with underweight." +
      "\nThey have an average cost of " + str(s_bmi_1[1]) + " Dollar.")
print("In this bmi group are "+
      str(round(ns_bmi_1[0]/(ns_bmi_1[0]+s_bmi_1[0])*100)) +
      "% non-smokers and " + 
      str(round(s_bmi_1[0]/(ns_bmi_1[0]+s_bmi_1[0])*100)) + "% smoker.")
# There are 15 non-smoker with underweight.
# They have an average cost of 5532.99 Dollar.
# There are 5 smoker with underweight.
# They have an average cost of 18809.82 Dollar.
# In this bmi group are 75% non-smokers and 25% smoker.
print("\nThere are " + str(ns_bmi_2[0]) + " non-smoker with normal weight." +
      "\nThey have an average cost of " + str(ns_bmi_2[1]) + " Dollar.")
print("There are " + str(s_bmi_2[0]) + " smoker with normal weight." +
      "\nThey have an average cost of " + str(s_bmi_2[1]) + " Dollar.")
print("In this bmi group are "+
      str(round(ns_bmi_2[0]/(ns_bmi_2[0]+s_bmi_2[0])*100)) +
      "% non-smokers and " + 
      str(round(s_bmi_2[0]/(ns_bmi_2[0]+s_bmi_2[0])*100)) + "% smoker.")
# There are 175 non-smoker with normal weight.
# They have an average cost of 7685.66 Dollar.
# There are 50 smoker with normal weight.
# They have an average cost of 19942.22 Dollar.
# In this bmi group are 78% non-smokers and 22% smoker.
print("\nThere are " + str(ns_bmi_3[0]) + " non-smoker with overweight." +
      "\nThey have an average cost of " + str(ns_bmi_3[1]) + " Dollar.")
print("There are " + str(s_bmi_3[0]) + " smoker with overweight." +
      "\nThey have an average cost of " + str(s_bmi_3[1]) + " Dollar.")
print("In this bmi group are "+
      str(round(ns_bmi_3[0]/(ns_bmi_3[0]+s_bmi_3[0])*100)) +
      "% non-smokers and " + 
      str(round(s_bmi_3[0]/(ns_bmi_3[0]+s_bmi_3[0])*100)) + "% smoker.")
# There are 312 non-smoker with overweight.
# They have an average cost of 8257.96 Dollar.
# There are 74 smoker with overweight.
# They have an average cost of 22495.87 Dollar.
# In this bmi group are 81% non-smokers and 19% smoker.
print("\nThere are " + str(ns_bmi_4[0]) + " non-smoker with obesity." +
      "\nThey have an average cost of " + str(ns_bmi_4[1]) + " Dollar.")
print("There are " + str(s_bmi_4[0]) + " smoker with obesity." +
      "\nThey have an average cost of " + str(s_bmi_4[1]) + " Dollar.")
print("In this bmi group are "+
      str(round(ns_bmi_4[0]/(ns_bmi_4[0]+s_bmi_4[0])*100)) +
      "% non-smokers and " + 
      str(round(s_bmi_4[0]/(ns_bmi_4[0]+s_bmi_4[0])*100)) + "% smoker.")
# There are 317 non-smoker with obesity.
# They have an average cost of 8532.14 Dollar.
# There are 74 smoker with obesity.
# They have an average cost of 39640.59 Dollar.
# In this bmi group are 81% non-smokers and 19% smoker.
print("\nThere are " + str(ns_bmi_5[0]) + " non-smoker with a BMI > 35." +
      "\nThey have an average cost of " + str(ns_bmi_5[1]) + " Dollar.")
print("There are " + str(s_bmi_5[0]) + " smoker with a BMI > 35." +
      "\nThey have an average cost of " + str(s_bmi_5[1]) + " Dollar.")
print("In this bmi group are "+
      str(round(ns_bmi_5[0]/(ns_bmi_5[0]+s_bmi_5[0])*100)) +
      "% non-smokers and " + 
      str(round(s_bmi_5[0]/(ns_bmi_5[0]+s_bmi_5[0])*100)) + "% smoker.")
# There are 245 non-smoker with a BMI > 35.
# They have an average cost of 9244.5 Dollar.
# There are 71 smoker with a BMI > 35.
# They have an average cost of 43556.4 Dollar.
# In this bmi group are 78% non-smokers and 22% smoker.


