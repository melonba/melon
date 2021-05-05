from flask import Flask, request, render_template, redirect, url_for, abort, sessions
import dbdb
from waitress import serve
import spo2_sensor_arduino as spo2
import json

app = Flask(__name__)


@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/loading')
def loading():
    return render_template("loading.html")

@app.route('/method', methods=['GET', 'POST'])
def method():
    if request.method == 'GET':
        username = request.form["username"]
        weight = request.form["weight"]
        height = request.form["height"]
        dbdb.create_table()
        dbdb.insert_data(username, weight, height)
        dbdb.export_csv()
        spo2.test()
        return redirect('/success')
    else:
        username = request.form["username"]
        weight = request.form["weight"]
        height = request.form["height"]
        dbdb.create_table()
        dbdb.insert_data(username, weight, height)
        dbdb.export_csv()
        spo2.test()
        return redirect('/success')


@app.route('/app/spo2')
def spo2_api():
    return render_template('spo2.json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)



