import os
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

# Dynamically determine the path to the CSV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(BASE_DIR, 'irisDataset.csv')

# Ensure the CSV file exists
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

# Load the CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Determine the minimum and maximum values from the first column
first_column_name = df.columns[0]
min_value = df[first_column_name].min()
max_value = df[first_column_name].max()

# Initialize the Dash app
app = DjangoDash('my_dash_app')

# Round min and max values to whole numbers for the slider
min_value_rounded = int(min_value)
max_value_rounded = int(max_value) + 1

# Generate marks for the slider
marks = {i: str(i) for i in range(min_value_rounded, max_value_rounded + 1)}

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Histogram of First Column of Iris Dataset", className='dash-title'),
    dcc.Slider(
        id='bins-slider',
        min=min_value_rounded,
        max=max_value_rounded,
        step=1,
        value=min_value_rounded,
        marks=marks,
        tooltip={"placement": "bottom", "always_visible": True},
        className='dash-slider'
    ),
    html.Div(
        dcc.Graph(id='histogram', className='dash-graph'),
        className='dash-graph-container'
    )
], className='dash-container')

# Define the callback to update the histogram
@app.callback(
    Output('histogram', 'figure'),
    [Input('bins-slider', 'value')]
)
def update_histogram(selected_value):
    filtered_df = df[df[first_column_name] <= selected_value]
    fig = px.histogram(
        filtered_df,
        x=first_column_name,
        nbins=20,
        title=f"Histogram of {first_column_name} (Up to {selected_value})",
        labels={first_column_name: first_column_name},
        template='plotly_white'
    )
    fig.update_layout(
        xaxis_title=first_column_name,
        yaxis_title="Count",
        bargap=0.1,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig
