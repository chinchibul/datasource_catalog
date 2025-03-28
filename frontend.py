# Import packages
import requests
import re
from dash import Dash, html, dash_table
import json
import pandas as pd


catalogo_json = requests.get("http://127.0.0.1:5000/catalogo").json()
catalogo_DF = pd.json_normalize(catalogo_json, record_prefix="Not")
catalogo_DF.columns = [ re.sub("Mallas\.","", col) for  col in catalogo_DF.columns]
catalogo_DF["EndPoint"] = catalogo_DF["EndPoint"].apply(lambda x:  "[Info de la fuente de datos](" + x + ")" if x != "" else "" )
catalogo_DF["Variables"] = catalogo_DF["Variables"].apply(lambda x:  "[Lista de variables](" + x + ")" if x != "" else "" )
# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children=html.H1("Catálogo de datos CHILAM")),
    dash_table.DataTable(data=catalogo_DF.to_dict('records'), page_size=10,
                         columns = [{'id': x, 'name': x, 'presentation': 'markdown'}  for x in catalogo_DF.columns])
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
