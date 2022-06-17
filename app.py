from dash import Dash, dcc, html, Input, Output
# import plotly.express as px
import plotly.graph_objects as gp

import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
df = pd.read_csv('years.csv')

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    new_df = str(df[df.year == selected_year]) + ".csv"
    print(new_df)

    # fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
    #                  size="pop", color="continent", hover_name="country",
    #                  log_x=True, size_max=55)
    y_age = new_df['Age']
    x_M = new_df['Male']
    x_F = new_df['Female'] * -1

    # fig.update_layout(transition_duration=500)
    # Creating instance of the figure
    fig = gp.Figure()
    
    # Adding Male data to the figure
    fig.add_trace(gp.Bar(y= y_age, x = x_M, 
                        name = 'Male', 
                        orientation = 'h'))

    # Adding Female data to the figure
    fig.add_trace(gp.Bar(y = y_age, x = x_F,
                        name = 'Female', orientation = 'h'))
    
    # Updating the layoutout for our graph
    fig.update_layout(title = 'Population Pyramid of Uganda-2015',
                    title_font_size = 22, barmode = 'relative',
                    bargap = 0.0, bargroupgap = 0,
                    xaxis = dict(tickvals = [-600000, -400000, -200000,
                                            0, 200000, 400000, 600000],
                                    
                                ticktext = ['6k', '4k', '2k', '0', 
                                            '2k', '4k', '6k'],
                                    
                                title = 'Population in Thousands',
                                title_font_size = 14)
                    )
    
    # fig.show()

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
