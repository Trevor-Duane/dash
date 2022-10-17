from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as gp
import pandas as pd
import MySQLdb
import mysql.connector
from sqlalchemy import create_engine

app = Dash(__name__)

conn = mysql.connector.connect(host="localhost",database="population",user="root",password="Computers1996." )
cursor = conn.cursor()
cursor.execute("SELECT Distinct Year FROM popdata")
years = []
for row in cursor:
    for field in row:
        int(field)
        years.append('{}'.format(field))

# print(years)

app.layout = html.Div(
    [
        html.H4("Population Pyramid Graph for years 2014 - 2040", style={'text-align': 'center', 'margin':'1px'}),

        dcc.Dropdown(
            id='select_year',
            options=[
                {'label': x, 'value': x} for x in years
            ],
            value='2014',
            searchable=True,
            clearable=False,
            style={
                'marginLeft': '20px',
                'marginRight': '80px',
                'align': 'center'
            }
        ),
        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id='my_ppyramid', figure={})
    ]
)


# Callbacks to connect the plotly graphs with the components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
      Output(component_id='my_ppyramid', component_property='figure'),],
    [Input(component_id='select_year', component_property='value')]
)


def update_output(value):
    if value:
        varY = value 
        my_conn = create_engine("mysql+mysqldb://root:Computers1996.@localhost/population")
        query="SELECT Age, Male, Female from popdata WHERE Year={varYear}".format(varYear = varY)    
        data = pd.read_sql(query,my_conn)
        print(data)

        container = html.P("Your are viewing population graph Date of {}".format(value), style={'margin':'2px 0px 2px 40px'})

        y_age = data['Age']
        x_M = data['Male']
        x_F = data['Female'] * -1

        # Creating instance of the figure
        fig = gp.Figure()

        # Adding Male data to the figure
        fig.add_trace(gp.Bar(y= y_age, x = x_M, 
                            name = 'Male', 
                            orientation = 'h'))

        # Adding Female data to the figure
        fig.add_trace(gp.Bar(y = y_age, x = x_F,
                            name = 'Female', orientation = 'h'))
        
        # Updating the layout http://tendasuites.com/gallery/out for our graph
        fig.update_layout(
                        title_font_size = 22, barmode = 'relative',
                        bargap = 0.0, bargroupgap = 0, height = 800, paper_bgcolor="LightSteelBlue",
                        xaxis = dict(tickvals = [-600000, -400000, -200000,
                                                0, 200000, 400000, 600000],
                                        
                                    ticktext = ['6k', '4k', '2k', '0', 
                                                '2k', '4k', '6k'],
                                        
                                    title = 'Population in Thousands',
                                    title_font_size = 14)
                        )

        return container, fig
    

    else:
        raise dash.exceptions.PreventUpdate


#___________________________________________________________________
if __name__ == '__main__':
    app.run_server(debug=True)