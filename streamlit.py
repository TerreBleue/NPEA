import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import geojson
import re

# Draw a title and some text to the app:
'''
# This is the document title

This is some _markdown_.
'''

with open("arrondissements.geojson", "r") as f:
    gj = geojson.load(f)
st.dataframe(gj) 

# TODO: map the geojson data to the dataframe
df = pd.read_csv("Arrondissements de Paris.csv")
# Extract the numbers from the "Name" column (example: "10e Arrondissement de Paris" -> "10")
df["Number"] = df["Name"].apply(lambda x: re.search(r"\d+", x).group(0))
# Rename column "Latitude" to "lat" and "Longitude" to "lon"
df.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)
df

# TODO: create a map of polygons 
st.map(df)



col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

options = ["Paris", "Center", "North", "East", "South", "West"]
selection = st.segmented_control(
    "Directions", options, selection_mode="single", default=options[0]
)
st.markdown(f"Your selected options: {selection}.")

x = 10
'x', x  # 👈 Draw the string 'x' and then the value of x


