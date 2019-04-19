import folium
import pandas as pd
import json

df_drug_total = pd.read_csv('PA_Drug_Total.csv')
df_her = pd.read_csv('PA_Herion.csv')
df_opi = pd.read_csv('PA_Opium.csv')
df_fen = pd.read_csv('PA_Fentanyl.csv')

total_geojson = json.load(open('total_geojson.json'))
her_geojson = json.load(open('her_geojson.json'))
opi_geojson = json.load(open('opi_geojson.json'))
fen_geojson = json.load(open('fen_geojson.json'))

m = folium.Map(location=[41.20, -77.50], tiles='cartodbpositron', zoom_start=8.3)

total = folium.Choropleth(
    geo_data=total_geojson,
    data=df_drug_total,               
    columns=['county_name', 'rate'],
    key_on='feature.properties.county_name',
    fill_color='BuPu',
    fill_opacity=0.4,
    legend_name='Total incident rate per 100,000 people',
    highlight=True,
    name='Total Incidents',
    show=True,
).add_to(m)

folium.GeoJson(
    total_geojson,
    tooltip=folium.features.GeoJsonTooltip(fields=['county_name', "arrests", "incident_count",
                                                   "incident_total", "drug_quantity", "population", "rate" ],
                                          aliases=['County', 'Arrests', 'Incident Count', 'Incident Total', 'Drug Quanity (kg)', 'Population', 'Rate'],
                                          localize=True)              
).add_to(total.geojson)

herion = folium.Choropleth(
    geo_data=her_geojson,
    data=df_her,               
    columns=['county_name', 'rate'],
    key_on='feature.properties.county_name',
    fill_color='OrRd',
    fill_opacity=0.4,
    legend_name='Herion incident rate per 100,000 people',
    highlight=True,
    name='Herion Incidents',
    show=False
).add_to(m)

folium.GeoJson(
    her_geojson,
    tooltip=folium.features.GeoJsonTooltip(fields=['county_name', "drug", "arrests", "incident_count",
                                                   "incident_total", "drug_quantity", "population", "rate" ],
                                          aliases=['County', 'Drug', 'Arrests', 'Incident Count', 'Incident Total', 'Drug Quanity (kg)', 'Population', 'Rate'],
                                          localize=True)
).add_to(herion.geojson)

opium = folium.Choropleth(
    geo_data=opi_geojson,
    data=df_opi,               
    columns=['county_name', 'rate'],
    key_on='feature.properties.county_name',
    fill_color='GnBu',
    fill_opacity=0.4,
    legend_name='Opium Incident rate per 100,000 people',
    highlight=True,
    name='Opium Incidents',
    show=False
).add_to(m)

folium.GeoJson(
   opi_geojson,
    tooltip=folium.features.GeoJsonTooltip(fields=['county_name', "drug", "arrests", "incident_count",
                                                   "incident_total", "drug_quantity", "population", "rate" ],
                                          aliases=['County', 'Drug', 'Arrests', 'Incident Count', 'Incident Total', 'Drug Quanity (kg)', 'Population', 'Rate'],
                                          localize=True)
).add_to(opium.geojson)

fentanyl = folium.Choropleth(
    geo_data=fen_geojson,
    data=df_fen,               
    columns=['county_name', 'rate'],
    key_on='feature.properties.county_name',
    fill_color='PuRd',
    fill_opacity=0.4,
    legend_name='Fentanyl incident rate per 100,000 people',
    highlight=True,
    name='Fentanyl Incidents',
    show=False
).add_to(m)

folium.GeoJson(
    fen_geojson,
    tooltip=folium.features.GeoJsonTooltip(fields=['county_name', "drug", "arrests", "incident_count",
                                                   "incident_total", "drug_quantity", "population", "rate" ],
                                          aliases=['County', 'Drug', 'Arrests', 'Incident Count', 'Incident Total', 'Drug Quanity (kg)', 'Population', 'Rate'],
                                          localize=True)
).add_to(fentanyl.geojson)

folium.LayerControl(collapsed=False).add_to(m) 
m.save('PA_County_Drug_Map.html')

print('Map created.')