#!/usr/bin/env python3

from datetime import date
import requests
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from json2html import *

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def student():
    return render_template('student.html')


@app.route('/result', methods=["GET", "POST"])
def result():

    if request.method == "POST":

        first_name = request.form.get("pincode")

        Date = date.today().strftime("%d-%m-%Y")
        # api-endpoint
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"

        # location given here

        # defining a params dict for the parameters to be sent to the API
        param = {'pincode': first_name,
                 'date': Date}
        # sending get request and saving the response as response object
        r = requests.get(url=URL,  params=param, headers=headers)
        # print(r.url)
        # extracting data in json format
        data = r.json()
        lst = data['centers']
        # print(lst[2]['sessions'][0]['session_id'])
        for i in range(len(lst)):
            lst[i].pop('lat')
            lst[i].pop('long')
            for item in lst[i]['sessions']:
                item.pop('session_id')
            # lst[i]['sessions'][0].pop('session_id')
        # data = data['sessions']
        # # extracting latitude, longitude and formatted address
        # # of the first matching location
        # return '''
        #       <h2>Name is: {}</h2>
        #       <h2>Address is: {}</h2>
        #       <h2>Available_Capacity is: {}</h2>
        #       <h2>min_age_limit is:{}'''.format(data[0]["name"], data[0]["address"], data[0]["available_capacity"], data[0]["min_age_limit"])
        return json2html.convert(json=data)

    return render_template('student.html')


if __name__ == '__main__':
    app.run(debug=True)
