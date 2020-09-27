def notif():
    import requests
    from datetime import datetime
    import time

    url = 'https://fcm.googleapis.com/fcm/send'

    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "key=AAAA6s6LYFE:APA91bFNRwKoWzgY56PnPGbmVpLmMboHh1hTm8GtSM1tIIFaXPv3x0hVVl8PbH5Z5nmfkIfiJ7oi1yf3SdBVUC9VZVqeNJ4P9s2yrp0dN5HvJKkbohP3kX_mcxsHyLbjM2uj1WDVq0n4"      }

    myobj = {
        "to": "/topics/all",
        "notification": {
        "title": "Training Completed",
        "body": "Training on AWS Completed at {}:{} Hours".format(datetime.now().hour,datetime.now().minute),
        "mutable_content": True,
        "sound": "Tri-tone"
        },

    "data": {
        "url": "<url of media image>",
        "dl": "<deeplink action on tap of notification>"
        }
    }

    x = requests.post(url, headers = headers, json = myobj)

import train
ticker_list = ['ADANIPORTS', 'ASIANPAINT', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV', 'BPCL', 'BHARTIARTL', 'INFRATEL', 'BRITANNIA', 'CIPLA', 'COALINDIA', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GRASIM', 'HCLTECH', 'HDFCBANK', ]
# ticker_list = ['BJ']
for ticker in ticker_list:
    train_stock = './data/Nifty50/Split/{}_Train.csv'.format(ticker)
    val_stock = './data/Nifty50/Split/{}_Val.csv'.format(ticker)
    window_size = 10
    batch_size = 32
    ep_count = 50
    strategy = 't-dqn'
    model_name = '{}_{}'.format(ticker,strategy)
    pretrained = False
    debug = True
    train.main(train_stock, val_stock, window_size, batch_size, ep_count, strategy=strategy, model_name=model_name, pretrained=pretrained, debug=debug)

notif()
