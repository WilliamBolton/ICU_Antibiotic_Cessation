"""
MIMIC DF
============================

"""

# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Create dataframes
icustays = pd.read_csv(r"/home/wb1115/mimic-iv-1.0/icu/icustays.csv")
diagnoses_icd = pd.read_csv(r"/home/wb1115/mimic-iv-1.0/hosp/diagnoses_icd.csv")
#procedures_icd = pd.read_csv(r"/home/wb1115/mimic-iv-1.0/hosp/procedures_icd.csv", dtype={'icd_code': 'object'})
antibiotic = pd.read_csv(r"/home/wb1115/mimic-iv-1.0/mimic_derived_antibiotic.csv")
microbiologyevents = pd.read_csv(r"/home/wb1115/mimic-iv-1.0/hosp/microbiologyevents.csv", dtype={'quantity': 'object', 'comments': 'object'})
#pharmacy = pd.read_csv(r"/home/wb1115/mimic-iv-1.0/hosp/pharmacy.csv", dtype={'lockout_interval': 'object', 'one_hr_max': 'object', 'expirationdate': 'object', 'fill_quantity': 'object'}, parse_dates=['starttime', 'stoptime', 'verifiedtime', 'expirationdate'])
#print(pharmacy.info())


# Check dataframes
#print(antibiotic.shape)
#print(procedures_icd.dtypes)
#print(icustays.shape)
#print(diagnoses_icd.shape)

# Filter dataframes
filtered_diagnoses_icd = diagnoses_icd[diagnoses_icd["icd_code"].isin(["99731", "J95851"])]
#print(filtered_diagnoses_icd.info())


#print(antibiotic.info())
antibiotic["starttime"] = pd.to_datetime(antibiotic["starttime"], infer_datetime_format=True)
antibiotic["stoptime"] = pd.to_datetime(antibiotic["stoptime"], infer_datetime_format=True)
filtered_antibiotics = antibiotic[(antibiotic["route"] == "IV")]
filtered_antibiotics['length_of_treatment'] = filtered_antibiotics['stoptime'] - filtered_antibiotics['starttime']
filtered_antibiotics = filtered_antibiotics[(filtered_antibiotics["length_of_treatment"] > '0 days')]

# Check filtered dataframes
#print(filtered_diagnoses_icd.shape)
#print(filtered_diagnoses_icd.head)
#print('size =', filtered_antibiotics.size)
#print(filtered_antibiotics.info())
#print(filtered_antibiotics.head)


# Join dataframes
merge_one = pd.merge(icustays, filtered_diagnoses_icd, how="inner")
print(merge_one.shape)

merge_two = pd.merge(merge_one, filtered_antibiotics, how="inner")
print(merge_two.shape)

merge_three = pd.merge(merge_two, microbiologyevents, how="inner")
merge_n = merge_three

# Check joined dataframes
print(merge_n.info())
print(merge_n.shape)
print(merge_n.columns)
print(merge_n.head)

# One patient
one_patient = merge_n[merge_n["subject_id"].isin(["10656173"])]
one_patient_condensed = merge_two[merge_two["subject_id"].isin(["10656173"])]


print(one_patient.info())
print(one_patient.shape)
print(one_patient.columns)
print(one_patient.head)

# Save df
merge_n.to_csv('ICU_diagnoses_antibiotics_microbiology.csv', index=False)
merge_two.to_csv('ICU_diagnoses_antibiotics.csv', index=False)

one_patient.to_csv('One_patient_10656173.csv', index=False)
one_patient_condensed.to_csv('One_patient_condensed_10656173.csv', index=False)

