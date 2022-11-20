# currency.py

import argparse
from configparser import ConfigParser
from datetime import date
import requests
from prettytable import PrettyTable

BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def _get_key():
    configuration = ConfigParser()
    configuration.read("secrets.ini")
    return configuration["APILayer"]["api_key"]


def read_user_cli_arguments():
    cur_date = date.today()
    parser = argparse.ArgumentParser(description="Converts amount from one currency into another")
    parser.add_argument("date", nargs="?",type=str, default=cur_date.strftime("%Y-%m-%d"), help="Enter the date (optional, for historical purposes)")
    parser.add_argument("from", nargs="+", type=str, help="Enter the three letter currency code you want to convert from")
    parser.add_argument("to", nargs="+", type=str, help="Enter the three letter currency code you want to convert to")
    parser.add_argument("amount", nargs="+", type=float, help="Enter the amount of money")
    return parser.parse_args()  #To access the dictionary variant, use vars()


def convert(cur_from, cur_to, cur_amount, ent_date):
    apikey = _get_key()
    headers = { "apikey" : apikey}
    parameters = {"to": str(cur_to), "from": str(cur_from), "amount": str(cur_amount), "date": str(ent_date)}
    response = requests.get(url = BASE_URL, params = parameters, headers = headers)
    if response.status_code == 200:
        return response.json()
    else:
        print ("Oops,something went wrong! [Status code:", response.status_code, "\b]")
        return None


def more_values(cur_from, ent_date):
    answer = []
    apikey = _get_key()
    headers = { "apikey" : apikey}
    currency_lst = ["INR", "USD", "EUR", "JPY", "GBP", "AUD", "CAD"]
    for x in range (0, len(currency_lst), 1):
        parameters = {"to": str(currency_lst[x]), "from": str(cur_from), "amount": '1', "date": str(ent_date)}
        response = requests.get(url = BASE_URL, params = parameters, headers = headers)
        if response.status_code == 200:
            answer.append(response.json()["result"])
        else:
            continue
    return answer

    
if __name__ == "__main__":  
    result = read_user_cli_arguments()
    dictionary = vars(result)
    ans_set = convert(dictionary["from"][0], dictionary["to"][0], dictionary["amount"][0], dictionary["date"])
    if ans_set is not None:
        print ("\n\b\b\b\b\b", dictionary["amount"][0], dictionary["from"][0], "is equal to", ans_set["result"], dictionary["to"][0], "as of", dictionary["date"])
        print ("Exchange rate: 1", dictionary["from"][0], "=", ans_set["info"]["rate"], dictionary["to"][0], "\n")
        answer = more_values(dictionary["from"][0], dictionary["date"])
        mytable = PrettyTable(["Given Currency", "INR", "USD", "EUR", "JPY", "GBP", "AUD", "CAD"])
        mytable.add_row(["1 "+dictionary["from"][0], answer[0], answer[1], answer[2], answer[3], answer[4], answer[5], answer[6]])
        print ("Exchange rates against some currencies around the world (as of", dictionary["date"], "\b): ")
        print (mytable)