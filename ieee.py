import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

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
            font-family: Arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        table.dataframe th, table.dataframe td {
            border: 1px solid #ddd;
            padding: 8px;
        }

        table.dataframe th {
            background-color: #f2f2f2;
        }

        table.dataframe tr:nth-child(even) {
            background-color: #f8f8f8;
        }

        table.dataframe tr:hover {
            background-color: #ddd;
        }
    </style>
"""

# Sidebar - SB name search
search_name = st.text_input('Enter Student Branch to search')

# Filter the data based on the search query
filtered_df = df[df[column_names[0]].str.contains(search_name, case=False)]

# Display the filtered data partially initially
display_df = filtered_df.head(10)  # Adjust the number of rows to display initially

# Checkbox to toggle between partial and full data display
show_full_data = st.checkbox("Show full data")

# Display the filtered data using a styled table
st.subheader(f"Student Branch: {search_name}")
if show_full_data:
    components.html(table_style, height=0)  # Apply the custom CSS styling
    st.table(filtered_df)
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
        st.pyplot()
