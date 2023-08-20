from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe

class User:
    db = 'recipes'
    def __init__(self,data):
        self.id=data['id']
        self.user_name=data['user_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.recipes=[]

    
