
################################## IMPORTS ####################################

# Import dash library and related ones
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from logzero import logger as lg

# Import use case tabs
from app import app, APP_TITLE
from tabs.tab_1 import tab_1_
from tabs.tab_2 import tab_2_
from app import server

# Creating stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

################################## MAIN APP ###################################

app.layout = html.Div(
    children=[
        # HEADER
        html.Div([

        html.Div([
            html.Img(
                    src = app.get_asset_url('logo.png'),
                    height = '50 px',
                    width = 'auto')
                ],
                className = 'header_3',
                style = {
                        'align-items': 'center',
                        'padding-top' : '1%',
                        'height' : 'auto'}
                ),
        html.Div([
            html.H1(children='Loan Dashboard',
                        style = {'textAlign' : 'center'}
                )],
                className='header_2',
                
                ),
        html.Div([
            ], className = 'header_1'), #Same as img width, allowing to have the title centrally aligned

    ], className = 'header'),
    
        # CONTENT and TABS
        html.Div(
            className="tabs__container",
            children=[
            
                dcc.Tabs(
                    id="tabs",
                    value="tab_1_val",
                    children=[
                        tab_1_,
                        tab_2_,
                    ],
                ),
            ],
        ),
    ],
)



#################################### RUN ######################################

if __name__ == '__main__':

    # Display app start
    lg.error("*" * 80)
    lg.error("Initialisation")
    lg.error("*" * 80)

    # Run application
    app.run_server(debug=True)
