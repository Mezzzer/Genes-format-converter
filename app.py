from processing_functions import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Header(children=[
        html.H1(children='GENES FORMAT CONVERTER'),
        html.Div(children='''
            HGNC to Ensembl Gene IDs
            ''', style={'font-style': 'italic'})
        ],        
        style={
            'padding': '30px',
            'text-align': 'center',
            'background': '#1abc9c',
            'color': 'white',
            'font-size': '30px'}),

    html.Hr(),
    
    html.Center(children=[
        html.Label('Upload list of genes in HGNC format for analysis (txt files only):'),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                 'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={
                'width': '25%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            }, multiple=False),
        html.Div([html.P(id = "upload-status",
                     children=["File not uploaded"], 
                     style={'font-style': 'italic'})]),
    ]),

    html.Hr(),
    
    dcc.Tabs([
        dcc.Tab(label='Convert to Ensembl Gene IDs', children=[
            html.Br(),
            dcc.Textarea(
                id='converted-textarea',
                value='',
                style={'width': '50%', 'height': 200},
                disabled=True, draggable='false'
            ),
            html.Br(),
            html.Button('Convert', id='convert-button', n_clicks=0),
        ]),
        dcc.Tab(label='Check for repeated genes', children=[
             html.Br(),
             html.Label('Upload additional files: '),
             dcc.Upload(
                id='upload-add-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '30%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },multiple=True),
            html.Div([html.P(id = "upload-add-status",
                     children=["File not uploaded"], 
                     style={'font-style': 'italic'})]),
            html.Br(),
            html.Label('List of genes which appear in additional files: '),
            dcc.Textarea(
                id='repeated-genes-textarea',
                value='',
                style={'width': '50%', 'height': 200},
                disabled=True, draggable='false'),
            html.Br(),
            html.Button('Check', id='check-button', n_clicks=0)
        ])
    ])
])

@app.callback(Output('upload-status', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(contents, filename):
    if contents is not None:
        return upload_file_prompt(filename)
    
@app.callback(Output('upload-add-status', 'children'),
              Input('upload-add-data', 'contents'),
              State('upload-add-data', 'filename'))
def add_update_output(list_of_contents, list_of_filenames):
    if list_of_contents is not None:
        return upload_add_file_prompt(list_of_filenames)
    
@app.callback(Output('converted-textarea', 'value'),
              Input('convert-button', 'n_clicks'),
              State('upload-data', 'contents'),
              State('upload-data', 'filename'))
def convert_file(n_clicks, contents, filename):
    if contents is not None and '.txt' in filename:
        return "\n".join(parse_file(contents))
    
@app.callback(Output('repeated-genes-textarea', 'value'),
              Input('check-button', 'n_clicks'),
              State('upload-add-data', 'contents'),
              State('upload-add-data', 'filename'),
              State('upload-data', 'contents'),
              State('upload-data', 'filename'))
def additional_upload(n_clicks, list_of_contents, list_of_names, contents, filename):
    if contents is not None and '.txt' in filename:
        parsed_file = parse_file(contents)
        if list_of_contents is not None:
            parsed_files = list()
            for c, f in zip(list_of_contents, list_of_names):
                if '.txt' in filename:
                    parsed_files.append(parse_file(c))
        if parsed_files is not None:
            return "\n".join(find_repeated(parsed_file, parsed_files))

app.title = 'Genes format converter'
app.run_server(port = 8090, debug=False)