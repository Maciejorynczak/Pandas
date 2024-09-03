import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import sys
import os

from db_handler import DBHandler
from callbacks import register_callbacks

# Inicjalizacja bazy danych
db = DBHandler()
df = db.merge()

# Inicjalizacja aplikacji Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout aplikacji
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Sprzedaż globalna', value='tab-1'),
        dcc.Tab(label='Produkty', value='tab-2'),
        dcc.Tab(label='Kanały sprzedaży', value='tab-3')
    ]),
    html.Div(id='tabs-content')
])

# Rejestracja callbacków
register_callbacks(app, df)

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run_server(debug=True, port=8057)
