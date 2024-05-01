"""
PhonePe Data Visualization and Exploration

This package provides utilities for visualizing and exploring data related to PhonePe,
India's leading digital payment platform. It utilizes streamlit for creating an
interactive web application and various data analysis and visualization libraries
such as pandas, plotly, and psycopg2.

Modules:
    - phonepe: Main module containing the Streamlit app and data processing functions.
    - data_loader: Module for loading and preprocessing data from various sources.
    - visualizations: Module containing functions for creating different types of visualizations.
    - utils: Module with utility functions for data manipulation and analysis.

Example:
    To run the Streamlit app, use the following command from the project root directory:
        streamlit run phonepe/phonepe.py
"""



# Import modules from the project
from phonepe import (
mydb,
cursor,
aggregated_insurance_data,
aggregated_insurance_df,
aggregated_transaction_data,
aggregated_transaction_df,
aggregated_user_data,
aggregated_user_df,
map_insurance_data,
map_insurance_df,
map_transaction_data,
map_transaction_df,
map_user_data,
map_user_df,
top_insurance_data,
top_insurance_df,
top_transaction_data,
top_transaction_df,
top_user_data,
top_user_df,
data1)