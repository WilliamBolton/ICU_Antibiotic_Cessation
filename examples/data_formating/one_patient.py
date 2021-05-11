# Libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Create dataframes
ICU = pd.read_csv(r"/home/wb1115/PycharmProjects/ICU_Antibiotic_Cessation/ICU_diagnoses_antibiotics_microbiology.csv")
ICU_condensed = pd.read_csv(r"/home/wb1115/PycharmProjects/ICU_Antibiotic_Cessation/ICU_diagnoses_antibiotics.csv")
# One patient
subject_id = 11803145

one_patient = ICU[ICU["subject_id"].isin([subject_id])]
one_patient_condensed = ICU_condensed[ICU_condensed["subject_id"].isin([subject_id])]


# Check df
print(one_patient.info())
print(one_patient.shape)
print(one_patient.columns)
print(one_patient.head)

# Save df
one_patient.to_csv('One_patient_11803145.csv', index=False)
one_patient_condensed.to_csv('One_patient_condensed_11803145.csv', index=False)
