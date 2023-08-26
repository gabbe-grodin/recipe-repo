from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template, redirect, request, session, flash
from flask_app.models import recipe
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
import re

class User:
    db = 'recipes'
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.recipes=[]

    @classmethod
    def create_user(cls,data):
        if not cls.user_validations(data):
            return False
        parsed_data = cls.parse_user_data(data)
        print("---------------------------line 26", parsed_data)
        query="""
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
            """
        print("--------------------- line 31")
        user_id = connectToMySQL(cls.db).query_db(query, parsed_data)
        print(user_id, "line 33 -------------------------")
        session['user_id'] = user_id
        print("line 35 ------------------")
        session['full_name'] = f"{parsed_data['first_name']} {parsed_data['last_name']}"
        print("line 37 ---------------")
        return True

    @classmethod
    def get_one_user_by_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s
        """
        result=connectToMySQL(cls.db).query_db(query, data)
        if result:
            one_user = cls(result[0])
            return one_user
        else:
            return False
        
    @staticmethod
    def user_validations(form_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        if len(form_data['first_name']) > 0 and len(form_data['first_name']) <= 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(form_data['first_name']) <= 0:
            flash("Cannot leave first name field blank. ")
            is_valid = False
        if len(form_data['last_name']) > 0 and len(form_data['last_name']) <= 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False
        if len(form_data['last_name']) <= 0:
            flash("Cannot leave last name field blank.")
        if not EMAIL_REGEX.match(form_data['email']) and len(form_data['email']) > 0:
            flash("Email must be in correct format.")
            is_valid = False
        if len(form_data['email']) <= 0:
            flash("Cannot leave email field blank.")
            is_valid = False
        if User.get_one_user_by_email(form_data['email']):
            flash("Email is already in our system. Please try again.")
            is_valid = False
        if len(form_data['password']) > 0 and len(form_data['password']) <= 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        if len(form_data['password']) <= 0:
            flash("Cannot leave password field blank.")
        return is_valid
    
    @staticmethod
    def parse_user_data(form_data):
        parsed_data = {}
        parsed_data['first_name'] = form_data['first_name']
        parsed_data['last_name'] = form_data['last_name']
        parsed_data['email'] = form_data['email']
        parsed_data['password'] = bcrypt.generate_password_hash(form_data['password'])
        return parsed_data
    
    @staticmethod
    def login_user(data):
        this_user = User.get_one_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['full_name'] = f"{this_user.first_name} {this_user.last_name}"
                return True
            else:
                flash("Your login failed.") # keep vague for security
                return False
        else:
            flash("Your login failed.")
            return False

    @classmethod
    def get_one_user_by_email(cls, email):
        data = {"email": email}
        query = """
        SELECT * FROM users
        WHERE email = %(email)s
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            one_user = cls(result[0])
            print("User not gettable.")
            return one_user
        else:
            print("User email not found.")
            return False

    # @classmethod
    # def get_all_users(cls):
    #     query = """
    #     SELECT * FROM users
    #     """
    #     results=connectToMySQL(cls.db).query_db(query)
    #     all_users = []
    #     for each_user in results:
    #         all_users.append(cls[each_user])
    #     return all_users

    # @classmethod
    # def update_user_by_id(cls,data):
    #     query="""
    #     UPDATE users
    #     SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s
    #     WHERE id=%(id)s
    #     """
    #     result=connectToMySQL(cls.db).query_db(query,data)
    #     return result
    
    # @classmethod
    # def delete_user_by_id(cls,data):
    #     query="""
    #     DELETE FROM users
    #     WHERE id = %(id)s
    #     """
    #     result=connectToMySQL(cls.db).query_db(query,data)
    #     return result
    
    # @classmethod
    # def get_one_user_with_recipes(cls,data):
    #     query="""
    #     SELECT * FROM users
    #     LEFT JOIN recipes
    #     ON user_id=users.id
    #     WHERE users.id = %(id)s
    #     """
    #     result=connectToMySQL(cls.db).query_db(query,data)
    #     user = cls(result[0])
    #     for row_from_db in result:
    #         recipe_data = {
    #             "id": row_from_db["recipes.id"],
    #             "recipe_name": row_from_db["recipe_name"],
    #             "recipe_description": row_from_db["recipe_description"],
    #             "recipe_instructions": row_from_db["recipe_instructions"],
    #             "recipe_date": row_from_db["recipe_date"],
    #             "under_30": row_from_db["under_30"],
    #             "created_at": row_from_db["recipes.created_at"],
    #             "updated_at": row_from_db["recipes.updated_at"],
    #             "user_id": row_from_db["user_id"]
    #         }
    #         user.recipes.append(recipe.Recipe[recipe_data])
    #     return user

    # @classmethod
    # def get_all_users_with_recipes(cls):
    #     query="""
    #     SELECT * FROM users
    #     LEFT JOIN recipes
    #     ON user_id=users.id
    #     """
    #     results=connectToMySQL(cls.db).query_db(query)
    #     all_users_with_recipes = []
    #     for row in results:
    #         #new_user=True
    #         one_recipe_info = {
    #             "id": row["recipes.id"],
    #             "recipe_name": row["recipe_name"],
    #             "recipe_description": row["recipe_description"],
    #             "recipe_instructions": row["recipe_instructions"],
    #             "recipe_date": row["recipe_date"],
    #             "under_30": row["under_30"],
    #             "created_at": row["recipes.created_at"],
    #             "updated_at": row["recipes.updated_at"],
    #             "user_id": row["user_id"]
    #         }

    #         if (len[all_users_with_recipes] == 0) or (row['id'] != all_users_with_recipes[len[all_users_with_recipes]-1].id):
    #             one_user_instance = cls(row)
    #             print("one user instance", one_user_instance)
    #             if one_recipe_info['id'] != None:
    #                 one_recipe_instance = recipe.Recipe(one_recipe_info)
    #                 print("one recipe instance", one_recipe_instance)
    #                 one_user_instance.recipes.append(one_user_instance)
    #             all_users_with_recipes.append(one_user_instance)
    #         else:
    #             if one_recipe_info['id'] != None:
    #                 one_recipe_instance = recipe.Recipe(one_recipe_info)
    #                 print("one recipe instance", one_recipe_instance)
    #                 all_users_with_recipes[len(all_users_with_recipes)-1].recipes.append(one_recipe_instance)
    #     return all_users_with_recipes

