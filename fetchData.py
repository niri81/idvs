import configparser
import json
import logging
from datetime import datetime
import requests

# define urls
atisUrl = 'https://api.ivao.aero/v2/tracker/whazzup/atis'

# get token from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
token = config['DEFAULT']['TOKEN']


def fetch_content(url):
    logging.info("Requesting Whazzup ATIS data")
    response = requests.get(url)
    if response.status_code == 200:
        logging.debug("Received data")
        return response.content
    else:
        logging.error(f"Status code received was {response.status_code}")


def fetch_whazzup():
    content = fetch_content(atisUrl)
    logging.debug("Loading data")
    content = json.loads(content)
    logging.info("Returning Whazzup ATIS data")
    return content


def get_utc_hour():
    logging.debug("Fetching UTC hour")
    return str(
        datetime.utcnow().time().hour) if datetime.utcnow().time().hour >= 10 else f"0{datetime.utcnow().time().hour}"


def get_utc_minute():
    logging.debug("Fetching UTC minute")
    return str(
        datetime.utcnow().time().minute) if datetime.utcnow().time().minute >= 10 else f"0{datetime.utcnow().time().minute}"


def get_utc_second():
    logging.debug("Fetching UTC second")
    return str(
        datetime.utcnow().time().second) if datetime.utcnow().time().second >= 10 else f"0{datetime.utcnow().time().second}"
