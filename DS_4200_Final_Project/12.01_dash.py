import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Load clean data
asthma_pop_df = pd.read_csv('clean_population_data.csv')
coverage_df = pd.read_csv('coverage_df_clean.csv')
df = pd.read_csv('Asthma RPM State Coverage.csv')

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
        # title='Asthma Prevalence in the United States',
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
    html.H1("Asthma Dashboard", style={'fontFamily': 'Montserrat', 'fontSize': '36px', 'marginLeft': '20px'}),
    html.Div([html.H2("Asthma Prevalence in the United States", style={'marginLeft': '40px', 'fontFamily': 'Montserrat', 'fontSize': '20px'}),],
             style={'marginTop': '40px'}),
    html.Div([dcc.Dropdown(
        id='demographic-dropdown',
        options=populations,
        value='Population',  # Default color scale
        style={'width': '200px', 'fontFamily': 'Montserrat', 'marginLeft': '20px'}
    ),
    ], style={'marginTop': '40px'}),
    dcc.Graph(id='population-choropleth-graph', style={'width': '100vw', 'height': '100vh', 'marginLeft': '20px'}),
    html.H2("Asthma Population by State", style={'marginLeft': '40px', 'fontFamily': 'Montserrat', 'fontSize': '20px'}),
    html.Div([
        dcc.Dropdown(
            id='top-n-dropdown',
            options=[
                {'label': f'Top {i} States', 'value': i} for i in range(5, df.shape[0] + 1, 5)
            ],
            value=5,
            multi=False,
            style={'width': '50%', 'marginLeft': '40px', 'fontFamily': 'Montserrat'}
        ),
    ], style={'marginTop': '40px'}),
    html.Div([
        dcc.Graph(id='stacked-bar-chart', style={'marginTop': '100px', 'width': '100vw', 'marginLeft': '20px'})
    ], style={'marginLeft': '20px'}),
    html.Div([html.H2("Remote Patient Monitoring Insurance Coverage, CPT: 99454", style={'marginLeft': '40px', 'fontFamily': 'Montserrat', 'fontSize': '20px'}),], style={'marginLeft': '20px'}),
    html.Div([dcc.Checklist(
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
        style={'width': '150px', 'fontFamily': 'Montserrat', 'marginLeft': '50px'},
        inline=True,
    ),], style={'marginTop': '40px'}),
    dcc.Graph(
        id='choropleth-map', style={'width': '100vw', 'height': '100vh'}
    ),

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
                        # title='Remote Patient Monitoring Coverage, CPT: 99454',
                        labels={'Sum': 'Selected Columns Sum'},
                        color_discrete_map={'#4575B4': '#4575B4', '#FFFFFF': '#FFFFFF'},  # Set discrete colors
                        )
    # Hide the color legend
    fig.update_traces(showlegend=False)

    return fig


# Melt the DataFrame to have 'State' as a column and 'Adult' and 'Child' as values
melted_df = pd.melt(df, id_vars=['US States'],
                    value_vars=['Adult Asthma Population Number', 'Child Asthma \nPopulation Number'],
                    var_name='Age Group', value_name='Population')

# Remove commas and convert 'Population' to numeric for correct counting
melted_df['Population'] = pd.to_numeric(melted_df['Population'].str.replace(',', ''), errors='coerce')

# Define callback to update the chart based on the selected top-n value
@app.callback(
    dash.dependencies.Output('stacked-bar-chart', 'figure'),
    [dash.dependencies.Input('top-n-dropdown', 'value')]
)
def update_chart(top_n):
    sorted_df = df.copy()
    sorted_df['Total Asthma Population'] = sorted_df['Total Asthma Population'].str.replace(',', '').astype(int)
    sorted_df = sorted_df.sort_values(by='Total Asthma Population', ascending=False).head(top_n)

    melted_sorted_df = pd.melt(sorted_df, id_vars=['US States'],
                                value_vars=['Adult Asthma Population Number', 'Child Asthma \nPopulation Number'],
                                var_name='Age Group', value_name='Population')

    melted_sorted_df['Population'] = pd.to_numeric(melted_sorted_df['Population'].str.replace(',', ''),
                                                    errors='coerce')

    fig = px.bar(
        melted_sorted_df,
        x='US States',
        y='Population',
        color='Age Group',
        # title=f'Top {top_n} States - Asthma Population by Age Group',
        labels={'Population': 'Population'},
        color_discrete_map={'Adult Asthma Population Number': 'grey', 'Child Asthma Population Number': 'purple'},
        barmode='stack'
    )

    # Adjust the figure height and rotate x-axis labels
    fig.update_layout(height=600, width=1200, xaxis_tickangle=-45)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)