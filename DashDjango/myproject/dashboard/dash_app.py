# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import pandas as pd
# import plotly.express as px



# # Create Dash app instance
# app = dash.Dash(__name__)

# # Define the layout of the Dash app
# app.layout = html.Div([
#     dcc.Input(id='input', value='Hello', type='text'),
#     html.Div(id='output')
# ])

# # Define the callback
# @app.callback(Output('output', 'children'),
#               [Input('input', 'value')])
# def update_output(value):
#     return f'You have entered: {value}'

# # Expose the Dash server to be used by Django
# server = app.server

# dashboard/dash_app.py
# dashboard/dash_app.py
# dash_app.py
# dash_app.py
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

# Path to your CSV file
csv_file_path = '/Users/kashishsethi/Desktop/DashDjango/myproject/dashboard/irisDataset.csv'

# Load the CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Determine the minimum and maximum values from the first column
first_column_name = df.columns[0]
min_value = df[first_column_name].min()
max_value = df[first_column_name].max()

def create_dash_app():
    # Initialize the Dash app
    app = DjangoDash('my_dash_app')

    # Round min and max values to whole numbers for the slider
    min_value_rounded = int(min_value)
    max_value_rounded = int(max_value) + 1  # Ensure the max value is included

    # Calculate step size for the slider
    range_span = max_value_rounded - min_value_rounded
    num_marks = range_span // 1  # Use integer division to get whole number steps
    step_size = 1

    # Generate marks based on the step_size
    marks = {i: str(i) for i in range(min_value_rounded, max_value_rounded + 1, step_size)}

    # Define the layout of the Dash app
    app.layout = html.Div([
        # Title
        html.H1("Histogram of First Column of Iris Dataset", className='dash-title'),

        # Slider to select the range of values in the x-axis
        dcc.Slider(
            id='bins-slider',
            min=min_value_rounded,
            max=max_value_rounded,
            step=step_size,
            value=min_value_rounded,
            marks=marks,
            tooltip={"placement": "bottom", "always_visible": True},
            className='dash-slider'  # Apply CSS class for styling
        ),

        # Container for the graph
        html.Div(
            dcc.Graph(id='histogram', className='dash-graph'),
            className='dash-graph-container'
        )
    ], className='dash-container')

    # Define the callback to update the histogram based on the selected value from the slider
    @app.callback(
        Output('histogram', 'figure'),
        [Input('bins-slider', 'value')]
    )
    def update_histogram(selected_value):
        # Filter the DataFrame based on the slider value
        filtered_df = df[df[first_column_name] <= selected_value]

        # Create the histogram using the filtered DataFrame
        fig = px.histogram(
            filtered_df,
            x=first_column_name,
            nbins=20,  # You can adjust the number of bins if needed
            title=f"Histogram of {first_column_name} (Up to {round(selected_value, 2)})",
            labels={first_column_name: first_column_name},
            template='plotly_white'
        )
        fig.update_layout(
            xaxis_title=first_column_name,
            yaxis_title="Count",
            bargap=0.1,
            title_font=dict(size=24, color='black', family='Arial'),
            xaxis_title_font=dict(size=18, color='black', family='Arial'),
            yaxis_title_font=dict(size=18, color='black', family='Arial'),
            margin=dict(l=50, r=50, t=50, b=50)  # Adjust the margins to ensure the graph is well-centered
        )
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
        return fig

    return app
