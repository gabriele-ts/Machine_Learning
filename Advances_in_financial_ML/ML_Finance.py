import pandas as pd

def dollar_bars(tick_data, bars_per_day=14,multiplicator=1):
    '''
    Function to reasample the tick data into dollars bars
    
    Tick_data = Dataframe with single ticks of the instrument
    bars_per_day = The approximate number of bars that we want for each day
    multiplicator = The dollar value for each instrument point
    '''
    ticks= tick_data.copy()
    ticks.dropna(inplace=True)
    ticks['Dollar'] = ticks.Close * ticks.Volume*multiplicator
    average_daily_volume = ticks.Dollar.resample('D').sum().mean() #the mean of the dollar amount exchanged every day
    vol_per_bar = round(average_daily_volume/bars_per_day,-2)
    ticks['Dollarcum'] = ticks.Dollar.cumsum()
    ticks = ticks.reset_index()
    ticks.set_index('Dollarcum',inplace=True)
    index = ticks.Date_Time.groupby(ticks.index // vol_per_bar).last()
    open_ = ticks.Open.groupby(ticks.index // vol_per_bar).first()
    close = ticks.Close.groupby(ticks.index // vol_per_bar).last()
    high = ticks.High.groupby(ticks.index // vol_per_bar).max()
    low = ticks.Low.groupby(ticks.index // vol_per_bar).min()
    volume = ticks.Volume.groupby(ticks.index // vol_per_bar).sum()
    dollar_bars = pd.concat([index,open_,close,high,low,volume],axis=1)
    dollar_bars.set_index(index,inplace=True)
    dollar_bars.drop('Date_Time',axis=1,inplace=True)
    dollar_bars.dropna(inplace=True)
    return dollar_bars