import pandas as pd
import numpy as np

#Read the unenriched data from the 'data folder'
SPARCS = pd.read_csv('data/Hospital_Inpatient_Discharges__SPARCS_De-Identified___2015.csv')
NYADI_ZIP = pd.read_csv('data/NY_2015_ADI_9 Digit Zip Code_v3.1.txt')

##Cleaning the data
#Make all column names lower case
SPARCS.columns = map(str.lower, SPARCS.columns)
NYADI_ZIP.columns = map(str.lower, NYADI_ZIP.columns)

#remove spaces and special characters from column names using regex
SPARCS.columns = SPARCS.columns.str.replace('[^A-Za-z0-9_]+', '_')
NYADI_ZIP.columns = NYADI_ZIP.columns.str.replace('[^A-Za-z0-9_]+', '_')

#Set empty values to nan
SPARCS.replace(to_replace=' ', value=np.nan, inplace=True)
SPARCS.replace(to_replace='', value=np.nan, inplace=True)

NYADI_ZIP.replace(to_replace=' ', value=np.nan, inplace=True)
NYADI_ZIP.replace(to_replace='', value=np.nan, inplace=True)

#Drop missing data
SPARCS.dropna(inplace=True)
NYADI_ZIP.dropna(inplace=True)

#Sanity check to make sure changes were successful
SPARCS.columns
NYADI_ZIP.columns

##Keep only necessary columns
#For the NYADI_ZIP data, we only need the zip code and the ADI score columns
NYADI_ZIP = NYADI_ZIP[['zipid', 'adi_staternk', 'adi_natrank']]

# In the NYADI_ZIP data for ZIPID column, we keep the first 3 digits after the G to match the deidentified SPARCS data
NYADI_ZIP['zipid'] = NYADI_ZIP['zipid'].str.slice(1,4)

#For the SPARCS data, we rename the Zip Code - 3 digits column to match the NYADI_ZIP data
SPARCS.rename(columns={'zip_code_3_digits': 'zipid'}, inplace=True)
SPARCS = SPARCS[['zipid', 'length_of_stay', 'race', 'ethnicity', 'apr_risk_of_mortality', 'facility_name']]
SPARCS['zipid'].sample(5)

#Sanity check to make sure changes were successful
SPARCS.columns
SPARCS.shape
SPARCS.isnull().sum()
SPARCS.sample(10)

NYADI_ZIP.columns
NYADI_ZIP.shape
NYADI_ZIP.isnull().sum()
NYADI_ZIP.sample(10)

#Drop duplicates in both data frames
SPARCS.drop_duplicates(inplace=True)
NYADI_ZIP.drop_duplicates(inplace=True)

#Merge the two dataframes on the ZIP code column
ENRICHED_SPARCS = SPARCS.merge(NYADI_ZIP, on='zipid', how='left')
ENRICHED_SPARCS.shape

#Export the enriched data to a csv file
ENRICHED_SPARCS.to_csv('enriched_data/enriched_sparcs.csv', index=False)