from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe, user

@app.route('/')
def index():
    return render_template('index.html')
# show forms

# register to save_user

# login

# show dash

# logout