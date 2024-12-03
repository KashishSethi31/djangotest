# dashboard/apps.py
from django.apps import AppConfig
from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px



# class DashboardConfig(AppConfig):
#     name = 'dashboard'

#     def ready(self):
#         # Define the Dash app
#         app = DjangoDash('my_dash_app')

#         # Define the layout of the Dash app
#         app.layout = html.Div([
#             dcc.Input(id='input', value='Hello', type='text'),
#             html.Div(id='output')
#         ])

#         # Define the callback
#         @app.callback(Output('output', 'children'),
#                       [Input('input', 'value')])
#         def update_output(value):
#             return f'You have entered: {value}'




# class DashboardConfig(AppConfig):
#     app = dash.Dash(__name__)
#     name = 'dashboard'
#     def ready(self):
#         # Define the Dash app
#         app = DjangoDash('my_dash_app')
#         # Path to your CSV file
#         csv_file_path = '/Users/kashishsethi/Desktop/DashDjango/myproject/dashboard/irisDataset.csv'

#         # Load the CSV data into a DataFrame
#         df = pd.read_csv(csv_file_path)

#         # Assuming the first column is unnamed or has a name like 'col1', we'll use it for the histogram
#         first_column_name = df.columns[0]
        
#     # Define the layout of the Dash app
#         app.layout = html.Div([
#             html.H1("Histogram of First Column of Iris Dataset", style={'text-align': 'center'}),

#             # Slider to select the number of bins
#             dcc.Slider(
#                 id='bins-slider',
#                 min=5,
#                 max=50,
#                 step=1,
#                 value=20,
#                 marks={i: str(i) for i in range(5, 51, 5)},
#                 tooltip={"placement": "bottom", "always_visible": True},
#             ),

#             # Histogram plot
#             dcc.Graph(id='histogram')
#         ])

#         # Define the callback to update the histogram based on the selected number of bins
#         @app.callback(
#             Output('histogram', 'figure'),
#             [Input('bins-slider', 'value')])
#         def update_histogram(bins):
#             # Create the histogram using the first column
#             fig = px.histogram(
#                 df,
#                 x=first_column_name,
#                 nbins=bins,
#                 title=f"Histogram of {first_column_name}",
#                 labels={first_column_name: first_column_name},
#                 template='plotly_white'
#             )
#             fig.update_layout(
#                 xaxis_title=first_column_name,
#                 yaxis_title="Count",
#                 bargap=0.1
#             )
#             return fig
#     server = app.server



from django.apps import AppConfig

class DashboardConfig(AppConfig):
    name = 'dashboard'


