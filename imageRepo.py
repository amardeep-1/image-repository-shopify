#Dash imports
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

#SQL/Flask imports
import sqlite3
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
from flask import request

import configparser
import warnings
import datetime
import base64
import os

from layouts import add_page, search, create, login, success, logout


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])



warnings.filterwarnings("ignore")
conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()
config = configparser.ConfigParser()


# followed tutorial from gitconnected for user login
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def get_username(self):
        return self.username

Users_tbl = Table('users', Users.metadata)
server = app.server
app.config.suppress_callback_exceptions = True
# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(server)
# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'
# Create User class with UserMixin
class Users(UserMixin, Users):
    pass

#sets page content based on path
app.layout= html.Div([
    html.Div(id='page-content', className='content')
    ,  dcc.Location(id='url', refresh=False)
])

# funtions to return images
def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.Img(src=contents,style={'width': '70%'}),
        html.Hr(),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

def parse_contents_search(filename,user):
    return html.Div([
        html.H5(filename + " by: " + user),
        html.Img(
            src=app.get_asset_url(os.path.join('public_images\\'+user+'\\',filename)),
            style = {
                'width': '30%',
                'padding-top': 10,
                'padding-right': 10
            }
        )
    ])
def parse_contents_search_p(filename,user):
    return html.Div([
        html.H5(filename + " by: " + user),
        html.Img(
            src=app.get_asset_url(os.path.join('user_images\\'+user+'\\',filename)),
            style = {
                'width': '30%',
                'padding-top': 10,
                'padding-right': 10
            }
        )
    ])

#funtions for saving images
def save_file_public(name, content, user):
    if not os.path.exists(os.path.join('assets\\public_images\\', user)):
        os.mkdir(os.path.join('assets\\public_images\\', user))
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join('assets\\public_images\\'+user+'\\', name), "wb") as fp:
        fp.write(base64.decodebytes(data))
def save_file_private(name, content, user):
    if not os.path.exists(os.path.join('assets\\user_images\\', user)):
        os.mkdir(os.path.join('assets\\user_images\\', user))
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join('assets\\user_images\\'+user+'\\', name), "wb") as fp:
        fp.write(base64.decodebytes(data))


'''
CALBACKS
'''

# USER ID CALLBACK
@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))

# PAGE CONTENT CALLBACK
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return create
    elif pathname == '/login':
        return login
    elif pathname == '/success':
        if current_user.is_authenticated:
            return success
        else:
            return create
    elif pathname =='/main': 
        if current_user.is_authenticated:
            return success
    elif pathname =='/add':
        if current_user.is_authenticated:
            return add_page
    elif pathname =='/search':
        if current_user.is_authenticated:
            return search
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout
        else:
            return logout
    else:
        return '404'


# LOGIN PAGES CALLBACKS
@app.callback(
    [Output('container-button-basic', "children")],
    [Input('submit-val', 'n_clicks')],
    [State('username', 'value'), 
    State('password', 'value'), 
    State('email', 'value')])
def insert_users(n_clicks, un, pw, em):
    hashed_password = generate_password_hash(pw, method='sha256')
    if un is not None and pw is not None and em is not None:
        ins = Users_tbl.insert().values(username=un,  password=hashed_password, email=em,)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
        return [login]
    else:
        return [html.Div([html.H2('Already have an account?'), dcc.Link('Click here to Log In', href='/login')])]

@app.callback(
    Output('url_login', 'pathname'),
    [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'), 
    State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = Users.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/success'
        else:
            pass
    else:
        pass

@app.callback(
    Output('output-state', 'children'), 
    [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'), 
    State('pwd-box', 'value')])
def update_output_b(n_clicks, input1, input2):
    if n_clicks > 0:
        user = Users.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''

@app.callback(
    Output('url_login_success', 'pathname'),
    [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'

@app.callback(
    Output('url_login_df', 'pathname'),
    [Input('back-button', 'n_clicks')])
def logout_dashboard_k(n_clicks):
    if n_clicks > 0:
        return '/'

# Create callbacks
@app.callback(
    Output('url_logout', 'pathname'),
    [Input('back-button', 'n_clicks')])
def logout_dashboard_i(n_clicks):
    if n_clicks > 0:
        return '/'



# ADD PAGE CALLBACKS
@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents'),
              Input('my-boolean-switch', 'on')],
              [State('upload-image', 'filename'),
              State('upload-image', 'last_modified')])
def update_output_a(list_of_contents, on, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)
        ]

        if on:
            for name, data in zip(list_of_names, list_of_contents):
                user = current_user.get_username()
                save_file_private(name, data, user) 
        else:
            for name, data in zip(list_of_names, list_of_contents):
                user = current_user.get_username()
                save_file_public(name, data, user)
            
        return children

@app.callback(
    dash.dependencies.Output('boolean-switch-output', 'children'),
    [dash.dependencies.Input('my-boolean-switch', 'on')])
def update_output(on):
    if on:
        return 'Your image will be private'
    else:
        return 'Your image will be public'
    return''


@app.callback(Output('output-image-upload-search', 'children'),
              [Input('search-button', 'n_clicks'),  #need to change button function
              Input("search-input", "value"),
              Input('dropdown', 'value')])
def update_search(click, searchValue, filterName):
    children = []    
    if click is None:
        allPublicUsers = os.listdir('assets\\public_images\\')
        for user in allPublicUsers:
            allPublicImages = os.listdir(os.path.join('assets\\public_images\\', user))
            for image in allPublicImages:
                children.append(parse_contents_search(image,user))
            
        return children
    else:
        if filterName=='names':
            allPublicUsers = os.listdir('assets\\public_images\\')
            for user in allPublicUsers:
                allPublicImages = os.listdir(os.path.join('assets\\public_images\\', user))
                for image in allPublicImages:
                    if searchValue in image:
                        children.append(parse_contents_search(image,user))
                
        elif filterName=='users':
            allPublicUsers = os.listdir('assets\\public_images\\')
            for user in allPublicUsers:
                if searchValue in user:
                    allPublicImages = os.listdir(os.path.join('assets\\public_images\\', user))
                    for image in allPublicImages:
                        children.append(parse_contents_search(image,user))
                
        elif filterName=='privateUser':
            if not os.path.exists(os.path.join('assets\\user_images\\', current_user.get_username())):
                allPublicImages = os.listdir(os.path.join('assets\\public_images\\', current_user.get_username()))
                for image in allPublicImages:
                    children.append(parse_contents_search(image,current_user.get_username()))
            else:
                allPrivateImages = os.listdir(os.path.join('assets\\user_images\\', current_user.get_username()))
                for image in allPrivateImages:
                    children.append(parse_contents_search_p(image,current_user.get_username()))
        elif filterName=='colours':
            return 'I am working on this filter'

    return children

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.server.run(debug=True, port=8050, host='127.0.0.1')

#127.0.0.1 for local machine 
#0.0.0.0 for AWS machine 
