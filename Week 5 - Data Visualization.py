# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

# Create a dash application
app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
# app.config.suppress_callback_exceptions = True

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'All Launch Sites', 'value': 'All Launch Sites'}
                                        ,],
                                    value='All Launch Sites', placeholder='All Launch Sites',
                                    style={'textAlign': 'center', 'width': '80%', 'padding': '3px', 'font-size': '20px'}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                #,
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=0, max=10000, step=1000, value=[min_payload,max_payload],
                                    id='payload-slider'
                                    ),
                                html.Br(),
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output("success-pie-chart", component_property='figure'), Input(component_id='site-dropdown', component_property='value'))

def get_graph(site_inputted):
    if site_inputted == "All Launch Sites":
        df_temp = spacex_df
        pie_data = df_temp
        fig = px.pie(pie_data, values='class', names='Launch Site',
                     title='Total success launches by Site')
    else:
        df_temp = spacex_df[spacex_df['Launch Site'] == site_inputted]
        pie_data = df_temp[['class','Launch Site','Flight Number']].groupby(['class', 'Launch Site']).count().reset_index()
        fig = px.pie(pie_data, values='Flight Number', names='class',
                     title='Total success launches for '+site_inputted)

    fig.update_layout()
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output("success-payload-scatter-chart", component_property='figure'), [Input(component_id='payload-slider', component_property='value'),Input(component_id='site-dropdown', component_property='value')])

def get_graph2(slider_input, site_inputted):
    if site_inputted == "All Launch Sites":
      df_temp2 = spacex_df[(spacex_df['Payload Mass (kg)'] >= slider_input[0]) & (spacex_df['Payload Mass (kg)'] <= slider_input[1])]
    else:
      df_temp2 = spacex_df[(spacex_df['Launch Site'] == site_inputted) & (spacex_df['Payload Mass (kg)'] >= slider_input[0]) & (spacex_df['Payload Mass (kg)'] <= slider_input[1])]
    print(slider_input[0])
    scatter_data = df_temp2[['class','Booster Version Category','Payload Mass (kg)']]
    fig2 = px.scatter(scatter_data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                          title='Correlation between Payload and Success for ' + site_inputted)
    fig2.update_layout()
    return fig2


# Run the app
if __name__ == '__main__':
    app.run_server(port='64267')




















