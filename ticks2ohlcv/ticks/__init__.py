from datetime import datetime
import pandas as pd

def to_ohlcv(data_file, interval, verbose=False):
    interval *= 60

    if verbose:
        print('reading')
    # dparser = lambda x: datetime.fromtimestamp(int(x))
    df = pd.read_csv(data_file, names=['date','price','volume'])
                    # parse_dates=[0], date_parser=dparser)

    if verbose:
        print('grouping')
    agg_data = list()
    for _name, group in df.groupby(df['date'] // interval):
        min_date = group['date'].min()
        agg_data.append((
            min_date - min_date % interval,
            group['price'].iloc[0],
            group['price'].max(),
            group['price'].min(),
            group['price'].iloc[-1],
            group['volume'].sum()
        ))

    if verbose:
        print('creating new data frame')

    columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    return pd.DataFrame(agg_data, columns=columns)

def export_dataframe(file, data_frame):
    data_frame.to_csv(file, index=False, float_format='%.4f')
