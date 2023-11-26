from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe:
    db = "recipes_share"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_cooked = data['date_cooked']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        # Empty space for single User dictionary, a recipe is made/posted by ONE user

    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO recipes (user_id, name, description, instructions, under_30, date_cooked)
                VALUES (%(user_id)s, %(name)s, %(description)s, 
                %(instructions)s, %(under_30)s, %(date_cooked)s);
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def delete(cls, id):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, id)
        return results
    
    @classmethod
    def update(cls, data):
        query = """
                UPDATE recipes
                SET user_id = %(user_id)s,
                name = %(name)s,
                description = %(description)s,
                instructions = %(instructions)s,
                under_30 = %(under_30)s,
                date_cooked = %(date_cooked)s
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, id):
        query = """
                SELECT * FROM recipes
                WHERE id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, {"id": id})
        return cls(results[0])
    
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM recipes 
                JOIN users ON recipes.user_id = users.id;
                """
        # Users need to be associated/linked to recipes (display who posted what)
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipe_creator_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            maker = user.User(one_recipe_creator_data)
            one_recipe.creator = maker
            all_recipes.append(one_recipe)
        return all_recipes
    
    @classmethod
    def get_by_id(cls, data):
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)
        # print(results)
        if not results:
            return False
        results = results[0]
        one_recipe = cls(results)
        one_recipe_creator_data = {
                "id": results['user_id'],
                "first_name": results['first_name'],
                "last_name": results['last_name'],
                "email": results['email'],
                "password": results['password'],
                "created_at": results['users.created_at'],
                "updated_at": results['users.updated_at']
            }
        one_recipe.creator = user.User(one_recipe_creator_data)
        return one_recipe

    @staticmethod
    def validate_recipe(form_recipe):
        is_valid = True
        if len(form_recipe['name']) < 3:
            flash("Name of recipe needs to be at least 3 characters!", "recipe")
            is_valid = False
        if len(form_recipe['description']) < 3:
            flash("Description of recipe needs to be at least 3 characters!", "recipe")
            is_valid = False
        if len(form_recipe['instructions']) < 3:
            flash("Instructions of recipe needs to be at least 3 characters!", "recipe")
            is_valid = False
        if form_recipe['date_cooked'] == "":
            flash("Please input a date!", "recipe")
            is_valid = False
        if 'under_30' not in form_recipe:
            flash("Please choose an option!", "recipe")
            is_valid = False
        return is_valid