import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.DataFrame(pd.read_csv("001_chest_AX6_6014664.csv"))
display_df = pd.DataFrame(pd.read_csv("test.csv"))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FAFAFA',
    'text': '#263238'
}


fig = px.scatter(df, x="time", y="posture")

fig.update_layout(
yaxis = dict(
    tickmode = 'array',
    tickvals = [0, 1, 2, 3, 4, 5],
    ticktext = ['Prone','Supine', 'Laying on Side','Sitting','Sitting/Standing', 'Dynamic']))

fig.update_layout(
    height = 450,
    xaxis_title="Time",
    yaxis_title="Posture",
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],

)
fig.update_traces(marker_color="gold", selector=dict(type='scatter'))

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], style={'marginLeft': 'auto', 'marginRight': 'auto'})

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Posture Algorithm',
        style={
            'textAlign': 'center',
            'font-size': '40px',
            'color': colors['text']
        }
    ),

    html.Div(children='Visual output of the Posture Detection algorithm developed by Arslan Salikhov, Ben Cornish, and Kyle Weber', style={
        'textAlign': 'center',
        'font-size': '25px',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig,
    ),
    html.H4(children='Posture DataFrame',
        style={
            'textAlign': 'center'
        }),
    generate_table(display_df, len(display_df))
])



app.run_server(debug=True)