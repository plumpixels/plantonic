import os
import json
from flask import Flask, request, render_template, jsonify
from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
creds_dict = json.loads(json_creds)
creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)

acc = authorize(creds)
sh = acc.open("Plantonic-Sensor-Data")
wk = sh.worksheet('temp-hum')


@app.route("/")
def home():
    return '<h1>Nothing here, go to <a href="/data">data</a>'


@app.route("/data", methods=["POST", "GET"])
def post():
    if (request.method == "GET"):
        data = wk.get("A2:C100")
        return render_template("data.html", data=data)
    data = request.get_json()
    print(data)
    reading = [data.get("time"), data.get("temperature"), data.get("humidity")]
    print(reading)
    if None in reading:
        return jsonify({"error": "Wrong format", "reading": data})
    wk.append_row(reading)
    return jsonify({"status": "successful"})
