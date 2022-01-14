import requests
import json

url = 'https://www.floatrates.com/daily/{0}.json'


def check_status(res):
    return True if res.status_code == 200 else False


def get_code(code_from, code_to):
    if code_from == code_to:
        cache[code_from][code_to] = 1
        return 1
    else:
        resp = requests.get(url.format(code_from))
        if not check_status(resp):
            return False
        currency = json.loads(resp.text)
        if currency.get(code_to):
            rate = currency.get(code_to).get('rate')
            cache[code_from][code_to] = rate
            return rate
    return False


def print_calculation(no_of_coins, rate, code):
    print(f'You received {no_of_coins * rate:.2f} {code.upper()}.')


def exchange(code_from, code_to, no_of_coins):
    print('Checking the cache...')
    cache_hit = cache.get(code_from).get(code_to, False)
    if cache_hit:
        print('Oh! It is in the cache!')
        print_calculation(no_of_coins, cache_hit, code_to)
    else:
        print('Sorry, but it is not in the cache!')
        rate = get_code(code_from, code_to)
        if rate:
            print_calculation(no_of_coins, rate, code_to)
        else:
            print('Cannot calculate the amount')


cache = dict()

currency_from = input('').lower().strip()
cache[currency_from] = dict()
get_code(currency_from, 'eur')
get_code(currency_from, 'usd')

while True:
    try:
        currency_to = input('').lower()
        if not currency_to:
            break
        coins = float(input(''))
        exchange(currency_from, currency_to, coins)
    except ValueError:
        print('Only number is allowed for the last input')

