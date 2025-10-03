# Import packages
import requests
import re
from dash import Dash, html, dash_table
import json
import pandas as pd
import os



url_catalogo = os.getenv("URL_CATALOGO_SERVICE")
url_mallas = os.getenv("URL_MALLAS")
catalogo_json = requests.get(f'{url_catalogo}/catalogo').json()
catalogo_DF = pd.json_normalize(catalogo_json)
catalogo_DF.fillna(0, inplace=True)
catalogo_DF["metainfo"] = catalogo_DF.apply(lambda x: f'[{x["meta.info"]}]({x["meta.url"]})', axis=1)
catalogo_DF["EndPoint"] = catalogo_DF["EndPoint"].apply(lambda x:  f"[{x}]({x}/variables)" if x != "" else "" )
columnas_espaciales = ['name', 'description', 'metainfo','EndPoint']
columnas_espaciales.extend(catalogo_DF.filter(like="spatial_ensembles", axis=1).columns.values)
columnas_individuales = ['name',  'description', 'metainfo','EndPoint']
columnas_individuales.extend(catalogo_DF.filter(like="individuals_ensembles", axis=1).columns.values)

df_espaciales = catalogo_DF[columnas_espaciales].copy()
df_espaciales = df_espaciales.loc[(df_espaciales.filter(like="spatial",axis=1)!=0).any(axis=1)]
df_individuos = catalogo_DF[columnas_individuales].copy()
df_individuos = df_individuos.loc[(df_individuos.filter(like='individuals_ensembles', axis=1)!=0).any(axis=1)]


servicios = [{"Nombre":"Catalogo", "url":f'[{url_catalogo}]({url_catalogo}/catalogo)'},
              {"Nombre":"Ensambles espaciales", "url":f'[{url_mallas}]({url_mallas})'}]
# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children=html.H1("Catálogo de datos CHILAM")),
    html.Div(children=html.H1("Ensambles espaciales")),
    dash_table.DataTable(data=df_espaciales.to_dict('records'), page_size=10,
                         columns = [{'id': x, 'name': x.replace("spatial_ensembles.","NumVars en "), 'presentation': 'markdown'}  for x in df_espaciales.columns]),
    html.Div(children=html.H1("Ensambles de individuos")),
    dash_table.DataTable(data=df_individuos.to_dict('records'), page_size=10,
                         columns = [{'id': x, 'name': x.replace("individuals_ensembles.","Numvars en "), 'presentation': 'markdown'}  for x in df_individuos.columns]),
    html.Div(children=html.H1("Servicios")),
    dash_table.DataTable(data=servicios, columns = [{"id":"Nombre", 'name':"nombre"}, {"id":"url", 'name':"url", "presentation":"markdown"} ])
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=9999)
