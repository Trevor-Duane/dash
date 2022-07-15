# twitter profiles name
user_names = [
    'AcalaNetwork',
    'ParallelFi',
    'MoonbeamNetwork',
    'BitDotCountry',
    'ShidenNetwork',
    'bifrost_finance',
    'Kiltprotocol',
    'CrustNetwork',
    'EquilibriumDeFi',
    'NodleNetwork',
    'polkadex',
    'centrifuge',
    'integri_t_e_e',
    'hydra_dx',
    'PhalaNetwork',
    'RmrkApp',
    'ComposableFin',
    'Picasso_Network',
    'efinityio',
    'ZeitgeistPM',
    'MangataFinance'
]
# Dropdown selector
user_dropdown = html.Div(
    [
        dcc.Dropdown(
            id='fig_dropdown',
            options=[
                {'label': x, 'value': x} for x in user_names
            ],
            value='AcalaNetwork',
            searchable=True,
            clearable=False,
            style={
                'marginLeft': '20px',
                'marginRight': '80px',
                'align': 'center'
            }
        )
    ]
)
So in the callback I just specified the CSV file path and based on the selected value from the dropdown I read that particular CSV file

Code for dropdown callback:

# Callbacks
@twitter_app.callback(
    [
        Output('date-range', 'min_date_allowed'),
        Output('date-range', 'max_date_allowed'),
        Output('date-range', 'start_date'),
        Output('date-range', 'end_date'),
        Output('local', 'data'),
    ],
    Input('fig_dropdown', 'value')
)
def update_output(value):
    if value:
        filepath = "../data/processed_data/processed_sentiment_"
        currfile = filepath + value + "_tweets.csv"
        df = pd.read_csv(currfile, engine='python')
        df['user_created_at'] =  pd.to_datetime(df['user_created_at'], infer_datetime_format=True)
        df['tweet_created_at'] =  pd.to_datetime(df['tweet_created_at'], infer_datetime_format=True)
        df['date_only'] = df['tweet_created_at'].dt.date

        # creating a copy of df
        return (
            df['date_only'].min(), 
            df['date_only'].max(), 
            df['date_only'].min(), 
            df['date_only'].max(),
            df.to_dict('records')
        )
    else:
        raise dash.exceptions.PreventUpdate
The last code contains a chained callback to plot all the graphs

@twitter_app.callback(
    Output('follower-count', 'children'),
    Output('following-count', 'children'),
    Output('tweet-trend', 'figure'),
    Output('pie-chart', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    State('local', 'data')
)
def update_plot(start_date, end_date, data):
    df = pd.DataFrame(data)
    mask = (
        (df.date_only >= start_date)
        & (df.date_only <= end_date)
    )
    # Filtered data as per start_date, end_date 
    filtered_df = df.loc[mask, :]
    sentiment_label(filtered_df)
    
    # returing the plots
    return (
        f"Followers count: {filtered_df['user_followers_count'].to_list()[0]}",
        f"Followings count: {filtered_df['user_tweet_count'].to_list()[0]}",
        tweet_trend_chart(filtered_df),
        pie_chart(filtered_df)
    )