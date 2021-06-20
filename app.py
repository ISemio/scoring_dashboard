
################################# CREATE APP ##################################

import dash
from whitenoise import WhiteNoise

APP_TITLE = 'Loan Dashboard'

# Creating app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

# Associating server
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='src/')

app.title = APP_TITLE
app.config.suppress_callback_exceptions = True
