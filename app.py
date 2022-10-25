import streamlit as st
import pandas as pd
import numpy as np
import csv
import subprocess
import sys
from st_aggrid import AgGrid

subprocess.run([f"{sys.executable}", "Scrape_Dubai_URLs.py"])

st.title('Properties for sale')

# with open('Location_URLs.csv', newline='') as f:
#     reader = csv.reader(f)
#     data = f.read().splitlines()

data01 = pd.read_csv('Location_URLs.csv')  
print(data01)

option = st.selectbox('Select your asset',data[:, 1:])
st.write('You selected:', option)


df = pd.read_csv('Properties_202210201625.csv') 
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#     return data

# data_load_state = st.text('Loading data...')
# data = load_data(100000)
# data_load_state.text("Done! (using st.cache)")

# if st.checkbox('Show raw data'):

st.write(df)
st.dataframe(df.style)
# st.dataframe(df, 200, 100)
# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)

# def choosing_asset():



import streamlit as st

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2 = st.columns(2)

with col1:
    st.checkbox("Disable selectbox widget", key="disabled")
    st.radio(
        "Set selectbox label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ("Email", "Home phone", "Mobile phone"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )