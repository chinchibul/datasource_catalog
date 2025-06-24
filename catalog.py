from flask import Flask
from flask import Response
import requests
import pandas as pd
import json
import itertools

url_spatial_ensembles = 'http://chilamdev.c3.unam.mx:5001/regions/region-grids/'

def get_spatial_ensembles_names(url):
    '''
    obtenemos una lista de los ensambles registrados en el servicio de ensambles espaciales (regions/grids).
    esto debería considerar el part footprint_region:resolution
    a manera de ejemplo, por ahora solo usamos 'resolution'.
    '''    
    ensembles_dict = requests.get(url).json()
    ensembles_DF = pd.json_normalize(ensembles_dict, record_path='data')
    return ensembles_DF["resolution"].unique() # como hay varias regiones, las 'resolution' están repetidas.


def get_spatial_ensembles_from_source(url, spatial_ensembles):
    '''
    a partir de la fuente (url) obtenemos la lista de 'ensambles espaciales' en las que la fuente proporciona 
    variables.
    '''
    if url:
        variables = pd.read_json(url  + '/variables')
        ensembles = {ensemble:variables["available_grids"].apply(lambda x: ensemble in x).sum() for ensemble in spatial_ensembles}
        return ensembles
    return {}

def get_individuals_ensembles_from_source(url, spatial_ensembles):
    '''
    a partir de la fuente (url) obtenemos la lista de 'ensambles de individuos'
    en los que la fuente proporciona variables. (cualquier ensamble que no está en la lista 'oficial' de ensambles  espaciales)
    '''
    if url:
        variables = pd.read_json(url  + '/variables')
        not_spatial_ensembles = variables["available_grids"].apply(lambda x: list(set(x) - set(spatial_ensembles)))
        not_spatials = set(itertools.chain.from_iterable(not_spatial_ensembles.values))
        individuals_ensembles = { ensemble:variables["available_grids"].apply(lambda x: ensemble in x).sum() for ensemble in not_spatials}
        return individuals_ensembles
    return {}


def get_df_catalogo():
    '''
    crea un DF con el catálogo 'oficial'. Para pruebas, este último es ahora un .csv local
    pero en un futuro puede ser una BD o un objeto en MINIO.
    '''
    catalogo = pd.read_csv("catalogo.csv")
    catalogo.fillna("", inplace=True) #read_csv llena con NaNs los vacios. con esto, los regresamos a vacios.
    return catalogo

spatial_ensembles = get_spatial_ensembles_names(url_spatial_ensembles)
catalogo = get_df_catalogo()


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello!</p>"


@app.route("/catalogo")
def dsources_api():
    catalogo["spatial_ensembles"] = catalogo["EndPoint"].apply(get_spatial_ensembles_from_source,
                                                               spatial_ensembles=spatial_ensembles)
    catalogo["individuals_ensembles"] = catalogo["EndPoint"].apply(get_individuals_ensembles_from_source,
                                                                   spatial_ensembles=spatial_ensembles) 
    return Response(response=catalogo.to_json(orient="records"), status=200, mimetype="application/json")


if __name__ == "__main__":
        app.run_server(debug=True, port=8051, host='0.0.0.0')
