import pandas as pd
import json
import requests
from pandas.io.json import json_normalize
import csv

# CALLS DATAFRAME AND PRINTS OUT INFORMATION OF ITS CONTENTS
def dataframe_info(dataframe):
    print('***NUMBER OF ROWS x COLUMNS***\n',dataframe.shape,'\n')
    print('***NUMBER OF EMPTY DATA***\n',dataframe.isnull().sum(),'\n')
    print('***DATA TYPE***\n',dataframe.dtypes)
    print(dataframe.columns)
    
# ~~~~~~~~~~~~~
# READS IN COUNTY POPULATION CSV VIA FILE
df_pop = pd.read_csv('Data Sources\PA_County_Population.csv')
# CLEANS UP COUNTY STRING BY REMOVING EVERYTHING BUT THE COUNTY NAME
df_pop['county_name'] = df_pop['county_name'].str.replace('County, Pennsylvania', '').str.strip().str.upper()
# ~~~~~~~~~~~~~

# ~~~~~~~~~~~~~
# READS IN DRUG DATA JSON VIA URL
drug_source = requests.get('https://data.pa.gov/resource/wpwa-yta5.json')
standardize_data = json.loads(drug_source.text)
# FLATTENS JSON DATA TO STRINGS (USED FOR NESTED DICTS)
df_drug = json_normalize(standardize_data)
df_drug['county_name'] = df_drug['county_name'].str.upper()
# ~~~~~~~~~~~~~

# # JOINS df_drug and df_pop ON COMMON DATAFRAME COLUMN 'county_name'
df_drug = df_pop.join(df_drug.set_index('county_name'), on='county_name', how='right')

# DROPS ALL ROWS CONTAINING 'Out of State' AS COUNTY NAME
# df_drug = df_drug[~df_drug.county_name.str.contains("Out of State")]
df_drug.dropna(how='any', inplace=True)

# CONVERTS SELECTED COLUMNS TO NUMERIC VALUES AFTER FLATTENED BY json_normalize
df_drug = df_drug.astype({'drug_quantity':'float', 'arrests':'int', 'incident_count':'int',
                          'population':'int'})

# CAPITILIZED ALL LETTERS SO IT MATCHES PA COUNTY BOUNDRIES and 'key_on' FUNCTION BETWEEN FOLIUM AND JSON
df_drug['county_name'] = df_drug['county_name'].str.upper()

# CREATED NEW LAT/LONG/RATE/INCIDNET_TOTAL COLUMNS W/ APPROPRIATE VALUES
df_drug['lat'] = df_drug['lat_long.coordinates'].apply(lambda x: x[1])
df_drug['long'] = df_drug['lat_long.coordinates'].apply(lambda x: x[0]) 
df_drug['incident_total'] = df_drug['incident_count'] + df_drug['arrests']
df_drug['rate'] = df_drug['incident_total'] / df_drug['population'] * 100000

# GROUPS DATAFRAME IN A MULTI INDEX
ser = df_drug.groupby(['county_name', 'drug', 'lat', 'long', 'population'])['drug_quantity', 
                       'arrests', 'incident_count', 'incident_total', 'rate'].sum()
ser_total = df_drug.groupby(['county_name', 'lat', 'long', 'population'])['drug_quantity', 
                             'arrests', 'incident_count', 'incident_total', 'rate'].sum()

# REINDEX FOR CSV OUTPUT
col_titles_drugs = ['county_name', 'drug', 'arrests', 'incident_count', 'incident_total',
                    'drug_quantity', 'population', 'rate']
col_titles_total = ['county_name', 'arrests', 'incident_count', 'incident_total', 
                    'drug_quantity', 'population', 'rate']

# DATA STANDARIZATION
def standardize_data(drug_name):
    drug_name = ser.loc[(slice(None), [drug_name]), :].reset_index().reindex(columns=col_titles_drugs) # resets index and reindexes with selected column names
    drug_name = df_pop.merge(drug_name, how='left')                                                    # merges missing counties that had no indicents to data frame so all counties are included in folium
    drug_name = drug_name.fillna(0)                                                                    # fills all NaN with a '0'
    drug_name['drug'].replace(0, 'Zero incidents recorded', inplace=True)                              # replaces 0 in drug column with 'zero incidents recorded'   
    drug_name = drug_name.astype({'drug_quantity':'float', 'arrests':'int', 'incident_count':'int',    # sets data type for each column
                              'population':'int', 'incident_total':'int'})
    return drug_name
    
df_her = standardize_data('Heroin')
df_fen = standardize_data('Fentanyl')
df_opi = standardize_data('Opium')

df_total = ser_total.reset_index().reindex(columns=col_titles_total)
df_total = df_pop.merge(df_total, how='left')                                                    # merges missing counties that had no indicents to data frame so all counties are included in folium
df_total = df_total.fillna(0)                                                                    # fills all NaN with a '0'

# WRITES DATA FRAMES TO .CSV
df_her.to_csv('PA_Herion.csv', sep=',', index=False)
df_fen.to_csv('PA_Fentanyl.csv', sep=',', index=False)
df_opi.to_csv('PA_Opium.csv', sep=',', index=False)
df_total.to_csv('PA_Drug_Total.csv', sep=',', index=False)
df_pop.to_csv('PA_Pop.csv', sep=',', index=False)
print('Data frames exported to .CSV')

# LOADS GEOJSON FILE
with open('Data Sources\PaCounty2019_01.json') as f:
    data = json.load(f)

# NORMALIZES, AND MERGES GEOJSON DATAFRAME TO DRUG DATAFRAME 
def df_gjson_merge(drug_dataframe):
    county_gjson = json_normalize(data["features"])
    county_gjson = county_gjson.rename(columns = {'properties.COUNTY_NAM':'county_name'})
    county_gjson = drug_dataframe.merge(county_gjson, how='left')
    return county_gjson

df_her = df_gjson_merge(df_her)
df_fen = df_gjson_merge(df_fen)
df_opi = df_gjson_merge(df_opi)
df_total = df_gjson_merge(df_total)

# DATAFRAME TO GEOJSON FORMAT
def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'geometry':{'type': row['geometry.type'],
                               'coordinates':row['geometry.coordinates']},
                    'properties':{}}
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

# CALLS df_to_geojson FUNCTION FOR ALL DRUG DATAFRAMES
her_geojson = df_to_geojson(df_her, col_titles_drugs)
fen_geojson = df_to_geojson(df_fen, col_titles_drugs)
opi_geojson = df_to_geojson(df_opi, col_titles_drugs)
total_geojson = df_to_geojson(df_total, col_titles_total)

# WRITES A GEOJSON FILE
with open('her_geojson.json', 'w') as outfile:
    json.dump(her_geojson, outfile, indent=2)

with open('fen_geojson.json', 'w') as outfile:
    json.dump(fen_geojson, outfile, indent=2)

with open('opi_geojson.json', 'w') as outfile:
    json.dump(opi_geojson, outfile, indent=2)

with open('total_geojson.json', 'w') as outfile:
    json.dump(total_geojson, outfile, indent=2) 

print('Data frames exported to GEOJSON')