import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
from PIL import Image
# Escape the backslashes
img = Image.open("C:\\Users\\Dell\\Desktop\\Next Hikes Project_5\\streamlit-logo-secondary-colormark-darktext.png")
st.image(img)
# Set page configuration
def main():
    # Call set_page_config as the first Streamlit command in your script
    st.set_page_config(page_title="Dashboard | Telecom User Data Analysis", layout="wide")
# Function to load data
def loadData():
    pd.set_option('display.max_columns', None)
    data = pd.read_csv(r'C:\Users\Dell\Desktop\Next Hikes Project_5\dashboard_data.csv')
    return data

# Function for selecting handset types
def selectHandset():
    df = loadData()
    handset = st.multiselect("Choose Handset Type(s)", list(df['Handset Type'].unique()))
    if handset:
        df = df[df['Handset Type'].isin(handset)]
        st.write(df)

# Function for selecting handset manufacturers
def selectHandsetManufac():
    df = loadData()
    manufacturer = st.multiselect("Choose Handset Manufacturer", list(df['Handset Manufacturer'].unique()))
    duration = st.multiselect("Choose Time spent on session", list(df['Dur. (ms)'].unique()))

    if manufacturer and not duration:
        df = df[df['Handset Manufacturer'].isin(manufacturer)]
        st.write(df)
    elif duration and not manufacturer:
        df = df[df['Dur. (ms)'].isin(duration)]
        st.write(df)
    elif duration and manufacturer:
        df = df[df['Handset Manufacturer'].isin(manufacturer) & df['Dur. (ms)'].isin(duration)]
        st.write(df)
    else:
        st.write(df)

# Function for creating a bar chart
def barChart(data, title, X, Y):
    title = title.title()
    st.title(f'{title} Chart')
    msgChart = (alt.Chart(data).mark_bar().encode(
        alt.X(f"{X}:N", sort=alt.EncodingSortField(field=f"{Y}", op="values", order='ascending')),
        y=f"{Y}:Q"
    ))
    st.altair_chart(msgChart, use_container_width=True)

# Function for displaying a bar chart of session counts
def stBarChart():
    df = loadData()
    dfCount = pd.DataFrame({'Session_count': df.groupby(['MSISDN/Number'])['Bearer Id'].count()}).reset_index()
    dfCount["MSISDN/Number"] = dfCount["MSISDN/Number"].astype(str)
    dfCount = dfCount.sort_values("Session_count", ascending=False)

    num = st.slider("Select number of Rankings", 0, 50, 5)
    title = f"Top {num} Sessions Ranking By User"
    barChart(dfCount.head(num), title, "MSISDN/Number", "Session_count")

# Function for displaying a bar chart of data usage by handset type
def DataUsageBarChart():
    df = loadData()
    dfCount = pd.DataFrame({'Session_count': df.groupby(['Handset Type'])['Bearer Id'].count()}).reset_index()
    dfCount["Handset Type"] = dfCount["Handset Type"].astype(str)
    dfCount = dfCount.sort_values("Session_count", ascending=False)

    num = 5
    title = f"Top {num} Sessions Ranking By Type of Handset"
    barChart(dfCount.head(num), title, "Handset Type", "Session_count")

# Function for displaying a pie chart of data usage per handset type
def DataUsagePerAppChart():
    df = loadData()
    app_data_list = ['social_media_data', 'google_data','email_data', 'youtube_data', 
                     'netflix_data', 'gaming_data', 'total_dl_ul']
    for column in app_data_list:                 
        dfLangCount = pd.DataFrame({'Data_Usage': df.groupby(['Handset Type'])[column].sum()}).head(10).reset_index()
        dfLangCount["Handset Type"] = dfLangCount["Handset Type"].astype(str)
        dfLangCount = dfLangCount.sort_values("Data_Usage", ascending=False)
        dfLangCount.loc[dfLangCount['Data_Usage'] < 10, 'Handset Type'] = 'Other Handsets'
        st.title("User data per Handsets pie chart")
        fig = px.pie(dfLangCount, values='Data_Usage', names='Handset Type', width=500, height=350)
        fig.update_traces(textposition='inside', textinfo='percent+label')

        colB1, colB2 = st.columns([2.5, 1])

        with colB1:
            st.plotly_chart(fig)
        with colB2:
            st.write(dfLangCount)

# Main function
def main():
    st.markdown("<h1 style='color:#0b4eab;font-size:36px;border-radius:10px;'>Dashboard | Telecommunication Users Data Analysis </h1>", unsafe_allow_html=True)
    selectHandset()
    selectHandsetManufac()

    st.title("Data Visualizations")
    
    with st.expander("Show More Graphs"):
        stBarChart()
        DataUsageBarChart()
        DataUsagePerAppChart()

if __name__ == "__main__":
    main()
