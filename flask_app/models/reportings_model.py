from flask_app.config.dbconnection import connectToSQLite  # Updated import
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash

class Report:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date = data['date']
        self.number_of = data['number_of']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create_report(cls, data):
        if not data.get('user_id'):
            print("User ID is not set correctly.")
            return False  # or handle as appropriate
        # print("Data passed to create_report:", data)  
        
        query = """
        INSERT INTO reportings (location, what_happened, date, number_of, user_id)
        VALUES (:location, :what_happened, :date, :number_of, :user_id);
        """
        return connectToSQLite(DATABASE).query_db(query, data)

    @classmethod
    def getall(cls):
        query = """
        SELECT reportings.*, users.id as user_id, users.first_name, users.last_name, users.created_at as user_created_at, users.updated_at as user_updated_at
        FROM reportings
        JOIN users ON reportings.user_id = users.id;
        """
        results = connectToSQLite(DATABASE).query_db(query)
        all_reportings = []
        if results:
            for row in results:
                this_report = cls(row)
                user_data = {
                    'id': row['user_id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'created_at': row['user_created_at'],
                    'updated_at': row['user_updated_at']
                }
                this_user = user_model.User(user_data)
                this_report.creator = this_user
                all_reportings.append(this_report)
            return all_reportings

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM reportings LEFT JOIN users ON users.id = reportings.user_id WHERE reportings.id = :id"
        results = connectToSQLite(DATABASE).query_db(query, data)
        if results:
            report_instance = cls(results[0])
            user_data = {
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'created_at': results[0]['users.created_at'],
                'updated_at': results[0]['users.updated_at']
            }
            user_instance = user_model.User(user_data)
            report_instance.creator = user_instance
            return report_instance
        return False

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM reportings WHERE id = :id"
        return connectToSQLite(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
        UPDATE reportings SET location = :location, what_happened = :what_happened, number_of = :number_of, date = :date
        WHERE id = :id;
        """
        return connectToSQLite(DATABASE).query_db(query, data)

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['location']) < 2:
            flash("location must be at least 2 chars", 'reg')
            is_valid = False
        if len(form_data['what_happened']) < 2:
            flash("insert description", 'reg')
            is_valid = False
        if len(form_data['date']) < 1:
            flash("set date", 'reg')
            is_valid = False
        if len(form_data['number_of']) < 1:
            flash("number please", 'reg')
            is_valid = False 
        return is_valid
