
################################## IMPORTS ####################################

# Import dash library and related ones
from dash_html_components import Data
from matplotlib.pyplot import xlabel, ylabel
import pandas as pd
import numpy as np
import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from app import app
from logzero import logger as lg


# Loading external data
#path = r"C:\Users\IS\Documents\Data Scientist\P7\P7_semionov_irina\P7_02_dossier\dashboard\src" +'\\'
path = 'src/'
DATA_PATH = path +'data_processed.csv'
lg.debug(DATA_PATH)
df = pd.read_csv(DATA_PATH)
df = df.fillna(0)

# FEATURES_PATH = path +'features_importances.sav'
# features_importances = pickle.load(open(FEATURES_PATH, 'rb'))
# features = features_importances[["feature", "importance"]].groupby(
#         "feature").mean().sort_values(by="importance", ascending=False)[:10].index.to_list()


################################## FUNCTIONS ####################################

def spacify_number(number):
    """ Takes a number and returns a string with spaces every 3 numbers
    """
    nb_rev = str(number)[::-1]
    new_chain = ''
    for val, letter in enumerate(nb_rev):
        if val%3==0:
            new_chain += ' '
        new_chain += letter
    final_chain = new_chain[::-1][:-1]
    return final_chain


################################## TAB 1 CONTENT ####################################

tab_1_ = dcc.Tab(
    label="Ongoing applications",
    value="tab_1_val",
    className='tab_name',
    children=[
        html.Div(
            className="tab_content",
            children=[
            html.Div(children=[
        
            html.Div([


                # Info box
                html.Div(children=[
                    html.Div(children=[
                    html.Label(children='', className='title_2'),
                    ]),
                    html.Div(children=[
                        html.Label(children='Loan Granted:', className='title_2'),
                        html.P(children='Loan Granted', id='Loan_granted'),
                    html.Div(children=[
                    html.Label(children='', className='title_2'),
                    ]),
                    html.Div(children=[    
                        html.Label(children='Customer score:', className='title_2'),
                        dcc.Graph(
                            id='score_gauge',
                        )
                    ]),
                    ], className='info_box_1'),

                    html.Div([
                        html.Label('Customer ID', className='title_2'),
                        dcc.Dropdown(
                        id='customer_id',
                        options=[{'label': i, 'value': i} for i in df['SK_ID_CURR']],
                        value=223232)
                    ], className='info_box_1', 
                    )
                ], className='info_box'),


                # Customer info
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label('Main information', className='title_4'),
                        ], className='title_4'
                        ),
                        html.Div(id='cust_info', children=[
                            html.Div([
                                html.Label('Age:'),
                                html.P(children='Age', id='Age'), 
                                html.Label('Gender:'),
                                html.P(children='Gender', id='Gender'),
                                html.Label('Income:'),
                                html.P(children='Income', id='Income'),
                            ], className='cust_info_1_1'),
                            html.Div([
                                html.Label('Family status:'),
                                html.P(children='Family_status', id='Family_status'),
                                html.Label('Children:'),
                                html.P(children='Children', id='Children'),
                                html.Label('Credit:'),
                                html.P(children='Credit', id='Credit'),

                            ], className='cust_info_1_1'),
                        ], className='cust_info_1',
                        ),
                    ], className='main_info'
                    ),

                    html.Div([
                        html.Div([
                        html.Label('TOP 3 Features', className='title_4'),
                    ],className='title_4'
                    ),
                        html.Div([
                        dcc.Graph(
                            id='top3_features',
                            )   
                        ], className='cust_info_2',
                        )
                    ], className='main_info'
                    ),
                ], className='cust_info'),

            ], className='customer_filter'),


            # Features distribution
            html.Div([
                html.Div([
                html.Label('TOP 3 Features Distribution', className='title_2'),
                ], className='feat_title'),
                html.Div([
                    html.Div([
                        dcc.Graph(id="feat_distplot_1", ),
                    ], className='feat_distr_1'),
                    html.Div([
                        dcc.Graph(id="feat_distplot_2"),
                    ], className='feat_distr_1'),
                    html.Div([
                        dcc.Graph(id="feat_distplot_3"),
                    ], className='feat_distr_1'),
                ], className='feat_content'),
            ], className='feat_distr'),

        ]),
    ]),
])


##################################  CALLBACKS #################################

@app.callback(
    Output('Loan_granted', 'children'),    
    [Input('customer_id', 'value')])
    
def update_status(customer_id):
    print('customer_id', customer_id)
    dff = df[df['SK_ID_CURR'] == customer_id]
    print(dff.shape)
    status = np.where(dff['TARGET'].iloc[0]==0, 'YES', 'NO')
    print('status',status)
    
    if status=='YES':
        return [html.Div("YES", className="granted")]
    return [html.Div("NO", className="not_granted")]


@app.callback(
    Output('score_gauge', 'figure'),
    [Input('customer_id', 'value')])

def update_gauge(customer_id):
    print('customer_id', customer_id)
    dff = df[df['SK_ID_CURR'] == customer_id]
    print(dff.shape)
    value = dff['PREDICTION'].iloc[0]
    print('value', value)
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = dff['PREDICTION'].iloc[0],
        mode = "gauge+number",
        #title = {'text': "Customer Score"},
        #delta = {'reference': 0.15},
        gauge = {'bar': {'color': "mediumpurple"},
        'axis': {'range': [0, 1]},
             'steps' : [
                 {'range': [0, 0.15], 'color': "darkgreen"},
                 {'range': [0.15, 0.30], 'color': "aquamarine"},
                 {'range': [0.30, 0.50], 'color': "coral"},
                 {'range': [0.50, 1], 'color': "crimson"},                
             ],
          }))
    fig.update_layout(
        #autosize=False,
        width=200,
        height=150,
        margin=dict(
            l=30,
            r=30,
            b=0,
            t=0,
            pad=0
        ),
    )
    return fig


@app.callback(
    [
    Output('Age', 'children'),
    Output('Gender', 'children'),
    Output('Family_status', 'children'),
    Output('Children', 'children'),
    Output('Income', 'children'),
    Output('Credit', 'children'),
    ], 
    [Input('customer_id', 'value')])

def update_text(customer_id):
    dff = df[df['SK_ID_CURR'] == customer_id]
    print('text', dff.shape)
    values = []
    columns_c = ['Age', 'Gender', 'Family_status']
    for c in columns_c:
            values.append(dff[c].iloc[0])
    columns = ['CNT_CHILDREN', 'AMT_INCOME_TOTAL', 'AMT_CREDIT_x']
    for c in columns:
            values.append(spacify_number(round(dff[c].iloc[0])))
    print('value_ch', values)
    return values 


@app.callback(
    Output('top3_features', 'figure'),
    [Input('customer_id', 'value')])

def update_barh(customer_id):
    print('customer_id', customer_id)
    df['AGE'] = df['Age']
    dff = df[df['SK_ID_CURR'] == customer_id]
    features = ['EXT_SOURCE_2',  'AGE', 'DAYS REGISTRATION']
    colors = ['lightsteelblue',] * 3
    colors[1] = 'mediumorchid'
    colors[2] = 'slateblue'
    x=[dff[features[0]].iloc[0]*100]
    x.append(dff[features[1]].iloc[0])
    x.append(dff[features[2]].iloc[0]/df[features[1]].max()*100)
    fig = go.Figure(go.Bar(
                y=features,
                x=x,
                width=[0.5, 0.5, 0.5], # customize width here
                marker_color=colors,
                orientation='h'),
                )
    fig.update_layout(
        autosize=True,
        #width=500,
        height=250,
        margin=dict(
            l=20,
            #r=30,
            b=10,
            t=0,
            pad=0
        ),
    )
    return fig


@app.callback(
    Output("feat_distplot_1", "figure"), 
    [Input('customer_id', 'value'),
        ]
    )
    
def update_distplot_1(customer_id):
    feat = 'EXT_SOURCE_2'
    x1 = df[df['TARGET']==0][feat]
    x2 = df[df['TARGET']==1][feat]
    marker = df[df['SK_ID_CURR'] == customer_id][feat].iloc[0]
    print('marker', marker)
    print('x1', x1.shape)
    print('x2', x2.shape)
    hist_data = [x1, x2]
    group_labels = ['Loan granted', 'Loan not granted']
    colors = ['#A56CC1', '#A6ACEC']
    
    fig = ff.create_distplot(
        hist_data, group_labels, 
        colors=colors,
        bin_size=.01
        )
    fig.add_scatter(x=[marker], mode="markers",
                marker=dict(size=10, color="LightSeaGreen"),
                name="Customer position",
                )
    fig.update_layout(
    height=320,
    xaxis_title=feat, 
    yaxis_title="Density", 
    showlegend=False,
    font=dict(
        size=10,
        color="RebeccaPurple"
    ),
    margin=dict(
            l=60,
            r=30,
            b=10,
            t=25,
            pad=0
        ),
    )
    return fig


@app.callback(
    Output("feat_distplot_3", "figure"), 
    [Input('customer_id', 'value'),
        ]
    )
    
def update_distplot_3(customer_id):
    feat = 'DAYS REGISTRATION'
    x1 = df[df['TARGET']==0][feat]
    x2 = df[df['TARGET']==1][feat]
    marker = df[df['SK_ID_CURR'] == customer_id][feat].iloc[0]
    print('marker', marker)
    print('x1', x1.shape)
    print('x2', x2.shape)
    hist_data = [x1, x2]
    group_labels = ['Loan granted', 'Loan not granted']
    colors = ['#A56CC1', '#A6ACEC']
    
    fig = ff.create_distplot(
        hist_data, group_labels, colors=colors,
        bin_size=100
        )
    fig.add_scatter(x=[marker], mode="markers",
                marker=dict(size=10, color="LightSeaGreen"),
                name="Customer position")
    fig.update_layout(
    height=320,
    width=650,
    xaxis_title='DAYS REGISTRATION',
    yaxis_title="Density",
    legend=dict(
    orientation="v",
    yanchor="top",
    y=1,
    xanchor="right",
    x=1.50
),
    font=dict(
        size=10,
        color="RebeccaPurple"
    ),
    margin=dict(
            l=30,
            r=30,
            b=10,
            t=25,
            pad=0
        ),
    )
    return fig

@app.callback(
    Output("feat_distplot_2", "figure"), 
    [Input('customer_id', 'value'),
        ]
    )
    
    
def update_distplot_2(customer_id):
    feat = 'Age'
    print(feat)
    x1 = df[df['TARGET']==0][feat]
    x2 = df[df['TARGET']==1][feat]
    marker = df[df['SK_ID_CURR'] == customer_id][feat].iloc[0]
    print('marker', marker)
    print('x1', x1.shape)
    print('x2', x2.shape)
    hist_data = [x1, x2]
    group_labels = ['Loan granted', 'Loan not granted']
    colors = ['#A56CC1', '#A6ACEC']
    
    fig = ff.create_distplot(
        hist_data, group_labels, colors=colors,
        bin_size=1
        )
    fig.add_scatter(x=[marker], mode="markers",
                marker=dict(size=10, color="LightSeaGreen"),
                name="Customer position")
    fig.update_layout(
    height=320,
    xaxis_title='AGE',
    yaxis_title="Density",
    showlegend=False,
    font=dict(
        size=10,
        color="RebeccaPurple"
    ),
    margin=dict(
            l=30,
            r=60,
            b=10,
            t=25,
            pad=0
        ),
    )
    return fig
