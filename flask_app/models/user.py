from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "recipes_share"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        # Users can have many recipes
    
    @classmethod
    def save(cls, data):
        query = """
                INSERT into users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        print (results)
        # Insert Queries return id number of the row inserted
        return results
    
    @classmethod
    def get_by_id(cls, id):
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query,id)
        # print(results)
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        # Check to see if the email that the user inputted, matches an email/account in the database
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            # if one or more matching results returns, then the email is already being used 
            flash("Email is already taken.","register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters!","register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters!","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters!","register")
            is_valid = False
        if user['password'] != user['password_confirm']:
            flash("Passwords don't match!","register")
            is_valid = False
        return is_valid