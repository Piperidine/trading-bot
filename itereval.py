import pandas as pd
import numpy as np

import altair as alt
import seaborn as sns
from trading_bot.agent import Agent
import logging
import coloredlogs
import tensorflow as tf
import keras.backend as K

from trading_bot.utils import show_eval_result, switch_k_backend_device, get_stock_data
from trading_bot.methods import evaluate_model
tlist = ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL', 'INFRATEL', 'BRITANNIA', 'CIPLA', 'COALINDIA']
data = pd.DataFrame(columns = ['ticker','strategy','ep_count','year','investment','returns','required capital','profit','profit percentage'])

def fn(ticker,strategy,ep_count,year):
    stock = '{}'.format(ticker)
    model_name = '{}_{}_{}'.format(ticker,strategy,ep_count)
    test_stock = 'data/Nifty50/Split/{}_{}.csv'.format(ticker,year)
    window_size = 10
    debug = True
    tf.keras.backend.clear_session()
    K.clear_session()
    agent = Agent(window_size, pretrained=True, model_name=model_name)

    # read csv into dataframe
    df = pd.read_csv(test_stock)
    # df = df.iloc[:55]
    # filter out the desired features
    df = df[['Date', 'Adj Close']]
    # rename feature column names
    df = df.rename(columns={'Adj Close': 'actual', 'Date': 'date'})
    # convert dates from object to DateTime type
    dates = df['date']
    dates = pd.to_datetime(dates, infer_datetime_format=True)
    df['date'] = dates

    df.head()



    coloredlogs.install(level='DEBUG')
    switch_k_backend_device()

    test_data = get_stock_data(test_stock)
    initial_offset = test_data[1] - test_data[0]

    test_result, history = evaluate_model(agent, test_data, window_size, debug)
    show_eval_result(model_name, test_result, initial_offset)

    def visualize(df, history, title="trading session"):
        # add history to dataframe
        position = [history[0][0]] + [x[0] for x in history]
        actions = ['HOLD'] + [x[1] for x in history]
        df['position'] = position
        df['action'] = actions

        # specify y-axis scale for stock prices
        scale = alt.Scale(domain=(min(min(df['actual']), min(df['position'])) - 50, max(max(df['actual']), max(df['position'])) + 50), clamp=True)

        # plot a line chart for stock positions
        actual = alt.Chart(df).mark_line(
            color='green',
            opacity=0.5
        ).encode(
            x='date:T',
            y=alt.Y('position', axis=alt.Axis(format='$.2f', title='Price'), scale=scale)
        ).interactive(
            bind_y=False
        )

        # plot the BUY and SELL actions as points
        points = alt.Chart(df).transform_filter(
            alt.datum.action != 'HOLD'
        ).mark_point(
            filled=True
        ).encode(
            x=alt.X('date:T', axis=alt.Axis(title='Date')),
            y=alt.Y('position', axis=alt.Axis(format='$.2f', title='Price'), scale=scale),
            color='action'
        ).interactive(bind_y=False)

        # merge the two charts
        chart = alt.layer(actual, points, title=title).properties(height=300, width=1000)

        return chart

    chart = visualize(df, history, title=test_stock)

    cap = [0]
    inv = 0
    ret = 0
    b = 0
    for i in range(len(df)):
        if df.iloc[i]['action']=='BUY':
            cap.append(cap[-1]+df.iloc[i]['actual'])
            inv+=df.iloc[i]['actual']
            b+=1
        if df.iloc[i]['action']=='SELL' and b>0:
            cap.append(cap[-1]-df.iloc[i]['actual'])
            ret += df.iloc[i]['actual']
            b-=1

    req_cap = max(cap)

    prof = ret+(df['action'].value_counts().get('BUY',0)-df['action'].value_counts().get('SELL',0))*df.iloc[-1]['actual']-inv

    return pd.DataFrame([[ticker,strategy,ep_count,year,inv,ret,req_cap, prof, (prof/req_cap)*100]],columns=['ticker','strategy','ep_count','year','investment','returns','required capital','profit','profit percentage'])

for ticker in tlist:
    for ep_count in range(10,60,10):
        for year in ['2018','2019']:
            data = data.append(fn(ticker,'t-dqn',ep_count,year))

data.to_csv('./evalresults.csv')
