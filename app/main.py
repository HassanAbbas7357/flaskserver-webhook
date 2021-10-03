from flask import Flask, jsonify
from flask import request, abort

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1>Welcome to CodingX</h1>"


@app.route('/webhook/api', methods=['POST'])
def create_task():
    print(request.data)
    print(type(request.data))
    data = request.data.decode("utf-8")

    dic = {}
    for i in data.split("&"):
        if "name" in i:
            name = i.replace("name=", "")
            dic['name'] = name
        elif "email" in i:
            email = i.replace("email=", "")
            dic['email'] = email
        elif "phone" in i:
            phone = i.replace("phone=", "")
            dic['phone'] = phone

    print(dic)

    return jsonify(dic), 201
