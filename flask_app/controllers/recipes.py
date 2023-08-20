from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe

@app.route('/')
def home():
    return render_template('index.html')

# create recipe
# edit recipe
# delete recipe
# show one recipe
# show all recipes