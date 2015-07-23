from flask import render_template, request, flash, redirect, url_for
from wall import app, db, models


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index_view():
    return render_template('index.html',
                           title="Dashboard")
