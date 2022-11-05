# currency.py

import argparse
from configparser import ConfigParser
from datetime import date

BASE_URL = "https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from}&amount={amount}"


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
    parser.add_argument("date", nargs="?", type=date, const=cur_date, help="Enter the date (optional, for historical purposes)")
    return parser.parse_args()


if __name__ == "__main__":
    read_user_cli_arguments()

