# currency.py

import argparse
from configparser import ConfigParser
from datetime import date, datetime
import requests

BASE_URL = "https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from_cur}&amount={amount}"


def _get_key():
    configuration = ConfigParser()
    configuration.read("secrets.ini")
    return configuration["APILayer"]["api_key"]


def read_user_cli_arguments():
    cur_date = date.today()
    parser = argparse.ArgumentParser(description="Converts amount from one currency into another")
    parser.add_argument("from", nargs="+", type=str, help="Enter the three letter currency code you want to convert from")
    parser.add_argument("to", nargs="+", type=str, help="Enter the three letter currency code you want to convert to")
    parser.add_argument("amount", nargs="+", type=float, help="Enter the amount of money")
    parser.add_argument("date", nargs="?", const=cur_date, type=date, default=cur_date, help="Enter the date (optional, for historical purposes)")
    return parser.parse_args()  #To access the dictionary variant, use vars()


def convert(cur_from, cur_to, cur_amount, ent_date):
    apikey = _get_key()
    headers = { "apikey" : apikey}
    cur_date_m = datetime.strftime(date.today(), format="%Y-%m-%d")
    ent_date_m = datetime.strftime(ent_date, format="%Y-%m-%d")
    if ent_date_m == cur_date_m:
        CONSTRUCTED_URL = BASE_URL.format(to = cur_to, from_cur = cur_from, amount = cur_amount)
    response = requests.request("GET", CONSTRUCTED_URL, headers = headers)
    if response.status_code == 200:
        return response.json()


if __name__ == "__main__":  
    result = read_user_cli_arguments()
    dictionary = vars(result)
    ans_set = convert(dictionary["from"][0], dictionary["to"][0], dictionary["amount"][0], dictionary["date"])
    print ("\n\b\b\b\b", dictionary["amount"][0], dictionary["from"][0], "is equal to", ans_set["result"], dictionary["to"][0], "as of", dictionary["date"])
    print (" Current exchange rate: 1", dictionary["from"][0], "=", ans_set["info"]["rate"], dictionary["to"][0], "\n")

