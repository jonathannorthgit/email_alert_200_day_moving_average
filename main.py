import load
from percent_over_200_day_average import email_the_result

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json
def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


email_the_result(load.loadfile['Stocks']['Stock1'],load.loadfile['endpoints']['api_key'])
email_the_result(load.loadfile['Stocks']['Stock2'],load.loadfile['endpoints']['api_key'])


