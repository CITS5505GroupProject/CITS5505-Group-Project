from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Tony', 'DoB':'10/12/2001'}
    return render_template('index.html', title = 'Home Page', user = user)