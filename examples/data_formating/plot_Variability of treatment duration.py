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
path = '/home/wb1115/PycharmProjects/ICU_Antibiotic_Cessation/ICU_VAP_antibiotics_treatment_length.csv'
#path = '/home/wb1115/PycharmProjects/ICU_Antibiotic_Cessation/ICU_SEPSIS_antibiotics_treatment_length.csv'

# -----------------------------
# Load data
# -----------------------------
# Read data
data = pd.read_csv(path, parse_dates=['date'])
#print(data.info())
#print(data)

# -----------------------------
# Format data
# -----------------------------

cleaned_df = data['antibiotics'].str.replace("^\[.|.\]$","")
cleaned_df = cleaned_df.str.replace("\'","")
#print(cleaned_df)
data['antibiotics_clean'] = cleaned_df
print(data)
counts = data['antibiotics_clean'].value_counts()
print(counts)
counts1 = data['treatment_length'].value_counts()
print(counts1)

filtered_df = data[data['antibiotics_clean'].map(data['antibiotics_clean'].value_counts()) > 400]
filtered_df2 = data[data['antibiotics_clean'] == 'cefepime, vancomycin']
print(filtered_df)
counts2 = filtered_df['treatment_length'].value_counts()
counts3 = filtered_df2['treatment_length'].value_counts()
print(counts2)
print(counts3)

overall_count_data = pd.DataFrame({'treatment_length': counts1.index, 'count': counts1.values})
most_common_count_data = pd.DataFrame({'treatment_length': counts2.index, 'count': counts2.values})
cefepime_vancomycin_count_data = pd.DataFrame({'treatment_length': counts3.index, 'count': counts3.values})

overall_count_data['count_normalized'] = overall_count_data['count']/overall_count_data['treatment_length']
most_common_count_data['count_normalized'] = most_common_count_data['count']/most_common_count_data['treatment_length']
cefepime_vancomycin_count_data['count_normalized'] = cefepime_vancomycin_count_data['count']/cefepime_vancomycin_count_data['treatment_length']

overall_count_data = overall_count_data.sort_values(by=['treatment_length'])
most_common_count_data = most_common_count_data.sort_values(by=['treatment_length'])
cefepime_vancomycin_count_data = cefepime_vancomycin_count_data.sort_values(by=['treatment_length'])

#print(count_data)

# -----------------------------
# Plot data
# -----------------------------

plt.scatter(x=overall_count_data['treatment_length'], y=overall_count_data['count_normalized'])
plt.title("Treatment length For All Antibiotics") #title
plt.xlabel("Treatment length (days)") #x label
plt.ylabel("Count (normalized)") #y label
plt.show()

plt.scatter(x=overall_count_data['treatment_length'], y=overall_count_data['count'])
plt.title("Treatment length For All Antibiotics") #title
plt.xlabel("Treatment length (days)") #x label
plt.ylabel("Count") #y label
plt.show()

plt.scatter(x=most_common_count_data['treatment_length'], y=most_common_count_data['count_normalized'])
plt.title("Treatment length For Most Common Antibiotics") #title
plt.xlabel("Treatment length (days)") #x label
plt.ylabel("Count (normalized)") #y label
plt.show()

plt.scatter(x=most_common_count_data['treatment_length'], y=most_common_count_data['count'])
plt.title("Treatment length For Most Common Antibiotics") #title
plt.xlabel("Treatment length (days)") #x label
plt.ylabel("Count") #y label
plt.show()

plt.scatter(x=cefepime_vancomycin_count_data['treatment_length'], y=cefepime_vancomycin_count_data['count_normalized'])
plt.title("Treatment length For cefepime_vancomycin") #title
plt.xlabel("Treatment length (days)") #x label
plt.ylabel("Count (normalized)") #y label
plt.show()

plt.scatter(x=cefepime_vancomycin_count_data['treatment_length'], y=cefepime_vancomycin_count_data['count'])
plt.title("Treatment length For cefepime_vancomycin") #title
plt.xlabel("Treatment length (days)") #x label
plt.ylabel("Count") #y label
plt.show()
