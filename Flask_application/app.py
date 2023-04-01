# -*- coding: utf-8 -*-
"""
Created on 2023-03-30
@author: turkalpmd
"""



from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    doctor_data = {
        'doctor_name': request.form['doctor_name'],
        'doctor_surname': request.form['doctor_surname'],
        'doctor_email': request.form['doctor_email'],
        'doctor_phone_number': request.form['doctor_phone_number']
    }
    response = requests.get("https://API_gateway_endpoint", params=doctor_data)
    if response.status_code == 200:
        var = 'Registration is succesfully'
    return render_template('index.html',var=var)

if __name__ == "__main__":
    app.run(debug=True, port=5001, host='0.0.0.0')
