import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Load clean data
asthma_pop_df = pd.read_csv('clean_population_data.csv')
coverage_df = pd.read_csv('coverage_df_clean.csv')
combined_df = asthma_pop_df.merge(coverage_df, left_on='States', right_on='State')
print(coverage_df)


# Generate asthma population chloropleth graph
def generate_fig(demographic):
    fig = px.choropleth(
        asthma_pop_df,
        locations='State Code',  # State Code as locations
        color=demographic,  # Color scale on population
        locationmode='USA-states',  # Set location mode to US
        scope='usa',  # Set scope to US
        hover_name='States',  # Hover show state names
        height=600,
        color_continuous_scale='Blues',  # Use selected color scale
        title='Asthma Prevalence in the United States',
    )

    fig.update_coloraxes(colorbar=dict(title='Population Count'))

    return fig


# Initialize the Dash app
app = dash.Dash(__name__,external_stylesheets=[
    {
        'href': 'https://fonts.googleapis.com/css?family=Montserrat',  # Link to custom font
        'rel': 'stylesheet'
    },
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',  # Bootstrap CSS
        'rel': 'stylesheet'
    }
])


# Define the demographic options for the dropdown
populations = {
    'Population': 'Total Population',
    'Adult Number': 'Adult Population',
    'Child Number': 'Child Population',
}

# Define the layout of the app with dropdown and graph
app.layout = html.Div([
    html.H1("Asthma Prevalence Dashboard", style={'fontFamily': 'Montserrat', 'fontSize': '36px'}),
    dcc.Dropdown(
        id='demographic-dropdown',
        options=populations,
        value='Population',  # Default color scale
        style={'width': '200px', 'fontFamily': 'Montserrat'}
    ),
    dcc.Graph(id='population-choropleth-graph', style={'width': '100vw', 'height': '100vh'}),
    dcc.Checklist(
        id='checkboxes',
        options=[
            {'label': 'Medicare', 'value': '99454 Coverage: Medicare'},
            {'label': 'Medicaid', 'value': '99454 Coverage: Medicaid'},
            {'label': 'Top Private Insurance', 'value': '99454 Coverage: Top Private Insurance'},
            {'label': 'Second Private Insurance', 'value': '99454 Coverage: Second Private Insurance'},
        ],
        value=['99454 Coverage: Medicare',
               '99454 Coverage: Medicaid',
               '99454 Coverage: Top Private Insurance',
               '99454 Coverage: Second Private Insurance'
        ],
        style={'width': '150px', 'fontFamily': 'Montserrat'},
        inline=True,
    ),
    dcc.Graph(
        id='choropleth-map', style={'width': '100vw', 'height': '100vh'}
    )
])


# Callback to update the graph when the dropdown value changes
@app.callback(
    Output('population-choropleth-graph', 'figure'),
    [Input('demographic-dropdown', 'value')]
)
def update_graph(demographic):
    # Generate the figure with the selected color scale
    updated_fig = generate_fig(demographic)
    return updated_fig


# Callback to update choropleth map based on checkbox selection
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('checkboxes', 'value')]
)
def update_choropleth(selected_checkboxes):
    # Filter the DataFrame based on selected checkboxes
    filtered_df = coverage_df[coverage_df[selected_checkboxes].sum(axis=1) == len(selected_checkboxes)]

    # Manually set colors for each state
    colors = ['#4575B4' if state_code in filtered_df['State Code'].values else '#FFFFFF' for state_code in coverage_df['State Code']]

    # Create Plotly Express choropleth map
    fig = px.choropleth(coverage_df,
                        locations='State Code',
                        locationmode="USA-states",
                        color=colors,
                        hover_name='State',
                        scope="usa",
                        title='Remote Patient Monitoring Coverage, CPT: 99454',
                        labels={'Sum': 'Selected Columns Sum'},
                        color_discrete_map={'#4575B4': '#4575B4', '#FFFFFF': '#FFFFFF'},  # Set discrete colors
                        )
    # Hide the color legend
    fig.update_traces(showlegend=False)

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
