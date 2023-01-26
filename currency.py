# currency.py

import argparse
from configparser import ConfigParser
from datetime import date, datetime, timedelta
import requests
from prettytable import PrettyTable

BASE_URL = "https://api.apilayer.com/exchangerates_data/"


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
    headers = { "apikey": apikey}
    parameters = {"to": str(cur_to), "from": str(cur_from), "amount": str(cur_amount), "date": str(ent_date)}
    response = requests.get(url = BASE_URL + "convert", params = parameters, headers = headers)
    if response.status_code == 200:
        return response.json()
    else:
        print ("Oops,something went wrong! [Status code:", response.status_code, "\b]")
        return None


def more_values(cur_from, ent_date):
    answer = []
    apikey = _get_key()
    headers = {"apikey": apikey}
    currency_lst = ["INR", "USD", "EUR", "JPY", "GBP", "AUD", "CAD"]
    for x in range (0, len(currency_lst), 1):
        parameters = {"to": str(currency_lst[x]), "from": str(cur_from), "amount": '1', "date": str(ent_date)}
        response = requests.get(url = BASE_URL + "convert", params = parameters, headers = headers)
        if response.status_code == 200:
            answer.append(response.json()["result"])
        else:
            continue
    if len(answer) > 0:
        return answer
    else:
        print ("Oops,something went wrong! [Status code:", response.status_code, "\b]")
        return None


def real_time_rates(reference):
    answer = []
    apikey = _get_key()
    headers = {"apikey": apikey}
    parameters = {"base": reference}
    response = requests.get(url = BASE_URL + "latest", params = parameters, headers = headers)
    if response.status_code == 200:
        answer.append(response.json()["rates"])
        return answer
    else:
        print ("Oops,something went wrong! [Status code:", response.status_code, "\b]")
        return None


def dated_exchange_rates(req_date):
    answer = []
    apikey = _get_key()
    headers = {"apikey": apikey}
    parameters = {"base": "USD", "date": datetime.strptime(req_date, '%-%m-%d').date()}
    # print (str((datetime.strptime(req_date, '%Y-%m-%d').date()).strftime("%Y-%m-%d")), type(str((datetime.strptime(req_date, '%Y-%m-%d').date()).strftime("%Y-%m-%d"))))
    response = requests.get(url = BASE_URL + "{{date}}", params = parameters, headers = headers)
    if response.status_code == 200:
        answer.append(response.json()["rates"])
        return answer
    else:
        print ("Oops,something went wrong! [Status code:", response.status_code, "\b]")
        return None


def timeseries(start, end, base, limits = "USD"):
    answer = []
    apikey = _get_key()
    headers = {"apikey": apikey}
    parameters = {"start_date": start, "end_date": end, "base": base, "symbols": "USD"}
    response = requests.get(url = BASE_URL + "timeseries", params = parameters, headers = headers)
    if response.status_code == 200:
        answer.append(response.json()["rates"])
        return answer
    else:
        print ("Oops,something went wrong! [Status code:", response.status_code, "\b]")
        return None



if __name__ == "__main__":  
    result = read_user_cli_arguments()
    dictionary = vars(result)
    ans_set = convert(dictionary["from"][0], dictionary["to"][0], dictionary["amount"][0], dictionary["date"])
    if ans_set is not None:
        print ("\n\b\b\b\b\b", dictionary["amount"][0], dictionary["from"][0], "is equal to", ans_set["result"], dictionary["to"][0], "as of", dictionary["date"])
        print ("Exchange rate: 1", dictionary["from"][0], "=", ans_set["info"]["rate"], dictionary["to"][0], "\n")

        print ("Please choose among the following options:")
        print ("(1) Compare the currency", dictionary["from"][0], "with other popular currencies at", dictionary["date"])
        print ("(2) Show real time exchange rate of", dictionary["from"][0], "against several popular currencies")
        print ("(3) To show the exchange rate of popular currencies against the USD on a particular date")
        print ("(4) Show the value of", dictionary["from"][0], "against the USD for 5 or 30 days from the current date")
        print ("(5) To exit")
        checker = True

        while checker:
            choice = int(input("Enter a choice: "))

            if choice == 1:
                checker1 = True
                answer = more_values(dictionary["from"][0], dictionary["date"])
                mytable = PrettyTable(["Given Currency", "INR", "USD", "EUR", "JPY", "GBP", "AUD", "CAD"])
                mytable.add_row(["1 "+dictionary["from"][0], answer[0], answer[1], answer[2], answer[3], answer[4], answer[5], answer[6]])
                print ("Exchange rates against some currencies around the world (as of", dictionary["date"], "\b): ")
                print (mytable)

                while checker1:
                    choice1 = str(input("Go again? (Y/N)?: "))
                    if choice1.lower() == "y":
                        checker = True
                        break
                    elif choice1.lower() == "n":
                        checker = False
                        checker1 = False
                        break
                    else:
                        print ("Please enter a valid answer!")

            if choice == 2:
                checker2 = True
                answer = real_time_rates(dictionary["from"][0])
                popular_currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "INR"]
                keys = list(answer[0].keys())
                values = list(answer[0].values())
                mytable = PrettyTable(["Currency", "1 INR Equivalent"])
                for x in range(0, len(keys), 1):
                    if keys[x] in popular_currencies:
                        mytable.add_row([keys[x], values[x]])
                print ("Latest exchange rates are as tabulated below")
                print (mytable)

                while checker2:
                    choice2 = str(input("Go again? (Y/N)?: "))
                    if choice2.lower() == "y":
                        checker = True
                        break
                    elif choice2.lower() == "n":
                        checker = False
                        checker2 = False
                        break
                    else:
                        print ("Please enter a valid answer!")

            if choice == 3:
                checker3 = True
                req_date = str(input("Enter the desired date in YYYY-MM-DD format: "))
                answer = dated_exchange_rates(req_date)
                print (answer)

                while checker3:
                    choice3 = str(input("Go again? (Y/N)?: "))
                    if choice3.lower() == "y":
                        checker = True
                        break
                    elif choice3.lower() == "n":
                        checker = False
                        checker3 = False
                        break
                    else:
                        print ("Please enter a valid answer!")
            
            if choice == 4:
                checker4 = True
                checker44 = True
                cur_date = datetime.now()
                print ("(1) To show the value of", dictionary["from"][0], "against USD 5 days from", cur_date)
                print ("(2) To show the value of", dictionary["from"][0], "against USD 30 days from", cur_date)
                while checker44:
                    choice4 = int(input("Enter a choice: "))
                    if choice4 == 1:
                        delta = 5
                        end_date = cur_date - timedelta(days = delta)
                        answer =  timeseries(end_date.strftime("%Y-%m-%d"), cur_date.strftime("%Y-%m-%d"), base = dictionary["from"][0], limits = "USD")
                        timeseries_table = PrettyTable(["Date", "1 INR in USD"])
                        answer_keys = list(answer[0].keys())
                        answer_values = list(answer[0].values())
                        for x in range(0, len(answer_keys), 1):
                            timeseries_table.add_row([answer_keys[x], answer_values[x]])
                        print ("Timeseries is as tabulated below: ")
                        print (timeseries_table)
                    elif choice4 == 2:
                        delta = 30
                        end_date = cur_date - timedelta(days = delta)
                        answer =  timeseries(end_date.strftime("%Y-%m-%d"), cur_date.strftime("%Y-%m-%d"), base = dictionary["from"][0], limits = "USD")
                        timeseries_table = PrettyTable(["Date", "1 INR in USD"])
                        answer_keys = list(answer[0].keys())
                        answer_values = list(answer[0].values())
                        for x in range(0, len(answer_keys), 1):
                            timeseries_table.add_row([answer_keys[x]['USD'], answer_values[x]['USD']])
                        print ("Timeseries is as tabulated below: ")
                        print (timeseries_table)
                    else:
                        print ("Please enter a valid choice")
                pass

            if choice == 5:
                checker = False
                break
        
            elif choice not in [1,2,3,4,5]:
                print ("Invalid input, enter again")

