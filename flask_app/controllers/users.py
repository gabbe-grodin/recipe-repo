from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
from flask_app.models.user import User



# LOGIN & REGISTRATION FORMS

@app.route('/')
def index():
    if 'user_id' in session: # doing this so if i go back a page in my browser i get logged out and cant loggin as a new user while still in session
        session.clear()
        # return render_template('index.html')
        return redirect('/logout')
    else:
        return render_template('index.html')




# CREATE USER FORM

@app.route('/user/new', methods=['POST'])
def sign_up_new_user(): #format requires mapping error happens here
    # pass in data dict instead
    User.create_user(request.form) 
    return redirect('/dashboard')




# LOGIN POST

@app.route('/login', methods=['POST'])
def login():
    if User.login_user(request.form):
        return redirect('/dashboard')
    else:
        return redirect('/')




# LOGOUT

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')




# READ ALL

# @app.route('/all/users')
# def show_all_users_with_recipes():
#     if 'user_id' in session:
#         logged_in_user = User.get_one_user_by_id(session['user_id'])
#         return render_template("dash.html", logged_in_user = logged_in_user)
#     else:
#         return redirect("/")

