from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User



# LOGIN & REGISTRATION FORMS
@app.route('/')
def index():
    if 'user_id' in session:
        session.clear()
        return render_template('index.html')
    else:
        return render_template('index.html')

# CREATE USER
@app.route('/create/user/submission', methods=['POST'])
def sign_up_new_user():
    if User.create_user(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/')

# LOGIN POST
@app.route('/login/user/submission', methods=['POST'])
def login():
    if User.login_user(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/')

# READ ALL
@app.route('/all/users')
def show_all_users_with_recipes():
    if 'user_id' in session:
        logged_in_user = User.get_one_user_by_id(session['user_id'])
        return render_template("dash.html", logged_in_user = logged_in_user)
    else:
        return redirect("/")


# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')