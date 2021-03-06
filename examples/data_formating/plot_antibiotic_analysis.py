"""
Antibiotic analysis
============================

"""

# Generic libraries
import pandas as pd
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 2000)
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# -----------------------------
# Constants
# -----------------------------
# Path
path = '/home/wb1115/PycharmProjects/ICU_Antibiotic_Cessation/ICU_VAP_diagnoses_antibiotics_formatted.csv'
#path = '/home/wb1115/PycharmProjects/ICU_Antibiotic_Cessation/ICU_SEPSIS_diagnoses_antibiotics_formatted.csv'

# -----------------------------
# Load data
# -----------------------------
# Read data
data = pd.read_csv(path, parse_dates=['date'])
#print(data.info())
#print(data)

counts = data['antibiotics'].value_counts()
print(counts)
#counts.to_csv('ICU_VAP_antibiotics_counts.csv')
#counts.to_csv('ICU_SEPSIS_antibiotics_counts.csv')

# -----------------------------
# Find out number of antibiotics and days in hospital per patient
# -----------------------------

data2 = data.groupby(["stay_id"]).nunique()
print(data2)
#data2.boxplot('date')
#data2.boxplot('antibiotics')
print('Mean n of antibiotics:')
print(data2['antibiotics'].mean())
print('Median n of antibiotics:')
print(data2['antibiotics'].median())
print('Mean length of stay:')
print(data2['date'].mean())
print('Median length of stay:')
print(data2['date'].median())

plt.boxplot([data2['antibiotics'], data2['date']], labels=['n_of_antibiotics', 'length_of_stay'], showmeans=True, meanline=True)
plt.ylabel('days')
plt.show()
sns.violinplot(data=[data2['antibiotics'], data2['date']])
plt.show()

# -----------------------------
# Define if antibiotic treatment is consecutive
# -----------------------------

consecutive1 = [1]
for data1, data2 in zip(data['antibiotics'][:], data['antibiotics'][1:]):
    if data1 == data2:
        consecutive1.append(1)
    else:
        consecutive1.append(0)

consecutive2 = []
for data1, data2 in zip(data['antibiotics'][1:], data['antibiotics'][:]):
    if data1 == data2:
        consecutive2.append(1)
    else:
        consecutive2.append(0)

#print(consecutive1)
#print(consecutive2)

consecutive3 = []
for n, m in zip(consecutive1, consecutive2):
    if n == 1:
        consecutive3.append(1)
    elif m == 1:
        consecutive3.append(1)
    else:
        consecutive3.append(0)

consecutive3.append(1)
#print(consecutive3)
data['consecutive'] = consecutive3
print(data)
#data.to_csv('ICU_VAP_antibiotics_consecutive.csv')
#data.to_csv('ICU_SEPSIS_antibiotics_consecutive.csv')

# -----------------------------
# Find out mean and SD length of treatment per antibiotic
# -----------------------------

cumcount2 = []
count2 = 1
pos = -1

for x in range(len(data)):
    pos += 1
    if pos == len(data) - 1:
        if data.iloc[x]['consecutive'] == 1:
            if data.iloc[x]['antibiotics'] == data.iloc[x - 1]['antibiotics']:
                count2 += 1
                cumcount2.extend([count2] * count2)
            else:
                if data.iloc[x - 1]['consecutive'] == 1:
                    cumcount2.extend([count2] * count2)
        elif data.iloc[x]['consecutive'] == 0:
                if count2 == 1:
                    cumcount2.append(1)
                else:
                    cumcount2.extend([count2] * count2)
                    cumcount2.append(1)
    elif data.iloc[x]['consecutive'] == 1:
        if x == 0:
            pass
            #print('pass')
        elif data.iloc[x]['antibiotics'] == data.iloc[x-1]['antibiotics']:
            #if data.iloc[x]['stay_id'] == data.iloc[x - 1]['stay_id']:
                count2 += 1
            #else:
            #    cumcount2.extend([count2] * count2)
            #    count2 = 1
            #    print('hi there')
            #print('add 1 to count')
        #elif data.iloc[x]['antibiotics'] == data.iloc[x-1]['antibiotics']:
        #    count += 1
        else:
            if data.iloc[x-1]['consecutive'] == 1:
                cumcount2.extend([count2] * count2)
                #print('added', count2, 'LOC-1')
                count2 = 1
            else:
                count2 = 1
                #print('count2 = 1')
    elif data.iloc[x]['consecutive'] == 0:
        if count2 == 1:
            cumcount2.append(1)
            #print('added 1')
        else:
            cumcount2.extend([count2] * count2)
            #print('added', count2, 'LOC-2')
            cumcount2.append(1)
            count2 = 1
    else:
        #cumcount2.append(1)
        print('???')

#print('cumcount2')
#print(cumcount2)
#print(len(cumcount2))

data['treatment_length'] = cumcount2
print(data)
#print(data.info())

### SAVE DATA ###
#data.to_csv('ICU_VAP_antibiotics_treatment_length.csv')
#data.to_csv('ICU_SEPSIS_antibiotics_treatment_length.csv')

### VISUALISE DATA ###
data3 = data.groupby(['antibiotics']).nunique()
print('Mean antibiotic treatment length:')
print(data3['treatment_length'].mean())
print('Median antibiotic treatment length:')
print(data3['treatment_length'].median())


plt.boxplot(data3['treatment_length'], labels=['antibiotic_treatment_length'], showmeans=True, meanline=True)
plt.ylabel('days')
plt.show()
sns.violinplot(data=data3['treatment_length'])
plt.show()

cleaned_df = data['antibiotics'].str.replace("^\[.|.\]$","")
cleaned_df = cleaned_df.str.replace("\'","")
print(cleaned_df)
data['antibiotics_clean'] = cleaned_df
print(data)

filtered_df = data[data['antibiotics_clean'].map(data['antibiotics_clean'].value_counts()) > 400]
print(filtered_df)

means = filtered_df.groupby('antibiotics_clean', as_index=False)['treatment_length'].mean()
print('means:')
print(means)
#plt.bar(means['antibiotics_clean'], means['treatment_length'])
#plt.show()
bar_plot = means.plot.bar(x='antibiotics_clean', y='treatment_length')
bar_plot.set_ylabel("days")
bar_plot.set_xlabel("antibiotic_treatment_length")
plt.xticks(fontsize=6)
plt.show()
