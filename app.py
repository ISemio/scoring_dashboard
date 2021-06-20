
################################# CREATE APP ##################################

import dash

APP_TITLE = 'Loan Dashboard'

# Creating app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

# Associating server
server = app.server
app.title = APP_TITLE
app.config.suppress_callback_exceptions = True