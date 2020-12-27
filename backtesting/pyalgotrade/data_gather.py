from datetime import datetime, date, timedelta
import pandas as pd
import ccxt

exchange = ccxt.binance()

def gather_data():
    symbol = 'BTC/USDT'

    yesterday = date.today() - timedelta(days=1)
    start_date = datetime.combine(yesterday, datetime.min.time())
    start_stamp = int(start_date.timestamp()) * 1000

    one_day = 24 * 60

    print(f'fetching data from {start_date.date().isoformat()}')
    data = exchange.fetch_ohlcv(symbol, timeframe='1m',
                                since=start_stamp, limit=one_day)

    df = pd.DataFrame(data)
    df.columns = (["Date Time", "Open", "High", "Low", "Close", "Volume"])

    def parse_dates(ts):
        return datetime.fromtimestamp(ts/1000.0)

    df["Date Time"] = df["Date Time"].apply(parse_dates)
    df.to_csv("sampledata.csv", index=False)

def main():
    gather_data()



if __name__ == "__main__":
    main()
