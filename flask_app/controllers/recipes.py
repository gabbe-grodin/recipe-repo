from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/')
def home():
    return render_template('index.html')

# create recipe "/add/recipe/form"
@app.route('/add/recipe/form')
def add_recipe_form():
    data = {"id": session["user_id"]}
    # is this the validation this needs?...
    if 'user_id' in session:
        User.get_one_user_by_id(data)
        return render_template('add_recipe.html')
    else:
        return redirect('/')

# create recipe "/add/recipe/submission"
@app.route('/add/recipe/submission', methods=['POST'])
def add_recipe():
    # needs validations like if user in session etc?
    Recipe.create_recipe(request.form)
    return redirect('/dashboard')

# show one recipe
@app.route("/view/recipe/<int:id>")
def show_one_recipe(id):
    data = {"id": id}
    one_recipe = Recipe.get_one_recipe_by_id(data)
    if one_recipe:
        return render_template('view_recipe.html', recipe = one_recipe)
    else:
        return redirect('dashboard')
    
# edit recipe
@app.route("/edit/recipe/form")
def edit_recipe_form():
    pass

# update recipe 
@app.route("/update/recipe/submission", methods=['POST'])
def update_recipe_submit():
    pass
    return redirect("/view/recipe/<int:id>")

# delete recipe "/delete/recipe"


# show all recipes