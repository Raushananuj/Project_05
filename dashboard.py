import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
from PIL import Image
import streamlit as st
import matplotlib as plt
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings('ignore')

# Escape the backslashes
img = Image.open("C:\\Users\\Dell\\Desktop\\Next Hikes Project_5\\streamlit-logo-secondary-colormark-darktext.png")
st.image(img)


import warnings
warnings.filterwarnings('ignore')
# make containers
header = st.container()
data_sets = st.container()
featuress = st.container()
modul = st.container()
with header:
    st.title("Telecommunication Dashboard")
    st.text("This is Dataset")
with data_sets:
    df = pd.read_csv(r'C:\Users\Dell\Desktop\Next Hikes Project_5\finel_data.csv')
    st.write(df.head())
   
st.title("User Overview analysis")
st.write("Identify the top 10 handsets used by the customers")
top_10_handsets = df['Handset Type'].value_counts(ascending = False).head(10)
top_10_handsets = pd.DataFrame(top_10_handsets)
st.write(top_10_handsets.head(10))
st.text("Bar chart top 10 Handsets type")
st.bar_chart(df['Handset Type'].value_counts(ascending = False).head(10))
st.write('### Correlation Heatmap')
with data_sets:
    df1 = pd.read_csv(r'C:\Users\Dell\Desktop\Next Hikes Project_5\net_data.csv')
# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(5,4))
# Exclude non-numeric columns from correlation calculation
numeric_columns = df1.select_dtypes(include=['float64', 'int64']).columns
corr_matrix = df1[numeric_columns].corr()
# Create a heatmap using Seaborn
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
st.set_option('deprecation.showPyplotGlobalUse', False)
# Streamlit display
st.pyplot()

# cache the result so that it doesn't load everytime
@st.cache()
@st.cache_data
def long_running_function(param1, param2):
    return
def loadData():
    df = pd.read_csv(r'C:\Users\Dell\Desktop\Next Hikes Project_5\Clean_data.csv')
    df['Total Avg RTT (ms)'] = df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)']
    df['Total Avg Bearer TP (kbps)'] = df['Avg Bearer TP DL (kbps)'] + df['Avg Bearer TP UL (kbps)']
    df['Total TCP Retrans. Vol (Bytes)'] = df['TCP DL Retrans. Vol (Bytes)'] + df['TCP UL Retrans. Vol (Bytes)']

    df = df[[
        'Bearer Id',
        'IMSI',
        'MSISDN/Number',
        'IMEI',
        'Total Avg RTT (ms)',
        'Total Avg Bearer TP (kbps)',
        'Total TCP Retrans. Vol (Bytes)',
        'Handset Manufacturer',
        'Handset Type',
        'Social Media Data Volume (Bytes)',
        'Google Data Volume (Bytes)',
        'Email Data Volume (Bytes)',
        'Youtube Data Volume (Bytes)',
        'Netflix Data Volume (Bytes)',
        'Gaming Data Volume (Bytes)',
        'Other Data Volume (Bytes)',
        'Total Data Volume (Bytes)']]

    scores_df = pd.read_csv(r'C:\Users\Dell\Desktop\Next Hikes Project_5\user_engagement_data.csv')
    return df, scores_df

def displayHandsetsInfo(df):
    st.title("Users Handsets")
    st.write("")
    st.markdown("**Click the boxes to zoom in and explore all the handset manufacturers and types.**")
    plotly_plot_treemap(df)
    st.write("")
    st.markdown("**Handset manufacturers with more than 200 devices.**")
    plotly_plot_pie(df, 'Handset Manufacturer', 200)
    st.write("")
    st.markdown("**Handset types with more than 700 devices.**")
    plotly_plot_pie(df, 'Handset Type', 700)

def displayClusterInfo(df):
    st.title("User Clusters")
    st.write("")
    st.markdown("**User engagement metrics table**")
    eng_df = scores_df[['MSISDN/Number', 'xDR Sessions', 'Total Data Volume (Bytes)']]
    st.write(eng_df.head(1000))
    st.write("")
    st.markdown("**Users classified into 6 clusters based on their engagement(i.e. number of xDR sessions, duration and total data used).**")
    plotly_plot_scatter(scores_df, 'Total Data Volume (Bytes)', 'Dur. (ms)', color='cluster', size='xDR Sessions')
    st.write("")
    st.markdown("**User experience metrics table**")
    print(scores_df.columns)
    exp_df = scores_df[['MSISDN/Number','cluster','xDR Sessions','Dur. (ms)','Total Data Volume (Bytes)']]
    st.write(exp_df.head(1000))
    plotly_plot_scatter(scores_df, 'MSISDN/Number', 'cluster', 'xDR Sessions','Total Data Volume (Bytes)')
    
    st.write("")
    df1 = pd.read_csv(r'C:\Users\Dell\Desktop\Next Hikes Project_5\user_experience_data.csv')
    st.title('User experience metrix')
    st.write(df1.columns)
    # Display markdown text
    st.markdown("**Users classified into 3 clusters based on their experience(i.e. average RTT, TCP retransmission', and throughput).**")

    # Check the column names in the DataFrame
    print(scores_df.columns)

# Make sure the column name is correct and matches the case
# If the column name is incorrect, you can rename it
# For example, if the correct column name is 'Total_TCP_Retrans_Vol_Bytes'
# you can rename it as follows:
    scores_df.rename(columns={'Total TCP Retrans. Vol (Bytes)': 'Total_TCP_Retrans_Vol_Bytes'}, inplace=True)
    
# Now you can use the corrected column name in your plotting function
    #fig = px.scatter(df1, x='Total_TCP_Retrans_Vol_Bytes', y='Total Avg Bearer TP (kbps)', color='experience_cluster', size='Total Avg RTT (ms)')
    fig.show()
    st.write("")
    df2 = pd.read_csv(r'C:\Users\Dell\Desktop\Next Hikes Project_5\finaldf.csv')
    st.title('User satisfaction metrics table')
    st.markdown("**User satisfaction metrics table**")
    sat_df = df2[['MSISDN/Number', 'engagement_score', 'experience_score']]
    st.write(sat_df.head(10))
    st.write("")
    st.markdown("**Users classified into 2 clusters based on their satisfactio(i.e. engagement score and experience score).**")
    #plotly_plot_scatter(df2, 'MSISDN/Number', 'engagement_score', 'experience_score', 'MSISDN/Number')

def displayApplicationsInfo(df):
    st.title("Usage of applications")
    st.write("")
    st.markdown("**Total data used per application**")
    apps = df[['Social Media Data Volume (Bytes)',
    'Google Data Volume (Bytes)',
    'Email Data Volume (Bytes)',
    'Youtube Data Volume (Bytes)',
    'Netflix Data Volume (Bytes)',
    'Gaming Data Volume (Bytes)',
    'Other Data Volume (Bytes)']].copy(deep=True)
    apps.rename(columns={
        'Social Media Data Volume (Bytes)': 'Social Media',
        'Google Data Volume (Bytes)': 'Google',
        'Email Data Volume (Bytes)': 'Email',
        'Youtube Data Volume (Bytes)': 'Youtube',
        'Netflix Data Volume (Bytes)': 'Netflix',
        'Gaming Data Volume (Bytes)': 'Gaming',
        'Other Data Volume (Bytes)': 'Other'},
        inplace=True)
    total = apps.sum()
    total = total.to_frame('Data volume')
    total.reset_index(inplace=True)
    total.rename(columns={'index': 'Applications'}, inplace=True)
    fig = px.pie(total, names='Applications', values='Data volume')
    st.plotly_chart(fig)
    app_handsets_df = df[[
        'Handset Type',
        'Social Media Data Volume (Bytes)',
        'Google Data Volume (Bytes)',
        'Email Data Volume (Bytes)',
        'Youtube Data Volume (Bytes)',
        'Netflix Data Volume (Bytes)',
        'Gaming Data Volume (Bytes)',
        'Other Data Volume (Bytes)']]
    app_handsets_df = app_handsets_df.groupby('Handset Type').sum()
    sort_df = app_handsets_df.sort_values('Gaming Data Volume (Bytes)').head()


def advanced_exploration(df, suppress_st_warning=True):
    df = df.drop(columns=["Bearer Id"])
    pr = df.profile_report(explorative=True)
    # st_profile_report(pr)

def plotly_plot_pie(df, column, limit=None):
    a = pd.DataFrame({'count': df.groupby([column]).size()}).reset_index()
    a = a.sort_values("count", ascending=False)
    if limit:
        a.loc[a['count'] < limit, column] = f'Other {column}s'
    fig = px.pie(a, values='count', names=column, width=800, height=500)
    st.plotly_chart(fig)

def plotly_plot_treemap(df):
    fig = px.treemap(df, path=[px.Constant("Handset Manufacturers"), 'Handset Manufacturer', 'Handset Type'])
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig)

def plotly_plot_scatter(df, x_col, y_col, color, size):
    fig = px.scatter(scores_df, x=x_col, y=y_col,
                 color=color, size=size)
    st.plotly_chart(fig)

# because the data in the database doesn't change, we need to call loadData() only once
df, scores_df = loadData()
st.sidebar.title("Pages")
choices = ["Handsets", "Applications", "User Clusters"]
page = st.sidebar.selectbox("Choose Page",choices)

if page == "Handsets":
    displayHandsetsInfo(df)
    pass
elif page == "Applications":
    displayApplicationsInfo(df)
elif page == "User Clusters":
    displayClusterInfo(scores_df)