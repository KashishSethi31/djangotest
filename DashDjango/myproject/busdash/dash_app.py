import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, State
from django_plotly_dash import DjangoDash
import os

# Define the absolute path to the CSV file (adjust if necessary)
csv_file_path = os.path.join(os.path.dirname(__file__), 'busdetails.csv')

# Read the CSV file
df = pd.read_csv(csv_file_path)

# Ensure BusId is treated as a string
df['BusId'] = df['BusId'].astype(str)

# Create the Dash app within Django
app = DjangoDash('BusDashApp')

app.layout = html.Div([
    html.H1("Bus Data Dashboard"),
    
    # Input field to enter Bus ID
    dcc.Input(
        id='bus-id-input',
        type='text',
        placeholder="Enter Bus ID",
        style={'margin-bottom': '20px'}
    ),
    
    # Search button to filter data based on input
    html.Button('Search', id='search-button', n_clicks=0),
    
    # Date picker to select a date
    dcc.DatePickerSingle(
        id='date-picker-single',
        date='2023-01-01',  # Default date to start
        display_format='YYYY-MM-DD',
        style={'margin-bottom': '20px', 'margin-left': '10px'}
    ),
    
    # Back button to return to the overview view
    html.Button('Back', id='back-button', n_clicks=0, style={'display': 'none'}),
    
    # Graph to display bar chart
    dcc.Graph(id='bar-chart'),
    
    # Area to display clicked data (Bus ID and Date)
    html.Div(id='click-data', style={'margin-top': '20px'}),
    
    # Store the current view mode and selected data
    dcc.Store(id='view-mode', data='overview'),
    dcc.Store(id='selected-bus-id', data=''),
    dcc.Store(id='selected-date', data='2023-01-01')
])

# Callback to update the bar chart and back button
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('back-button', 'style')],
    [Input('search-button', 'n_clicks'),
     Input('date-picker-single', 'date'),
     Input('bar-chart', 'clickData'),
     Input('back-button', 'n_clicks')],
    [State('bus-id-input', 'value'),
     State('view-mode', 'data'),
     State('selected-bus-id', 'data'),
     State('selected-date', 'data')]
)
def update_bar_chart(search_clicks, selected_date, click_data, back_clicks, bus_id, view_mode, stored_bus_id, stored_date):
    ctx = dash.callback_context
    triggered = [p['prop_id'] for p in ctx.triggered]
    
    # Check if the back button was clicked to return to the overview view
    if 'back-button' in triggered:
        view_mode = 'overview'
        return get_initial_view(), {'display': 'none'}
    
    # Filter data based on selected date
    filtered_df = df[df['Date'] == selected_date]
    
    if view_mode == 'detailed':
        # Drill down to detailed data for a selected bus
        if click_data:
            bus_id_click = click_data['points'][0]['x']
            month_df = df[(df['BusId'] == bus_id_click) & (df['Date'].str.startswith(stored_date[:7]))]
            fig = px.bar(month_df, x='Date', y='Miles', title=f'Daily Miles for Bus ID {bus_id_click} in {stored_date[:7]}')
            fig.update_layout(xaxis_title='Date', yaxis_title='Miles')
            return fig, {'display': 'block'}
        
    if bus_id:
        filtered_df = filtered_df[filtered_df['BusId'] == str(bus_id)]
        
    fig = px.bar(filtered_df, x='BusId', y='Miles', title='Miles per BusId', custom_data=['Date'])
    fig.update_traces(marker_line_color='blue', marker_line_width=2, hovertemplate='<b>Bus ID:</b> %{x}<br><b>Miles:</b> %{y}<br><b>Date:</b> %{customdata[0]}<extra></extra>')
    fig.update_layout(xaxis_title='BusId', yaxis_title='Miles')
    
    if view_mode == 'overview':
        return fig, {'display': 'none'}
    return fig, {'display': 'block'}

def get_initial_view():
    selected_date = '2023-01-01'
    filtered_df = df[df['Date'] == selected_date]
    daily_totals = filtered_df.groupby(['BusId', 'Date']).sum().reset_index()
    daily_totals = daily_totals.sort_values('BusId')
    return px.bar(daily_totals, x='BusId', y='Miles', color='Date', title=f'Total Miles per Bus per Day on {selected_date}')

# Callback to update view mode (overview or detailed)
@app.callback(
    [Output('view-mode', 'data'),
     Output('selected-bus-id', 'data'),
     Output('selected-date', 'data')],
    [Input('bar-chart', 'clickData'),
     Input('back-button', 'n_clicks')],
    [State('view-mode', 'data')]
)
def update_view_mode(click_data, back_clicks, view_mode):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == 'bar-chart' and click_data:
        bus_id_click = click_data['points'][0]['x']
        selected_date = click_data['points'][0]['customdata'][0]
        return 'detailed', bus_id_click, selected_date
    elif triggered_id == 'back-button':
        return 'overview', '', ''
    return view_mode, '', ''

# Callback to display the data clicked on the bar chart
@app.callback(
    Output('click-data', 'children'),
    [Input('bar-chart', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        bus_id = clickData['points'][0]['x']
        date = clickData['points'][0]['customdata'][0]
        return f"You clicked on Bus ID: {bus_id} on Date: {date}"
    return "Click on a bar to see Bus ID and Date details"
