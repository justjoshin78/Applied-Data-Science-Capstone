# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


ddoptions = [{'label' : 'All Sites', 'value' : 'ALL'}]
for i in sorted(spacex_df['Launch Site'].unique()):
    ddoptions.append({'label' : i, 'value' : i})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',                                   
                                    options = ddoptions,
                                    value='ALL',
                                    placeholder="select a site",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', style={'width': '90vw'})),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={
                                        0 : '0',
                                        2500 : '2500',
                                        5000 : '5000',
                                        7500 : '7500',
                                        10000 : '10000'
                                        },
                                    value=[min_payload , max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart', style={'width': '90vw'})),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_value):
    filtered_df = spacex_df
    if selected_value == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total successful launches by site')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==selected_value]
        filtered_df = filtered_df[['Launch Site', 'class']]
        class_counts = sorted(filtered_df['class'].value_counts(dropna=True))
        filtered_df = filtered_df.sort_values('class').drop_duplicates()
        filtered_df['class_count'] = class_counts
        #print(filtered_df)
        #tmp_df.columns = {'class', 'count'}
        fig = px.pie(filtered_df, values='class_count', 
        names='class', 
        labels = 'class',
        title='Successful launches at site - {}'.format(selected_value))
        return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_chart(selected_site, selected_payloads):
    #print(selected_site)
    #print(selected_payloads[0])
    #print(selected_payloads[1])
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payloads[0]) & (spacex_df['Payload Mass (kg)'] <= selected_payloads[1])]
    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', 
            y =  'class',
            color = 'Booster Version Category')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]        
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', 
            y =  'class',
            color = 'Booster Version Category')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)
