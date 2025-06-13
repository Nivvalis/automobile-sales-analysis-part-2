#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Dropdown options and year list
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Statistics'}
]
year_list = sorted(data['Year'].unique())

# Layout
app.layout = html.Div([
    html.H1("Automobile Sales Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='statistics-dropdown',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a statistics category'
        )
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value=year_list[0]
        )
    ]),

    html.Div(id='output-container', className='output-container', style={'marginTop': '20px'})
])

# Enable/Disable year selection based on dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('statistics-dropdown', 'value')
)
def toggle_year_dropdown(selected):
    return selected == 'Recession Statistics'

# Callback to render graphs
@app.callback(
    Output('output-container', 'children'),
    Input('statistics-dropdown', 'value'),
    Input('select-year', 'value')
)
def update_dashboard(selected_stats, selected_year):
    if selected_stats == 'Recession Statistics':
        recession_data = data[data['Recession'] == 1]

        # Chart 1: Average Sales Over Recession Years
        sales_over_time = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(sales_over_time, x='Year', y='Automobile_Sales', title='Average Sales Over Recession'))

        # Chart 2: Avg Vehicles Sold by Type
        avg_sales_by_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart2 = dcc.Graph(figure=px.bar(avg_sales_by_type, x='Vehicle_Type', y='Automobile_Sales', title='Avg Sales by Vehicle Type'))

        # Chart 3: Ad Spend Share by Vehicle Type
        ad_exp = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart3 = dcc.Graph(figure=px.pie(ad_exp, names='Vehicle_Type', values='Advertising_Expenditure', title='Ad Spend Share by Vehicle Type'))

        # Chart 4: Effect of Unemployment
        unemployment_effect = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        chart4 = dcc.Graph(figure=px.bar(unemployment_effect, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', title='Unemployment Effect'))

        return [
            html.Div([chart1, chart2], style={'display': 'flex', 'flexWrap': 'wrap'}),
            html.Div([chart3, chart4], style={'display': 'flex', 'flexWrap': 'wrap'})
        ]

    elif selected_stats == 'Yearly Statistics':
        yearly_data = data[data['Year'] == selected_year]

        # Chart 1: Line chart for all years
        all_years = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(all_years, x='Year', y='Automobile_Sales', title='Yearly Sales Over Time'))

        # Chart 2: Monthly sales for selected year
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        chart2 = dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title=f'Monthly Sales in {selected_year}'))

        # Chart 3: Average sales by vehicle type
        avg_sales_type = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart3 = dcc.Graph(figure=px.bar(avg_sales_type, x='Vehicle_Type', y='Automobile_Sales', title=f'Avg Sales by Type in {selected_year}'))

        # Chart 4: Pie chart for ad expenditure by type
        ad_expenditure = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        chart4 = dcc.Graph(figure=px.pie(ad_expenditure, names='Vehicle_Type', values='Advertising_Expenditure', title=f'Ad Spend by Type in {selected_year}'))

        return [
            html.Div([chart1, chart2], style={'display': 'flex', 'flexWrap': 'wrap'}),
            html.Div([chart3, chart4], style={'display': 'flex', 'flexWrap': 'wrap'})
        ]
    return html.Div("No data to display")

# Run server
if __name__ == '__main__':
    app.run(debug=True)