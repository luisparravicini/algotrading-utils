from datetime import datetime
import pandas as pd


def to_ohlcv(data_file):
    # minutes
    interval = 1

    # dparser = lambda x: datetime.fromtimestamp(int(x))
    df = pd.read_csv(data_file, names=['date','price','volume'])
                    # parse_dates=[0], date_parser=dparser)

    agg_data = list()
    for _name, group in df.groupby(df['date'] / 60):
        print(group)
        agg_data.append((
            group['date'].min(),
            group['price'].mean(),
            group['volume'].mean()
        ))

    return pd.DataFrame(agg_data, columns=list(df.columns))
