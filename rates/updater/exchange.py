import ccxt


def build_exchange(name):
    exchange = getattr(ccxt, name)
    return exchange({
        'enableRateLimit': True
    })

def timestamps_to_seconds(data):
    for datum in data:
        datum[0] = datum[0] // 1000

def secs_to_millis(datum):
    return datum * 1000
