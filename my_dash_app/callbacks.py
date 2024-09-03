import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

def register_callbacks(app, df):
    @app.callback(Output('bar-sales', 'figure'),
                  [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
    def tab1_bar_sales(start_date, end_date):
        truncated = df[(df['tran_date'] >= start_date) & (df['tran_date'] <= end_date)]
        grouped = truncated[truncated['total_amt'] > 0].groupby(
            [pd.Grouper(key='tran_date', freq='ME'), 'Store_type'])['total_amt'].sum().unstack()

        traces = []
        for col in grouped.columns:
            traces.append(go.Bar(x=grouped.index, y=grouped[col], name=col,
                                 hoverinfo='text', hovertext=[f'{y/1e3:.2f}k' for y in grouped[col].values]))

        fig = go.Figure(data=traces, layout=go.Layout(
            title='Przychody', barmode='stack', legend=dict(x=0, y=-0.5)))
        return fig

    @app.callback(Output('choropleth-sales', 'figure'),
                  [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
    def tab1_choropleth_sales(start_date, end_date):
        truncated = df[(df['tran_date'] >= start_date) & (df['tran_date'] <= end_date)]
        grouped = truncated[truncated['total_amt'] > 0].groupby('country')['total_amt'].sum().round(2)

        trace0 = go.Choropleth(colorscale='Viridis', reversescale=True,
                               locations=grouped.index, locationmode='country names',
                               z=grouped.values, colorbar=dict(title='Sales'))

        fig = go.Figure(data=[trace0], layout=go.Layout(
            title='Mapa', geo=dict(showframe=False, projection={'type': 'natural earth'})))
        return fig

    @app.callback(Output('barh-prod-subcat', 'figure'),
                  [Input('prod_dropdown', 'value')])
    def tab2_barh_prod_subcat(chosen_cat):
        grouped = df[(df['total_amt'] > 0) & (df['prod_cat'] == chosen_cat)].pivot_table(
            index='prod_subcat', columns='Gender', values='total_amt', aggfunc='sum').assign(
            _sum=lambda x: x['F'] + x['M']).sort_values(by='_sum').round(2)

        traces = []
        for col in ['F', 'M']:
            traces.append(go.Bar(x=grouped[col], y=grouped.index,
                                 orientation='h', name=col))

        fig = go.Figure(data=traces, layout=go.Layout(barmode='stack', margin={'t': 20}))
        return fig

    @app.callback(Output('sales_by_day_of_week', 'figure'),
                  [Input('channel_dropdown', 'value')])
    def update_sales_by_day_of_week(selected_channel):
        filtered_df = df[df['Store_type'] == selected_channel]
        sales_by_day = filtered_df.groupby(filtered_df['tran_date'].dt.day_name())['total_amt'].sum()
        sales_by_day = sales_by_day.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        fig = go.Figure(data=[go.Bar(x=sales_by_day.index, y=sales_by_day.values)],
                        layout=go.Layout(title=f'Sprzedaż w {selected_channel} według dnia tygodnia'))
        return fig

    @app.callback(Output('customer_info_by_channel', 'figure'),
                  [Input('channel_dropdown', 'value')])
    def update_customer_info_by_channel(selected_channel):
        filtered_df = df[df['Store_type'] == selected_channel]
        customer_info = filtered_df.groupby('Gender')['cust_id'].nunique()

        fig = go.Figure(data=[go.Pie(labels=customer_info.index, values=customer_info.values)],
                        layout=go.Layout(title=f'Struktura klientów w {selected_channel}'))
        return fig

    @app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
    def render_content(tab):
        if tab == 'tab-1':
            return render_tab1(df)
        elif tab == 'tab-2':
            return render_tab2(df)
        elif tab == 'tab-3':
            return render_tab3(df)

def render_tab1(df):
    layout = html.Div([
        html.H1('Sprzedaż globalna', style={'text-align': 'center'}),
        html.Div([
            dcc.DatePickerRange(
                id='sales-range',
                start_date=df['tran_date'].min(),
                end_date=df['tran_date'].max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '100%', 'text-align': 'center'}),
        html.Div([
            html.Div([
                dcc.Graph(id='bar-sales')
            ], style={'width': '50%'}),
            html.Div([
                dcc.Graph(id='choropleth-sales')
            ], style={'width': '50%'})
        ], style={'display': 'flex'})
    ])
    return layout

def render_tab2(df):
    grouped = df[df['total_amt'] > 0].groupby('prod_cat')['total_amt'].sum()
    fig = go.Figure(data=[go.Pie(labels=grouped.index, values=grouped.values)],
                    layout=go.Layout(title='Udział grup produktów w sprzedaży'))
    layout = html.Div([
        html.H1('Produkty', style={'text-align': 'center'}),
        html.Div([
            html.Div([dcc.Graph(id='pie-prod-cat', figure=fig)], style={'width': '50%'}),
            html.Div([
                dcc.Dropdown(id='prod_dropdown',
                             options=[{'label': cat, 'value': cat} for cat in df['prod_cat'].unique()],
                             value=df['prod_cat'].unique()[0]),
                dcc.Graph(id='barh-prod-subcat')
            ], style={'width': '50%', 'display': 'flex'})
        ])
    ])
    return layout

def render_tab3(df):
    layout = html.Div([
        html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
        
        # Dropdown do wyboru kanału sprzedaży
        html.Div([
            dcc.Dropdown(
                id='channel_dropdown',
                options=[{'label': store, 'value': store} for store in df['Store_type'].unique()],
                value=df['Store_type'].unique()[0]
            )
        ], style={'width': '50%', 'margin': 'auto'}),

        # Wykres pokazujący sprzedaż w zależności od dnia tygodnia
        html.Div([
            dcc.Graph(id='sales_by_day_of_week')
        ]),

        # Wykres pokazujący dane o klientach w zależności od kanału sprzedaży
        html.Div([
            dcc.Graph(id='customer_info_by_channel')
        ])
    ])
    return layout

