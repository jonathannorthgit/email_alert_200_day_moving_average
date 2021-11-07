import load
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def percentover200dayaverage(symbol,api_key):
    i = 0
    pricesum=0
    base_url = load.loadfile["endpoints"]["historicalprice"]
    url = base_url + symbol + "?apikey=" + api_key
    the_data = get_jsonparsed_data(url)
    while i < load.loadfile["params"]["daysback"]:
        i = i + 1
        pricesum = pricesum + the_data['historical'][i]['adjClose']
    twohundreddayaverage = pricesum / load.loadfile["params"]["daysback"]
    percent_over = ((the_data['historical'][0]['adjClose'] / twohundreddayaverage) * 100) -100
    return percent_over

def email_the_result(symbol,api_key):
    two_Hundred_day_average_stock = percentover200dayaverage(symbol, api_key)
    print two_Hundred_day_average_stock
    gmail_user = 'jonathannorthmoto@gmail.com'
    gmail_password = load.loadfile["params"]["password"]
    print(gmail_password)

    sent_from = gmail_user
    to = ['ciacciojon@gmail.com', 'jonathannorthmoto@gmail.com']
    subject = 'Daily Moving Average Alert'
    body = "Stock: " + str(symbol) + " is trading at this percent of its 200 day average : " + str(two_Hundred_day_average_stock)
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print 'Email sent!'
    except:
        print 'Something went wrong...'


