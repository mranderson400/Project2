from flask_app import app
from flask import render_template,redirect,request,flash,session
from flask_app.models.user_model import User
from flask_app.models.reportings_model import Report



@app.route('/')
def index():
    
    return render_template("index.html")

@app.route('/report/create', methods = ['POST'])
def create_report():
    if "user_id" not in session:
        flash("You don't belong there!")
        return redirect('/')
    if not Report.validator(request.form):
        return redirect('/report/new')
    report_data = {
        **request.form,
        'user_id': session['user_id']
    }
    
    Report.create_report(report_data)
    return redirect('/welcome')


@app.route('/welcome')
def getall():
    try:
        all_reports = Report.getall()
        if all_reports is None:  # Ensure all_reports is always a list
            all_reports = []
    except Exception as e:
        print(f"Error fetching reports: {e}")
        all_reports = []  # In case of any exception, initialize it to an empty list

    return render_template('welcome.html', all_reports=all_reports)


@app.route('/report/new')
def new_report():
    if "user_id" not in session:
        return redirect('/')
    return render_template("reportings_new.html")

@app.route('/report/<int:id>/edit')
def edit_report(id):
    this_report = Report.get_one({'id':id})
    return render_template("reportings_edit.html", this_report= this_report)

@app.route('/report/<int:id>/update', methods =['POST'])
def update_report(id):
    if not Report.validator(request.form):
        return redirect(f"/report/{id}/edit")
    data ={
        **request.form,
        'id': id,
        'user_id':session['user_id']
    }
    
    Report.update(data)
    return redirect("/welcome")

@app.route('/report/<int:id>/view')
def get_one(id):
    if 'user_id' not in session:
        flash("user not logged in")
        return redirect('/')
    user_data = {'id': session['user_id']}
    this_report = Report.get_one({"id":id})
    logged_user = User.get_by_id(user_data)
    
    return render_template("reportings_view.html", logged_user= logged_user, this_report=this_report)

@app.route('/report/<int:id>/delete')
def delete_user(id):
    Report.delete({'id':id})
    return redirect('/welcome')

