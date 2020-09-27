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