from flask_app.config.mysqlconnection import connectToMySQL
from flask import session, flash
from flask_app.models import user
from flask_app import app


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

    @classmethod
    def create_recipe(cls, form_data):
        recipe_data = {
                "recipe_name": form_data["recipe_name"],
                "recipe_description": form_data["recipe_description"],
                "recipe_instructions": form_data["recipe_instructions"],
                "recipe_date": form_data["recipe_date"],
                "under_30": form_data["under_30"],
                "user_id": session["user_id"]
            }
        query = """
        INSERT INTO recipes (recipe_name, recipe_description, recipe_instructions, recipe_date, under_30, user_id)
        VALUES (%(recipe_name)s, %(recipe_description)s, %(recipe_instructions)s, %(recipe_date)s, %(under_30)s, %(user_id)s)
        """
        result = connectToMySQL(cls.db).query_db(query, recipe_data)
        print("Create recipe method in model", result)
        return result
    
    # get_one

    # get_all