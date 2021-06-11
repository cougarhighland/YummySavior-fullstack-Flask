"""Auth routes module."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    """GET signup page."""
    if current_user.is_authenticated:
        return redirect(
            url_for('views.dashboard',
                    username=current_user.username,
                    user=current_user))

    return render_template(
        'signup.html',
        user=current_user)


@auth.route('/login')
def login():
    """GET login page."""
    if current_user.is_authenticated:
        return redirect(
            url_for('views.dashboard',
                    username=current_user.username,
                    user=current_user))

    return render_template(
        'login.html',
        user=current_user)


@auth.route('/login', methods=['POST'])
def login_post():
    """Log the user in."""
    # Retrieve the data the user entered into the form.
    username = request.form.get('username')
    password = request.form.get('password')

    # Find the user in the database
    user = User.query.filter_by(username=username).first()

    # If no user was found or the password was incorrect create error message
    # and redirect to the login page to display it.
    # status_code 401: Unauthorized
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect username or password!', category='error')
        return redirect(
            url_for('auth.login',
                    user=current_user))

    # If the above block didnt run, there is a user with the correct
    # credentials. Log the user in and create success message.

    login_user(user)
    flash("Log in Successful!", category='success')
    return redirect(
        url_for('views.dashboard',
                username=user.username,
                user=current_user))


@auth.route('/signup', methods=['POST'])
def signup_post():
    """Register a new user."""
    # Retrieve the data the user entered into the form.
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    businessname = request.form.get('businessname')
    location = request.form.get('location')
    user_type = request.form.get('user_type')

    if not (username and password and confirm and businessname and location and user_type):
        msg = "Missing required fields"
    else:
        # Check if there is a user in the database with the entered username
        user = User.query.filter_by(username=username).first()
        user_business = User.query.filter_by(businessname=businessname).first()
        # If there is a user, that username is not available. Create error msg
        if user:
            msg = 'Username not available!'
        elif user_business:
            msg = 'Business name is already in use!'
        # If no user with entered username, confirm the passwords match. If they
        # don't match, create the error message.
        elif password != confirm:
            msg = 'The passwords do not match!'
        # If username unique and passwords are correct.
        else:
            msg = 'Account created!'
            # Create the new user object
            user = User(username=username,
                        password=generate_password_hash(password, method='sha256'),
                        businessname=businessname,
                        location=location,
                        user_type=user_type)

            # Add the user to the database
            db.session.add(user)
            # Save the changes to the database
            db.session.commit()
            # Create message to display to user
            flash(msg, category='success')
            # log the user in
            login_user(user)
            # redirect the user to the dashboard
            return redirect(
                url_for('views.dashboard',
                        username=user.username,
                        user=current_user))

    flash(msg, category='error')
    # If the else block above didn't run, refresh the signup page
    # to display messages to user.
    return redirect(
        url_for('auth.signup',
                user=current_user))


@auth.route('/logout')
@login_required
def logout():
    """Logout the user."""
    logout_user()
    return redirect(
        url_for('views.home',
                user=current_user))
