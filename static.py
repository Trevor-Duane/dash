# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as gp
import pandas as pd
import MySQLdb
from sqlalchemy import create_engine

app = Dash(__name__)

varY = 2040
my_conn = create_engine("mysql+mysqldb://root:Computers1996.@localhost/population")
query="SELECT Age, Male, Female from popdata WHERE Year={varYear}".format(varYear = varY)    
data = pd.read_sql(query,my_conn)
# data = pd.read_csv('2015_pop.csv')
print(data)

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
  
# Updating the layout for our graph
fig.update_layout(title = 'Population Pyramid',
                 title_font_size = 22, barmode = 'relative',
                 bargap = 0.0, bargroupgap = 0,
                 xaxis = dict(tickvals = [-60000000, -40000000, -20000000,
                                          0, 20000000, 40000000, 60000000],
                                
                              ticktext = ['6M', '4M', '2M', '0', 
                                          '2M', '4M', '6M'],
                                
                              title = 'Population in Millions',
                              title_font_size = 14)
                 )
  
fig.show()


if __name__ == '__main__':
    app.run_server(debug=True)