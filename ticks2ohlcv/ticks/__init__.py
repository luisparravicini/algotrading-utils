from datetime import datetime
import csv

def to_ohlcv(path_in, path_out, interval):
    interval *= 60

    with open(path_out, 'w') as file_out:
        writer = csv.writer(file_out)
        writer.writerow(('date', 'open', 'high', 'low', 'close', 'volume'))

        with open(path_in, 'r') as file:
            frame_date = None

            for row in csv.reader(file):
                row_date = int(row[0])
                if frame_date is None or frame_date + interval <= row_date:
                    if frame_date is not None:
                        write_row(frame_date, frame_prices, volume, writer)

                    frame_date = row_date - row_date % interval

                    frame_prices = list()
                    volume = 0
                
                frame_prices.append(float(row[1]))
                volume += float(row[2])
            
            if len(frame_prices) > 0:
                write_row(frame_date, frame_prices, volume, writer)

def format_float(x):
    return '%.4f' % x

def write_row(frame_date, frame_prices, volume, writer):
    out_date = datetime.fromtimestamp(frame_date)
    out_row = (
        out_date.strftime('%Y-%m-%d %H:%M:%S'),
        format_float(frame_prices[0]),
        format_float(max(frame_prices)),
        format_float(min(frame_prices)),
        format_float(frame_prices[-1]),
        format_float(volume)
    )
    writer.writerow(out_row)
