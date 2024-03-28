from flask_app import app
from flask import render_template,redirect,request,flash,session
from flask_app.models.user_model import User
from flask_app.models.reportings_model import Report
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




@app.route('/users/new', methods =['POST'])
def reg_user():
    print('------------------------->',request.form)
    if not User.validator(request.form):
        return redirect('/')
    hashed_pass =  bcrypt.generate_password_hash(request.form['password'])
    data = {
         **request.form,
        'password': hashed_pass 
    }
    logged_user_id = User.create(data)
    session['user_id'] = logged_user_id 
    session['first_name'] = request.form['first_name']
    return redirect('/welcome')



@app.route('/users/login', methods = ['POST'])
def log_user():
    data = {
        'email': request.form['email']
    }
    user_in_db= User.get_by_email(data)
    if not user_in_db:
        flash("invalid credentials", 'log')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid credentials", 'log')
        return redirect("/") 
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/welcome')

@app.route('/users/logout')
def log_out():
    session.clear()  # This clears the entire session
    flash('You have been logged out successfullyyyy.', 'info')
    return redirect('/')
