# Import packages
import requests
import re
from dash import Dash, html, dash_table
import json
import pandas as pd


catalogo_json = requests.get("http://10.90.0.83:8059/catalogo").json()
#catalogo_DF = pd.json_normalize(catalogo_json, record_prefix="Not")
catalogo_DF = pd.json_normalize(catalogo_json)
catalogo_DF.fillna(0, inplace=True)

print(catalogo_DF.columns)
columnas_espaciales = ['Name', 'EndPoint']
columnas_espaciales.extend(catalogo_DF.filter(like="spatial_ensembles", axis=1).columns.values)
columnas_individuales = ['Name',  'EndPoint']
columnas_individuales.extend(catalogo_DF.filter(like="individuals_ensembles", axis=1).columns.values)

df_espaciales = catalogo_DF[columnas_espaciales].copy()
df_espaciales = df_espaciales.loc[(df_espaciales.filter(like="spatial",axis=1)!=0).any(axis=1)]
df_individuos = catalogo_DF[columnas_individuales].copy()
df_individuos = df_individuos.loc[(df_individuos.filter(like='individuals_ensembles', axis=1)!=0).any(axis=1)]
catalogo_DF["EndPoint"] = catalogo_DF["EndPoint"].apply(lambda x:  "[Info de la fuente de datos](" + x + ")" if x != "" else "" )
# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children=html.H1("Catálogo de datos CHILAM")),
    html.Div(children=html.H1("Ensambles espaciales")),
    dash_table.DataTable(data=df_espaciales.to_dict('records'), page_size=10,
                         columns = [{'id': x, 'name': x.replace("spatial_ensembles.",""), 'presentation': 'markdown'}  for x in df_espaciales.columns]),
    html.Div(children=html.H1("Ensambles de individuos")),
    dash_table.DataTable(data=df_individuos.to_dict('records'), page_size=10,
                         columns = [{'id': x, 'name': x.replace("individuals_ensembles.",""), 'presentation': 'markdown'}  for x in df_individuos.columns])
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=9999)
