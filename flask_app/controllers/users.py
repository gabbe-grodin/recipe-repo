from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User


# shows forms
@app.route('/')
def index():
    return render_template('index.html')

# register to create_user
@app.route('/create/user/submission', methods=['POST'])
def sign_up_new_user():
    if User.create_user(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/')

# login
@app.route('/login/user/submission', methods=['POST'])
def login():
    if User.login_user(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/')

# table of all users and their recipes
@app.route('/dashboard')
def show_all_users_with_recipes():
    if 'user_id' in session:
        logged_in_user = User.get_one_user_by_id(session['user_id'])
        # all_users_with_recipes = User.get_all_users_with_recipes()
        # print(all_users_with_recipes)
        # return render_template("dash.html", all_users = all_users_with_recipes, logged_in_user = logged_in_user)

        return render_template("dash.html", logged_in_user = logged_in_user)

    else:
        return redirect("/")


# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')