from _csv import writer

import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    keys = request.form.keys()
    print(keys)

    if keys.__contains__('name'):
        name = request.form['name']
    else:
        return render_template("error.html", message="Required field Plant Name is empty! Check and try again!")
    latin_name = "Not provided"
    if keys.__contains__('latin_name'):
        latin_name = request.form['latin_name']
    if keys.__contains__('region'):
        region = request.form['region']
    else:
        return render_template("error.html", message="Required field REgion is empty! Check and try again!")
    if keys.__contains__('plant_type'):
        plant_type = request.form['plant_type']
    else:
        return render_template("error.html", message="Required field Plant Type is empty! Check and try again!")
    if keys.__contains__('latitude'):
        latitude = request.form['latitude']
    else:
        return render_template("error.html", message="Required field Latitude is empty! Check and try again!")
    if keys.__contains__('longitude'):
        longitude = request.form['longitude']
    else:
        return render_template("error.html", message="Required field Longitude is empty! Check and try again!")
    if keys.__contains__('id_researcher'):
        id_researcher = request.form['id_researcher']
    else:
        return render_template("error.html", message="Required field Researcher's id is empty! Check and try again!")
    if keys.__contains__('agree'):
        agree = request.form['agree']
    else:
        return render_template("error.html", message="Required checkbox is empty! Check and try again!")
    with open('survey.csv', 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow([name, latin_name, region, plant_type, latitude, longitude, id_researcher, agree])
        f_object.close()
    return redirect("/sheet")

@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open('survey.csv') as csvfile:
        lines = [line.split('\t') for line in csvfile]
        result = ''
        for line in lines:
            str = '<tr>'
            for lin in line:
                data = lin.split(',')
                data.pop()
                for value in data:
                    str += '<td>{}</td>'.format(value)
                str += '</tr>'
                result += str
    return render_template("sheet.html", data_var=[result])
