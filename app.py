from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import requests


app = Flask(__name__)

correct_username = "admin"
correct_password = "admin123"

logfile = "login_attempts.log"


def get_location(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        city = data.get("city", "Unknown")
        country = data.get("country", "Unknown")
    except Exception:
        city = "Unknown"
        country = "Unknown"
    return city, country

def log_attempt(username, success, ip_address, city="Unknown", country="Unknown"):
    with open(logfile, "a", encoding="utf-8") as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "SUCCESSFUL" if success else "UNSUCCESSFUL"
        f.write(f"[{time}] User: {username}, Status: {status}, IP: {ip_address}, City: {city}, Country: {country}\n")

@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    ip_address = request.remote_addr

    city, country = get_location(ip_address)

    if username == correct_username and password == correct_password:
        log_attempt(username, True, ip_address, city, country)
        return redirect(url_for("success"))
    else:
        log_attempt(username, False, ip_address, city, country)
        return render_template("login.html", message="Incorrect username or password")

@app.route("/success")
def success():
    return "<h1>Sucessful log-in, Welcome</h1>"

if __name__ == "__main__":
    app.run(debug=True)

#Run server on localhost: http://127.0.0.1:5000/