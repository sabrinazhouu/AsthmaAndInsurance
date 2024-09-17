import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import base64

#
# def read_sunspot():
#     """ One-time reading cleaning of sunspot data to make
#     interactive features more responsive
#
#     Returns:
#         sunspot (df): Monthly mean total sunspot number data
#     """
#     # create sunspot dataframe csv file
#     df = pd.read_csv("SN_m_tot_V2.0.csv", sep=';')
#
#     # select and assign variables to each column
#     df = df.iloc[:, [2, 3]]
#     df.columns = ['year', 'Sunspot count(monthly mean)']
#
#     return df
#
#
# # Convert a base64 image string, https://community.plotly.com/t/how-to-embed-images-into-a-dash-app/61839
# def b64_image(image_filename):
#     with open(image_filename, 'rb') as f:
#         image = f.read()
#     return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
#
#
# # read sunspot data
# sunspot = read_sunspot()
#
# # create year labels dictionary
# year_dict = {}
# # loop through years 1740-2030 by decade
# for i in range(1740, 2030, 10):
#     year_dict[i] = str(i)
#
# # define path to sun image
# image_path = 'sun_image.jpeg'

# create the layout
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Asthma Dashboard'),
    html.P('Asthma Population in the United States'),
    dcc.Graph(id='Asthma Population', style={'width': '80vw', 'height': '70vh'}),
    html.P('Choose Population range'),
    # dcc.RangeSlider(id='year slider', min=1749.042, max=2023.042, step=12,
    #                 value=[1960, 2023], marks=year_dict),
    html.P('Choose range of smoothing (Months):'),
    # dcc.Slider(id='average slider', min=0, max=24, step=1, value=5, marks=None,
    #            tooltip={"placement": "bottom", "always_visible": True}),
    dcc.Graph(id='Remote Patient Monitoring Coverage', style={'width': '100vw', 'height': '100vh'}),
    html.P('Choose a Payer:'),
    dcc.Slider(id='cycle slider', min=0, max=22, step=1, value=11),
    html.P('Current Sun')

])


# define the callback
@app.callback(
    Output('Sunspot count graph', 'figure'),
    Input('year slider', 'value'),
    Input('average slider', 'value'),
)
def line_graph(time_frame, smoothing):
    """ Plot sunspot count over time graph with adjusting time frame and moving average

        Args:
            time_frame(list): List with upper and lower bound of time frame
            smoothing(int): Chosen value to perform smoothing over
        Returns:
            fig (plot): Line plot of sunspot count over time
        """
    # calculate smooth moving averager over user given value,
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html
    sunspot['Smoothed'] = sunspot['Sunspot count(monthly mean)'].rolling(smoothing).mean()
    # set time frame to slider determined upper and lower bound
    sun_range = sunspot[(sunspot['year'] >= time_frame[0]) & (sunspot['year'] <= time_frame[1])]
    y_axis = ['Sunspot count(monthly mean)', 'Smoothed']
    # plot figure
    fig = px.line(sun_range,
                  x='year', y=y_axis,
                  title='International sunspot number Sn: Monthly mean total sunspot number',
                  )
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Mean Sunspot Count')

    return fig


# define the callback
@app.callback(
    Output('Sunspot scatter', 'figure'),
    Input('cycle slider', 'value'),
)
def scatter_plot(value):
    """ Plot sunspot count over specified cycle

            Args:
                value(int): Sunspot cycle in years
            Returns:
                fig (plot): Scatter plot of sunspot count over cycle
            """

    # transform years to overlay each cycle
    sunspot['year_fraction'] = (sunspot['year'] % value)
    # plot scatter plot
    fig = px.scatter(sunspot, x='year_fraction', y='Sunspot count(monthly mean)', title=f'Sun Cycle: {value}',
                     width=800, height=800)
    fig.update_xaxes(title_text='Year')
    fig.update_yaxes(title_text='Mean Sunspot Count(monthly)')

    return fig


# run the server
app.run_server(debug=True)
