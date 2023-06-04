import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel file
excel_file = 'Student Branch and Member count.xlsx'
df = pd.read_excel(excel_file)

# Sidebar - SB name search
search_name = st.sidebar.text_input('Enter Student Branch to search')

# Filter the data based on the search query
filtered_df = df[df['Student Branch'].str.contains(search_name, case=False)]

# Group the data by month and calculate the sum
monthly_sum = filtered_df.groupby('Feb').sum().reset_index()

# Create an animated bar chart using Plotly
fig = px.bar(monthly_sum, x='Feb', y='Count of SB Chapters/Affinity Groups', animation_frame='Feb', range_y=[0, monthly_sum['Count of SB Chapters/Affinity Groups'].max()])

# Configure the layout
fig.update_layout(
    title='Membership Growth',
    xaxis_title='Month',
    yaxis_title='Membership',
    yaxis=dict(title_standoff=30)
)

# Display the animated bar chart
st.plotly_chart(fig)
