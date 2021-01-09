'''
LAYOUTS FOR DASH
'''
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq




# AUTHENTICATION LAYOUTS
create = html.Div([ 
    html.Div([
        html.H1('Create User Account'), 
        dcc.Location(id='create_user', refresh=True), 
        dbc.Input(id="username", type="text", placeholder="user name", maxLength =15), 
        dbc.Input(id="password", type="password", placeholder="password"), 
        dbc.Input(id="email", type="email", placeholder="email", maxLength = 50),
        dbc.Button('Create User', id='submit-val', n_clicks=0, color="primary", className="mr-1"),
    ], style={
        'backgroundColor': 'grey',
        'border-radius': '10px',
        'color': 'white',
        'padding': '30px'
    }),
    html.Div(
        id='container-button-basic',
        style={
            'backgroundColor': 'lightgrey',
            'border-radius': '10px',
            'color': 'white',
            'padding': '30px'
        })
    ], style={
        'backgroundColor': 'green',
        'border-radius': '10px',
        'color': 'white',
        'padding': '30px'
})

login =  html.Div([
    dcc.Location(id='url_login', refresh=True), 
    html.H2('''Please log in to continue:''', id='h1'),
    dbc.Input(placeholder='username', type='text', id='uname-box'),
    dbc.Input(placeholder='password', type='password', id='pwd-box'), 
    dbc.Button(children='Login', n_clicks=0, type='submit', id='login-button', color='primary'),
    html.Div(children='', id='output-state')
    ], style={
        'backgroundColor': 'grey',
        'border-radius': '10px',
        'color': 'white',
        'padding': '10px'
})

logout = html.Div([
    dcc.Location(id='logout', refresh=True),
    html.Br(),
    html.Div(html.H2('You have been logged out - Please login')),
    html.Br(),
    html.Div([login])
    ], style={
        'backgroundColor': 'green',
        'border-radius': '10px',
        'color': 'white',
        'padding': '30px'
})



## CONTENT PAGES
navbar = dbc.Navbar(
    children=[
        html.Span(
            dbc.Row([
                    dbc.Col(dbc.NavbarBrand("Summer 2021 - Shopify Developer Intern Challenge", className="ml-2")),
                ],
                align="center",
                no_gutters=True,               
            ),         
        ),
        dbc.Nav([
                dbc.NavLink("HOME", href="main"),
                dbc.NavLink("ADD", href="add"),
                dbc.NavLink("SEARCH", href="search"),
                dbc.NavLink("LOGOUT", href="logout"),
            ],
            pills=True,
            className="ml-auto"
        ) 
    ],
    color="lightgrey",
    dark=False,
    sticky="top",
    style={
        'border': '2px solid green',
        'outline': 'green',
        'border-radius': '10px',
        'color':'white',
    }
)

success = html.Div([
    navbar,
    html.Div([
        html.H1(children='Image Repo', style={'padding': '0px 10px' }),
        html.Br(),
        html.H2(id='show-output', children='e'),
        
        html.Div("  By Amardeep Singh"),
    ], style={
        'backgroundColor': 'green',
        'border-radius': '10px',
        'color': 'white',
        'padding': '30px'
    }),
    html.Div(id='page-main-content'),
])

add_page = html.Div([
    navbar,
    html.Div([
        html.H1(children='Add Your Images', style={'padding': '0px 10px' }),
        
    ], style={
        'backgroundColor': 'green',
        'border-radius': '10px',
        'color': 'white',
        'padding': '30px'
    }),
    html.Div([
        dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Click to Select Files')
        ]),
        style={
            'width': '95%',
            'height': '450px',
            'lineHeight': '450px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
        
    ], style={
        'width': '30%',
        'height': '500px',
        'backgroundColor': 'grey',
        'border-radius': '10px',
        'color': 'white',
        'padding': '0px',
        'float':'left'
    }),
    html.Div([
        daq.BooleanSwitch(
            id='my-boolean-switch',
            on=False,
            color="#9B51E0",
        ),
        html.Div(id='boolean-switch-output')
    ], style={
        'width': '70%',
        # 'border': '2px solid green',
        'height': '500px',
        'backgroundColor': 'lightgrey',
        'border-radius': '10px',
        'color': 'darkgrey',
        'padding': '0px',
        'float':'right'
    }),
    html.Div([
        
    html.Div(id='output-image-upload'),
        
    ], style={
        'height': '500px',
        'backgroundColor': 'lightgrey',
        'border-radius': '10px',
        'color': 'darkgrey',
        'padding': '0px',
    }),

    html.Div("by Amardeep Singh", style={'float': 'right'}),
    html.Div(id='page-1-content')
])

search = html.Div([
    navbar,
    html.Div([
        html.H1(children='More Coming Soon', style={'padding': '0px 10px' }),
        
    ], style={
        'backgroundColor': 'green',
        'border-radius': '10px',
        'color': 'white',
        'padding': '30px'
    }),
    html.Div("by Amardeep Singh", style={'float': 'right'}),
    html.Div(id='page-2-content')
])