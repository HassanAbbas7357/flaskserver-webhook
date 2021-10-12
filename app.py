import json
import config
from flask import Flask, request
from binance.client import Client
from binance.enums import *

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Welcome to BOT</h1>"


client = Client(config.API_KEY, config.API_SECRET)


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


@app.route('/webhook/api', methods=['POST'])
def create_task():
    # print(request.data)
    data = json.loads(request.data)
    print(f"Data from Signal : {data}")

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
