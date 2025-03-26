from flask import Flask
import pandas as pd
import json

catalogo = pd.read_csv("catalogo.csv")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello!</p>"


@app.route("/me")
def me_api():
    return {
        "db": "INEGI",
        "fuente": "inegi",
        "url" : "https://chilam.c3.unam.mx/inegi-db"
    }


@app.route("/datasources")
def dsources_api():
    return json.loads(catalogo.to_json(orient="records"))

if __name__ == "__main__":
        app.run_server(debug=True, port=8051, host='0.0.0.0')
