# from flask import Flask, jsonify
# from flask import request, abort

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return "<h1>Welcome to CodingX</h1>"


# @app.route('/webhook/api', methods=['POST'])
# def create_task():
#     print(request.data)
#     print(type(request.data))
#     data = request.data.decode("utf-8")

#     dic = {}
#     for i in data.split("&"):
#         if "name" in i:
#             name = i.replace("name=", "")
#             dic['name'] = name
#         elif "email" in i:
#             email = i.replace("email=", "")
#             dic['email'] = email
#         elif "phone" in i:
#             phone = i.replace("phone=", "")
#             dic['phone'] = phone

#     print(dic)

#     return jsonify(dic), 201


import json
import config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET, tld='us')


def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(
            symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(f"order placed : {order}")
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order


@app.route('/')
def index():
    return "<h1>Welcome to Trading Bot</h1>"


@app.route('/webhook/api', methods=['POST'])
def webhook():
    # print(request.data)
    data = json.loads(request.data)
    print(f"Data from Signal : {data}")

    # if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
    #     return {
    #         "code": "error",
    #         "message": "Nice try, invalid passphrase"
    #     }

    side = data['side'].upper()
    quantity = data['order_contracts']
    ticker = data['ticker'].upper()
    order_response = order(side, quantity, ticker)

    if order_response:
        print("order Success")
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
