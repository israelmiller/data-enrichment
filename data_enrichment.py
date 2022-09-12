import pandas as pd
import numpy as np

#Read the unenriched data from the 'data folder'

SPARCS = pd.read_csv('data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv')

NYADI_ZIP = pd.read_csv('data/NY_2015_ADI_9 Digit Zip Code_v3.1.txt')

#For the NYADI_ZIP data, we only need the zip code and the ADI score columns

NYADI_ZIP = NYADI_ZIP[['ZIPID', 'ADI_STATERNK', 'ADI_NATRANK']]

# In the NYADI_ZIP data for ZIPID column, we keep the first 3 digits after the G to match the deidentified SPARCS data
NYADI_ZIP['ZIPID'] = NYADI_ZIP['ZIPID'].str.slice(1,4)

NYADI_ZIP.sample(5)
NYADI_ZIP.shape

#For the SPARCS data, we rename the Zip Code - 3 digits column to match the NYADI_ZIP data

SPARCS.rename(columns={'Zip Code - 3 digits': 'ZIPID'}, inplace=True)
SPARCS = SPARCS[['ZIPID', 'Length of Stay', 'Race', 'Ethnicity', 'APR Risk of Mortality', 'Facility Name']]

SPARCS['ZIPID'].sample(5)
SPARCS.columns
SPARCS.shape
#Merge the two dataframes on the ZIP code column

ENRICHED_SPARCS = SPARCS.merge(NYADI_ZIP, on='ZIPID', how='left')
