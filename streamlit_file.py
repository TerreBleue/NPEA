import json
import streamlit as st
import pandas as pd
import geopandas as gpd
from mongodbFunctions import get_noise_data

@st.cache_data
def load_data() -> tuple[pd.DataFrame, gpd.GeoDataFrame]:
    """
    Load data from MongoDB and GeoJSON file.
    Returns:
        db_df (DataFrame): DataFrame containing noise data from MongoDB.
        arr_df (GeoDataFrame): GeoDataFrame containing arrondissement data from GeoJSON.
    """
    db_df = pd.DataFrame(get_noise_data())
    with open("arrondissements.geojson", "r") as f:
        arr_df = gpd.read_file(f)
    return db_df, arr_df


LDEN_REGLEMENTAIRE = 68
LN_REGLEMENTAIRE = 62
dict_arr = {
    "north": [9, 10, 17, 18, 19],
    "east": [11, 12, 20],
    "south": [5, 6, 13, 14],
    "west": [7, 8, 15, 16],
    "center": [1, 2, 3, 4],
}
COLOR_PALETTE = [(54, 162, 235, .75), (255, 99, 132, .75), (75, 192, 192), (255, 159, 64, .75), (153, 102, 255, .75), (255, 205, 86, .75)]
options = ["Center", "North", "East", "South", "West"]

st.set_page_config(
    page_title="NPEA in Paris",
    page_icon=":loud_sound:",
)

# Load data, as dataframes, from a MongoDB database and a GeoJSON file
data_loading_toast = st.toast("Data loading...")
try: 
    db_df, arr_df = load_data()
    data_loading_toast.toast("Data loaded!", icon="🎉")
except Exception as e:
    st.exception(e)
    raise RuntimeError("Failed to load data from MongoDB or GeoJSON file.")


st.title("Noise Pollution Exposure Analysis in Paris")
selection = st.pills("Zone", options, selection_mode="single", default=None)


# Specific section
# It will have both metrics and a chart
if selection is not None:
    st.header(f"Statistics of {selection} Zone")
    # Filter the dataframe "db_df" based on the selected option
    current_db_df = db_df[db_df["location"] == selection.lower()]

    for time in ["Day", "Night"]:
        limit = LN_REGLEMENTAIRE if time == "Night" else LDEN_REGLEMENTAIRE
        nb2022 = float(
            current_db_df[current_db_df["year"] == 2022][time.lower()].iloc[0]
        )
        nb2015 = float(current_db_df[current_db_df["year"] == 2015].day.iloc[0])
        nb_percentage = round((nb2022 - nb2015) / nb2015 * 100, 2)

        st.subheader(time)
        col1, col2 = st.columns(2)
        col1.metric("Limit", f"{limit} dB")
        col2.metric(
            "Citizens above limit in 2022",
            nb2022,
            f"{nb_percentage}%",
            delta_color="inverse",
        )

    # Duplicate the row of year 2015 of the dataframe "current_db_df" from 2016 until 2021
    for year in range(2016, 2022):
        new_row = current_db_df[current_db_df["year"] == 2015].copy()
        new_row["year"] = year
        current_db_df = pd.concat([current_db_df, new_row], ignore_index=True)

    st.subheader("Chart")
    # Draw an area chart from the dataframe "current_db_df"
    # x: year
    # y1: noise level "day"
    # y2: noise level "night"
    st.area_chart(
        current_db_df,
        x="year",
        y=["day", "night"],
        y_label="Parisians above the limit",
        use_container_width=True,
    )


# General section
st.divider()
st.header("Noise Pollution Map")

# Map "geom_x_y" string dictionary, containing "lat" and "lon", to columns "lat" and "lon" in the dataframe
gdf = arr_df["geom_x_y"].apply(lambda x: json.loads(x))
arr_df["lat"] = gdf.apply(lambda x: x["lat"])
arr_df["lon"] = gdf.apply(lambda x: x["lon"])

# Create a new dataframe that aggregates the data by zone and calculates the mean latitude and longitude for each zone
# Each zone is defined by the keys of "dict_arr", which are "north", "east", "south", "west", and "center".
# Each zone of the dataframe must aggregate the column "c_ar", which corresponds to the current arrondissement number.
# The aggregation should calculate the mean latitude and longitude for each zone based on the "lat" and "lon" columns in the dataframe.
# Result:
# zone: key of "dict_arr", lat: mean latitude, lon: mean longitude
df_agg = pd.DataFrame(columns=["zone", "lat", "lon", "pt_size", "color"])
for zone, arr in dict_arr.items():
    df_zone = arr_df[arr_df["c_ar"].isin(arr)]
    # Specify the size of the points based on the number of citizens above the limit in 2022
    citizens_above_limit = float(
        db_df[(db_df["year"] == 2022) & (db_df["location"] == zone)]["day"].iloc[0]
    )
    df_agg.loc[len(df_agg)] = [
        zone,
        df_zone["lat"].mean(),
        df_zone["lon"].mean(),
        citizens_above_limit / 20,
        COLOR_PALETTE[len(df_agg) % len(COLOR_PALETTE)],
    ]
# Duplicate all the 2022-year rows of "df_agg" for the year 2015
# And update the "pt_size" column to use the data from 2015, and "color" column to add more alpha 
df_agg_2015 = df_agg.copy()
df_agg_2015["pt_size"] = (
    db_df[db_df["year"] == 2015]["day"].iloc[0] / 20
)
df_agg_2015["color"] = [
    (c[0], c[1], c[2], .5) for c in df_agg_2015["color"]
]
df_agg = pd.concat([df_agg, df_agg_2015], ignore_index=True)

st.subheader("Noise Pollution by Arrondissement in 2022, compared to 2015")
# Draw a map with the aggregated data
st.map(df_agg, zoom=11, use_container_width=True, size="pt_size", color="color")
st.caption(
    "Drawn points are proportional to the number of citizens above the limit. The color represents the zone, and the transparency indicates the year (2022 is more opaque than 2015)."
)