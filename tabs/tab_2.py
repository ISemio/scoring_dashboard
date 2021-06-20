
################################## IMPORTS ####################################

# Import dash library and related ones
import requests
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from seaborn.rcmod import set_style
from app import app

# API URL
#URL = 'http://127.0.0.1:5000/scoring'
URL = 'https://loan-scoring-api.herokuapp.com/scoring'


################################## TAB 2 CONTENT ####################################

tab_2_ = dcc.Tab(
    label="New Application",
    value="tab_2_val",
    className='tab_name',
    children=[
        html.Div(
            className="tab_content",
            children=[
            
            html.Div([
                html.Div([
                html.H3('Please fill the data for simulation:', className='title_3'),
                ]), 

                html.Div(children=[
                            html.Div([
                            html.Label('CUSTOMER_ID'),
                            dcc.Input(id='info_1', type='number', value=12345),
                        ],className='form_content'
                        ),
                        html.Div([
                                html.Label('EXT_SOURCE_2'),
                                dcc.Input(id='info_2', type='number'),
                        ],className='form_content'
                        ),
                        html.Div([
                            html.Label('GENDER'),
                            dcc.Dropdown(
                                id='info_3',
                                options=[
                                    {'label': 'Female', 'value': 'F'},
                                {'label': 'Male', 'value': 'M'}
                                ], value='F'
                                ),
                        ],className='form_content'
                        ),
                        html.Div([
                            html.Label('GLOBAL INCOME'),
                            dcc.Input(id='info_4', type='number'),
                        ],className='form_content'
                        ),
                        
                        html.Div([
                            html.Label('CREDIT AMOUNT'),
                            dcc.Input(id='info_5', type='number'),
                        ],className='form_content'
                        ),

                        html.Div([
                            html.Label('AGE'),
                            dcc.Input(id='info_6', type='number'),
                        ],className='form_content'
                        ),

                        html.Div([
                            html.Label('DAYS REGISTRATION'),
                            dcc.Input(id='info_7', type='number'),
                        ],className='form_content'
                        ),

                        html.Div([
                            html.Label('ANNUITY AMOUNT'),
                            dcc.Input(id='info_8', type='number'),
                        ],className='form_content'
                        ),
                    ]),

                html.Div([ 
                        html.Button('Submit', id='button', n_clicks=0),
                        html.Div(id='container-button-basic',
                            children='Press to submit')
                ], className='button'),
            html.Div([
            html.Div(id='label_resultat'),
            ]),
            ]),
    ]),
])

##################################  CALLBACKS #################################

@app.callback(
    Output('app-2-display-value', 'children'),
    Input('tab_2_dropdown', 'value'))
  
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    [Output(component_id="label_resultat", component_property="children")],
    [Input(component_id="button", component_property="n_clicks")],
    [
        State(component_id="info_1", component_property="value"),
        State(component_id="info_2", component_property="value"),
        State(component_id="info_3", component_property="value"),
        State(component_id="info_4", component_property="value"),
        State(component_id="info_5", component_property="value"),
        State(component_id="info_6", component_property="value"),
        State(component_id="info_7", component_property="value"),
        State(component_id="info_8", component_property="value"),

    ],
)
def request_result(n_clicks, 
    value_info_1, 
    value_info_2, 
    value_info_3, 
    value_info_4, 
    value_info_5,
    value_info_6,
    value_info_7,
    value_info_8,
    ):

    list_values = [
    value_info_2, 
    value_info_4, 
    value_info_5,
    value_info_6,
    value_info_7,
    value_info_8,
    ]
    
    for v in list_values:
        if v is None:
            return [html.Div("Error: Fill missing data", className="error")] #classname
    
    value_info_6 = value_info_6 * 365 * (-1)
    print('value_info_6', value_info_6)
    value_info_7 = value_info_7 * (-1)
    print('value_info_7', value_info_7)

    new_json = {
        "SK_ID_CURR":value_info_1,
        "CODE_GENDER": value_info_2, 
        "EXT_SOURCE_2": value_info_3, 
        "AMT_INCOME_TOTAL":value_info_4,
        "AMT_CREDIT_x":value_info_5,
        "DAYS_BIRTH":value_info_6,
        "DAYS_REGISTRATION":value_info_7,
        "AMT_ANNUITY_x":value_info_8,
    }
    print(new_json)
    print(URL)
    rep = requests.post(url=URL, json=new_json)
    print('is_emprunt', rep)
    import json
    data = json.loads(rep.content)
    score = data['score']
    print(score)

    if score<0.30:
        return [html.Div("Loan granted", className="granted")]
    return [html.Div("Loan not granted", className="not_granted")]
