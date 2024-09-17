import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Load clean data
asthma_pop_df = pd.read_csv('clean_population_data.csv')
coverage_df = pd.read_csv('coverage_df_clean.csv')
combined_df = asthma_pop_df.merge(coverage_df, left_on='States', right_on='State')

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

# Define the layout of the app with dropdown and graph
app.layout = html.Div([
    html.H1("Asthma Prevalence Dashboard", style={'fontFamily': 'Montserrat', 'fontSize': '36px'}),
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


# Callback to update choropleth map based on checkbox selection
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('checkboxes', 'value')]
)
def update_choropleth(selected_checkboxes):
    filtered_df = combined_df[combined_df[selected_checkboxes].sum(axis=1) == len(selected_checkboxes)]

    # Create choropleth map
    fig = px.choropleth(
        filtered_df,
        locations='State Code_x',
        locationmode="USA-states",
        color='Population',
        hover_name='State',
        scope="usa",
        title='Remote Patient Monitoring Coverage, CPT: 99454',
        labels={'Sum': 'Selected Columns Sum'},
        color_continuous_scale='Blues',
        )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
