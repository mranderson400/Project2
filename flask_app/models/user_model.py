from flask_app.config.dbconnection import connectToSQLite  # Updated import
from flask_app import DATABASE
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (:first_name, :last_name, :email, :password);
        """
        return connectToSQLite(DATABASE).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = :id"
        results = connectToSQLite(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = :email"
        results = connectToSQLite(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("first name must be at least 2 chars")
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("last name must be at least 2 chars")
            is_valid = False
        if len(form_data['email']) < 1:
            flash("email required")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("email invalid")
            is_valid = False
        else:
            data = {'email': form_data['email']}
            potential_user = User.get_by_email(data)
            if potential_user:
                flash("email already exists")
                is_valid = False
        if len(form_data['password']) < 8:
            flash("password must be at least 8 chars")
            is_valid = False
        elif form_data['password'] != form_data['conf_pass']:
            flash("passwords must match")
            is_valid = False
        return is_valid
