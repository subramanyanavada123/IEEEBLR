import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import io
import base64
from PIL import Image
import requests

def validate_member(email):
    url = f"https://services20.ieee.org/bin/svc/ieee-webapps/membership-validator.validate-member.json?emailAddress={email}"
    response = requests.get(url)
    return response.json()

st.title("IEEE Membership Validator")

email = st.text_input("Enter your email address:")
if st.button("Validate"):
    response = validate_member(email)
    st.write(response)

# Load the Excel file
excel_file = 'Student Branch and Member count.xlsx'
df = pd.read_excel(excel_file)

# Get the column names
column_names = df.columns.tolist()
column_names[0] = 'Student Branch'

# Specify the columns to aggregate
columns_to_aggregate = ['Feb', 'Mar', 'Apr']

# Aggregate values for specified columns
aggregate_values = df[columns_to_aggregate].sum()

# Set Streamlit option to suppress warning about global pyplot usage
st.set_option('deprecation.showPyplotGlobalUse', False)

# Custom CSS styling for the table
table_style = """
    <style>
    table.dataframe {
        font-family: 'Arial', sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    table.dataframe thead th {
        background-color: #212529;
        color: #ffffff;
        border-color: #dee2e6;
    }
    table.dataframe tbody td {
        border-color: #dee2e6;
    }
    table.dataframe tbody tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    table.dataframe tbody tr:hover {
        background-color: #e9ecef;
    }
    table.dataframe tbody td {
        padding: 10px;
    }
    table.dataframe tbody td:first-child {
        font-weight: bold;
    }
    table.dataframe tbody tr td:first-child {
    display: none;
    }
</style>
"""

# Sidebar - SB name search
search_name = st.text_input('Enter Student Branch to search')

# Filter the data based on the search query
filtered_df = df[df[column_names[0]].str.contains(search_name, case=False)]


# Get unique values for each column
filters = {}
for column in column_names:
    filters[column] = ['All'] + filtered_df[column].unique().tolist()

# Apply filters
selected_values = {}
for column in column_names:
    selected_values[column] = st.sidebar.selectbox(f'Select {column}', filters[column], index=0)
    if selected_values[column] != 'All':
        filtered_df = filtered_df[filtered_df[column] == selected_values[column]]

# Interactive sorting options
sort_by = st.selectbox('Sort By', column_names)
sort_ascending = st.checkbox('Ascending', True)

# Sort the DataFrame based on selected options
sorted_df = filtered_df.sort_values(by=sort_by, ascending=sort_ascending)

# Checkbox to toggle between partial and full data display
show_full_data = st.checkbox("Show full data")

# Display the filtered data partially initially
display_df = sorted_df.head(10)  # Adjust the number of rows to display initially



# Display the filtered data using a styled table
st.subheader(f"Student Branch: {search_name}")
if show_full_data:
    components.html(table_style, height=10)  # Apply the custom CSS styling
    st.table(sorted_df)
else:
    components.html(table_style, height=0)  # Apply the custom CSS styling
    st.table(display_df)
    
if not filtered_df.empty:
    # Get the specific SB values
    sb_values = filtered_df[columns_to_aggregate].values.flatten()
    colors = ['blue', 'red', 'green', 'orange', 'purple']  # Custom colors for each line
    plt.figure(figsize=(8, 6))
    

    if(len(sb_values)>len(columns_to_aggregate)):
    # Bar plot for specific SB values
        st.subheader("The Membership growth")
        plt.bar(columns_to_aggregate, aggregate_values)
        plt.xticks(rotation=45)
        plt.xlabel("Month")
        plt.ylabel("Membership")
        st.pyplot()
    else:
        # Bar plot for specific SB values
        st.subheader("The Membership growth")
        plt.bar(columns_to_aggregate, sb_values)
        plt.xticks(rotation=45)
        plt.xlabel("Month")
        plt.ylabel("Membership")
        line_plot_fig = plt.gcf()
        st.pyplot()

    # Aggregate values for specified SB
    if(len(sb_values)>len(columns_to_aggregate)):
        # Line plot for aggregate values of specified SB
        
        st.subheader("Growth in past 3 months")
        plt.plot(columns_to_aggregate, aggregate_values)
        plt.xticks(rotation=45)
        plt.xlabel("Month")
        plt.ylabel("Aggregate Membership")
        st.pyplot()
    else:
        # Line plot for aggregate values of specified SB
        st.subheader("Growth in past 3 months")
        plt.plot(columns_to_aggregate, sb_values)
        plt.xticks(rotation=45)
        plt.xlabel("Month")
        plt.ylabel("Aggregate Membership")
        line_plot_fig = plt.gcf()
        st.pyplot()
    if st.button("Share Line Plot"):
        line_plot_buffer = io.BytesIO()
        line_plot_fig.savefig(line_plot_buffer, format='png')
        line_plot_buffer.seek(0)
        line_plot_pil = Image.open(line_plot_buffer)
        st.image(line_plot_pil, caption='Line Plot', use_column_width=True)

        # Share as a downloadable file
        line_plot_pil.save('line_plot.png')
        with open('line_plot.png', 'rb') as f:
            line_plot_bytes = f.read()
            b64_line_plot = base64.b64encode(line_plot_bytes).decode()
            href = f'<a href="data:image/png;base64,{b64_line_plot}" download="line_plot.png">Download Line Plot</a>'
            st.markdown(href, unsafe_allow_html=True)

        # Line plot using Plotly Express

