import ccxt


def build_exchange(name):
    exchange = getattr(ccxt, name)
    return exchange({
        'enableRateLimit': True
    })
