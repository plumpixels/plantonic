from flask import Flask, request, render_template, jsonify
from gspread import service_account

acc = service_account()
sh = acc.open("Plantonic-Sensor-Data")
wk = sh.worksheet('temp-hum')

app = Flask(__name__)


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


if (__name__ == "__main__"):
    app.run(debug=True)
