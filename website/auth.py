from flask import Blueprint, render_template, request, redirect, url_for, flash
from website.funcs import userLogin
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user input from the form
        userID = request.form.get('userID')
        password = request.form.get('password')

        login_success, verified_user = userLogin(userID, password)
        if(login_success==True):
            flash('Logged in successfully!', category='success')
            login_user(verified_user)
            return redirect(url_for('views.dashboard'))

    # If it's a GET request, render the login form
    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))