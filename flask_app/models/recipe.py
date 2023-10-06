from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
from flask_app.models import user
from flask_app import app
import pprint
from datetime import datetime

class Recipe:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.recipe_description = data['recipe_description']
        self.recipe_instructions = data['recipe_instructions']
        self.recipe_date = data['recipe_date']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['recipe_name']) <= 0:
            flash("Cannot leave 'Name' field empty.")
            is_valid = False
        if len(recipe['recipe_description']) <= 0:
            flash("Cannot leave 'Description' field empty.")
            is_valid = False
        if len(recipe['recipe_instructions']) <= 0:
            flash("Cannot leave 'Instructions' field empty.")
            is_valid = False
        if not (recipe['recipe_date']):
            flash("Must add the date you created this recipe.")
            is_valid = False
        return is_valid
    
    
    
    @classmethod
    def create_recipe(cls, form_data):
        print(form_data)
        recipe_data = {
            "recipe_name": form_data["recipe_name"],
            "recipe_description": form_data["recipe_description"],
            "recipe_instructions": form_data["recipe_instructions"],
            "recipe_date": form_data["recipe_date"],
            "under_30": form_data["under_30"],
            "user_id": session["user_id"]} # because reference to the user is made here, a hidden input is not necessary in submit form. 
        query = """INSERT INTO recipes (recipe_name, recipe_description, recipe_instructions, recipe_date, under_30, user_id)
            VALUES (%(recipe_name)s, %(recipe_description)s, %(recipe_instructions)s, %(recipe_date)s, %(under_30)s, %(user_id)s)"""
        result = connectToMySQL(cls.db).query_db(query, recipe_data)
        print("Create recipe method in model", result)
        return result
    
    @classmethod
    def get_one_recipe_by_id_with_creator(cls, data):
        query = """SELECT * FROM recipes
            LEFT JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s"""
        result=connectToMySQL(cls.db).query_db(query, data)
        print("Result: ")
        pprint.pp(result)
        one_recipe = cls(result[0])
        # instance of recipe class and creator...
        for row in result:
            recipe_creator_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]}
        one_recipe.creator = user.User(recipe_creator_data)
        if one_recipe:
            return one_recipe
        else:
            return False

    @classmethod
    def get_all_recipes_with_creators(cls):
        query="""SELECT * FROM recipes
            LEFT JOIN users
            ON recipes.user_id = users.id"""
        results=connectToMySQL(cls.db).query_db(query)
        recipe_creator_list = []
        # instances of recipe class and creator...
        for row in results:
            one_recipe = cls(row)
            #
            creator_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]}
            one_recipe.creator = user.User(creator_data)
            recipe_creator_list.append(one_recipe)
        return recipe_creator_list
    









    # UPDATE
    @classmethod
    def update_one_recipe_by_id_with_user(cls, data):
        recipe_data = {
                "id": data["id"],
                "recipe_name": data["recipe_name"],
                "recipe_description": data["recipe_description"],
                "recipe_instructions": data["recipe_instructions"],
                "recipe_date": data["recipe_date"],
                "under_30": data["under_30"],
                "user_id": session["user_id"]}
        query = """
        UPDATE recipes
        SET id=%(id)s, recipe_name=%(recipe_name)s, recipe_description=%(recipe_description)s, recipe_instructions=%(recipe_instructions)s, recipe_date=%(recipe_date)s, under_30=%(under_30)s, updated_at=NOW()
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.db).query_db(query, recipe_data)





    # DELETE
    @classmethod
    def delete_one_recipe_by_id(cls, data):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.db).query_db(query, data)
    

    # https://www.programiz.com/python-programming/datetime/strftime
    
    @classmethod
    def format_date(cls,date_time,output_fmt):
        tmp_date_time = datetime.strptime(date_time,"%Y-%m-%d %H:%M:%S")
        output_format = output_fmt
        date_time_output = tmp_date_time.strftime(output_format)
        return date_time_output