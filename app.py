from processing_functions import *
from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc

external_stylesheets=[dbc.themes.BOOTSTRAP]

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
        dbc.Row(
            [              
                dbc.Col(children=[
                    html.Label('Provide list of genes in HGNC format for analysis...'),
                    html.Br(),
                    dcc.Textarea(
                        id='insert-textarea',
                        value='',
                        style={'width': '80%', 'height': 200},
                        disabled=False, draggable='false'
                    )

                ]),
                dbc.Col(children=[
                    html.Label('...or upload it here (txt files only):'),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                             'Drag and Drop or ',
                            html.A('Select File')
                        ]),
                        style={
                            'width': '50%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        }, multiple=False
                    )
                ])
            ]),
        
    ]),

    html.Hr(),
    
    dcc.Tabs([
        dcc.Tab(label='Convert to Ensembl Gene IDs', children=[
            html.Center(children=[
                html.Br(),
                dcc.Textarea(
                    id='converted-textarea',
                    value='',
                    style={'width': '50%', 'height': 200},
                    disabled=True, draggable='false'
                ),
                html.Br(),
                dbc.Button('Convert', color="success", id='convert-button', n_clicks=0, outline=True),
                ])
        ]),
        dcc.Tab(label='Check for repeated genes', children=[
            html.Br(),
            html.Center(children=[
            dbc.Row([              
                    dbc.Col(children=[
                        html.Label('Provide additional list...'),
                        html.Br(),
                        dcc.Textarea(
                            id='insert-add-textarea',
                            value='',
                            style={'width': '80%', 'height': 200},
                            disabled=False, draggable='false'
                        )

                    ]),
                    dbc.Col(children=[
                        html.Label('...or upload it here:'),
                        dcc.Upload(
                            id='upload-add-data',
                            children=html.Div([
                                 'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '50%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px'
                            }, multiple=True
                        )
                ])
            ]),
        ]),
        html.Br(),
        html.Center(children=[
            html.Label('List of genes which appear in additional files: '),
            html.Br(),
            dbc.Row([
                dbc.Col(children=[
                    html.Label('Ensembl IDs'),
                    html.Br(),
                    dcc.Textarea(
                        id='repeated-genes-textarea',
                        value='',
                        style={'width': '80%', 'height': 200},
                        disabled=True, draggable='false')
                        ]),
                dbc.Col(children=[
                    html.Label('HGNC name (GRCh37)'),
                    html.Br(),
                     dcc.Textarea(
                        id='repeated-names-textarea',
                        value='',
                        style={'width': '80%', 'height': 200},
                        disabled=True, draggable='false')
                ])
            ]),
            html.Br(),
            dbc.Button('Check', color="success", id='check-button', n_clicks=0, outline=True)
            ])
        ])
    ],colors={
        "border": "white",
        "primary": "#1abc9c",
        "background": "#E0E0E0"}
    ),
    
    html.Br(),

    html.Footer(children=[
        html.H5(children='for MNM Diagnostics'),
        html.Div(children='''
            by Maciej Meler
            ''', style={'font-style': 'italic'})
        ],        
        style={
            'padding': '10px',
            'text-align': 'right',
            'background': '#1abc9c',
            'color': 'white',
            'font-size': '12px'}),

    #erro dialogs        
    dcc.ConfirmDialog(
        id='only-txt',
        message='You can upload only txt file!',
    ),
    dcc.ConfirmDialog(
        id='only-txts',
        message='You can upload only txt files!',
    ),
    dcc.ConfirmDialog(
        id='not-valid-gene',
        message='You have to provide a valid genes list of genes. \nCheck if all names are in GRCh37 or GRCh38 format and seperated in new lines.',
    ),
    dcc.ConfirmDialog(
        id='not-valid-genes',
        message='You have to provide a valid genes list of genes. \nCheck if all names are in GRCh37 or GRCh38 format and seperated in new lines.',
    ),
])
    
@app.callback(
    [
        Output('insert-textarea', 'value'),
        Output('only-txt', 'displayed')
    ],
    [
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    ])
def upload_file(contents, filename):
    if contents is not None:
        if '.txt' in filename:
            return "\n".join(parse_file(contents)), False
        else:
            return None, True
    return None, False
    
@app.callback(
    [
        Output('converted-textarea', 'value'),
        Output('not-valid-gene', 'displayed')
    ],
    [
        Input('convert-button', 'n_clicks'),
        State('insert-textarea', 'value')
    ])
def convert_file(n_clicks, value):
    if value is not None:
        try:
            return "\n".join(process_list(value.split())), False
        except:
            return None, True
    return None, False

@app.callback(
    [
        Output('insert-add-textarea', 'value'),
        Output('only-txts', 'displayed')
    ],
    [
        Input('upload-add-data', 'contents'),
        State('upload-add-data', 'filename')
    ])
def additional_upload(list_of_contents, list_of_names):
    if list_of_contents is not None:
        parsed_files = list()
        for c, f in zip(list_of_contents, list_of_names):
            if '.txt' in f:
                parsed_files = parsed_files + parse_file(c)
            else:
                return None, True
        return "\n".join(parsed_files), False
    return None, False
    
@app.callback(
    [
        Output('repeated-genes-textarea', 'value'),
        Output('repeated-names-textarea', 'value'),
        Output('not-valid-genes', 'displayed')
    ],
    [
        Input('check-button', 'n_clicks'),
        State('insert-textarea', 'value'),
        State('insert-add-textarea', 'value')
    ])
def additional_check(n_clicks, genes1, genes2):
    if genes1 is not None and genes2 is not None:
        try:
            processed_genes1 = process_list(genes1.split())
            processed_genes2 = process_list(genes2.split())
            ensembls = find_repeated(processed_genes1, processed_genes2)
            names = ensembl_list_to_GRCh37(ensembls)
            return "\n".join(ensembls), "\n".join(names), False
        except:
            return None, None, True
    return None, None, False

app.title = 'Genes format converter'
app.run_server(port = 8090, debug=False)