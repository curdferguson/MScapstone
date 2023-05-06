from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

cicc_scatter = pd.read_csv('data/analysis/exploratory/cicc_scatter.csv')

def safe_log(col):
    try:
        return np.log10(col)
    except:
        None
    
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.RadioItems(
            ['natural', 'cube_root', 'log'],
            'natural',
            inline=True,
            id='dist'
            ),
        dcc.Checklist(
            options=[{'label': 'cicc_scatter', 'value': 0}, {'label': 'cicc_scatterai', 'value': 1}],
            value=[0, 1],
            inline=True,
            id='data'
        )]),
    html.Div([
        dcc.Slider(50, 300, 50,
        value=50,              
        id='bins'
        ),
        dcc.Dropdown(
            cicc_scatter.columns,
            'net_pop_chg_domestic_indivs',    
            id='col'
        )]),
    html.Div([
        html.Div([dcc.Graph(id='graphic1')], style={"display": "inline-block", "width": "50%"}),
        html.Div([dcc.Graph(id='graphic2')], style={"display": "inline-block", "width": "50%"})
    ])
])

@app.callback(
    Output('graphic1', 'figure'),
    Input('data', 'value'),
    Input('dist', 'value'),
    Input('col', 'value'),
    Input('bins', 'value')
)    
def update_fig1(data, dist, col, bins):
    df = cicc_scatter[cicc_scatter['ai_activity_class'].isin(data)]
    dist_lookup = {'natural': df[col], 'cube_root': df[col]**(1/3), 'log': safe_log(df[col])}

    fig = px.histogram(data_frame = dist_lookup[dist], x = col, nbins=bins)
    fig.update_layout(title=f'{col}')
    fig.update_layout(transition_duration=500)
    #fig.update_xaxes(type="log")

    return fig

@app.callback(
    Output('graphic2', 'figure'),
    Input('data', 'value'),
    Input('dist', 'value'),
    Input('col', 'value')
)    
def update_fig2(data, dist, col):
    df = cicc_scatter[cicc_scatter['ai_activity_class'].isin(data)]
    dist_lookup = {'natural': df[col], 'cube_root': df[col]**(1/3), 'log': safe_log(df[col])}

    fig = px.scatter(cicc_scatter, 
            y="net_pop_chg_domestic_indivs",
            x=dist_lookup[dist],
            trendline="ols",
            trendline_color_override="red",
            title=f'{col}'
            )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)