from flask import Flask
from flask import Response
import requests
import pandas as pd
import json




def completa(fuente):
    url = fuente["EndPoint"]
    if url:
        variables = pd.read_json(url  + '/variables')
        datos = { res:variables["available_grids"].apply(lambda x: res in x).sum() for res in resolutions}
        return datos
    return {}
        
regions_dict = requests.get('http://chilamdev.c3.unam.mx:5001/regions/region-grids/').json()
regions_DF = pd.json_normalize(regions_dict, record_path='data')
resolutions = regions_DF["resolution"].unique()

catalogo = pd.read_csv("catalogo.csv")
catalogo.fillna("", inplace=True)

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


@app.route("/catalogo")
def dsources_api():
    mallas = catalogo.apply(completa, axis=1)
    catalogo["Mallas"] = mallas
    catalogo["Variables"] = catalogo.apply(lambda x: x["EndPoint"] + "variables" if x["EndPoint"] != "" else "", axis=1)
    return Response(response=catalogo.to_json(orient="records"), status=200, mimetype="application/json")


if __name__ == "__main__":
        app.run_server(debug=True, port=8051, host='0.0.0.0')

