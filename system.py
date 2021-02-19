from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'MYSQL_HOST'
app.config['MYSQL_USER'] = 'MYSQL_USER'
app.config['MYSQL_PASSWORD'] = 'MYSQL_PASSWORD'
app.config['MYSQL_DB'] = 'MYSQL_DB'

conn = MySQL (app)

@app.route("/country", methods = ["GET"])
def country():
    Data = []
    status = True
    status_code = 200

    try:
        cur = conn.connection.cursor()
        cur.execute("select country, zip from zip_code")
        for country in cur.fetchall():
            Data.append({"country": country[0], "zip_code": country[1]})
        cur.close()

    except Exception as e:
        print(e.args)
        status = False
        status_code = 500

    return jsonify({"Countries": Data, "Status": status}), status_code


@app.route("/country/<string:name>", methods = ["GET"])
def view(name):
    Data = []
    name = re.sub('[^A-Za-z ]', '', name)
    status = True
    status_code = 200

    try:
        cur = conn.connection.cursor()
        cur.execute(f"select country, zip from zip_code where country = '{name}'")
        for country in cur.fetchall():
            Data.append({"country": country[0], "zip_code": country[1]})

        if not Data:
            status = False
            status_code = 404

        cur.close()

    except Exception as e:
        print(e.args)
        status = False
        status_code = 500

    return jsonify({"Countries": Data, "Status": status}), status_code


@app.route("/country", methods = ["POST"])
def add():
    if not request.json or not "country" in request.json or not "zip_code" in request.json:
        return jsonify({"Status": False}), 400

    status = True
    status_code = 201

    country_name = re.sub('[^A-Za-z ]', '', request.json["country"])
    country_zip_code = int(request.json["zip_code"])

    try:

        cur = conn.connection.cursor()
        cur.execute(f"insert into zip_code(country, zip) values('{country_name}', {country_zip_code})")
        cur.close()
        conn.connection.commit()

    except Exception as e:
        print(e.args)
        status = False
        status_code = 500

    return jsonify({"Status": status}), status_code


@app.route("/country/<string:name>/<int:zip_code>", methods = ["PUT"])
def edit(name, zip_code):
    country_name = re.sub('[^A-Za-z ]', '', name)
    country_zip_code = int(zip_code)
    status = True
    status_code = 200
    
    try:
        cur = conn.connection.cursor()
        cur.execute(f"update zip_code set zip = {country_zip_code} where country = '{country_name}'")
        cur.close()
        conn.connection.commit()

    except Exception as e:
        print(e.args)
        status = False
        status_code = 500

    return jsonify({"Status": status}), status_code


@app.route("/country/<string:name>", methods = ["DELETE"])
def delete(name):
    country_name = re.sub('[^A-Za-z ]', '', name)
    status = True
    status_code = 200

    try:
        cur = conn.connection.cursor()
        cur.execute(f"DELETE FROM zip_code where country = '{country_name}'")
        cur.close()
        conn.connection.commit()

    except Exception as e:
        print(e.args)
        status = False
        status_code = 500

    return jsonify({"Status": status}), status_code


if __name__ == "__main__":
    app.run(debug=True)
