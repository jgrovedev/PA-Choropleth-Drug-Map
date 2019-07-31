## PA Choropleth Drug Map
A web map that displays drug related incident rates of counties in PA.  

## Motivation
I was interested in using pandas dataframes with different data sources to create a map in folium.

## Screenshots
![screenshot](https://github.com/jgrovedev/PA-Choropleth-Drug-Map/blob/master/Screenshot_drugmap.png)

## Tech/framework used
<b>Built with</b>
- [Python](https://www.python.org/) 
- [Folium](https://python-visualization.github.io/folium/)
- [JSON](https://docs.python.org/3/library/json.html)
- [Pandas](https://pandas.pydata.org/)
- [CSV](https://docs.python.org/3/library/csv.html)

## Features
Users can roll mouse over each county to display pop-up information and also select different layers.

NOTE: There is a bug with Folium v0.8.3 where multiple choropleth layer map legends will always be visible even if the layer isn't selected. Also, there is currently no solution to make choropleth layers managed by radio buttons instead of checkboxes and function properly. This means the user will need to uncheck a layer manually and check the next layer. 

## How to use?
Open PA_County_Drug_Map.html to view map
