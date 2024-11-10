from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from forms import LoginForm, SignupForm

#Authentication blueprint
auth_bp = Blueprint('auth', __name__)
# Parent User class 
class User:
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
#Authentication methods
    def is_authenticated(self):
        return True
#Active user
    def is_active(self):
        return True
#Anonymous user
    def is_anonymous(self):
        return False
#Get user id
    def get_id(self):
        return str(self.id)
# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
#validata data
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        #connect to the database
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        #update on login success
        if user and check_password_hash(user[3], password):
            user_obj = User(id=user[0], username=user[1], email=user[2], password_hash=user[3])
            login_user(user_obj)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        #update on login failure
        flash('Please check your login details and try again.', 'danger')
    #render login template
    return render_template('login.html', form=form)
#Signup route
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
#Validate signup data
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        #connect to the database
        conn = sqlite3.connect('resumes.db')
        c = conn.cursor()
        
        # Check if email already exists
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        if c.fetchone():
            conn.close()
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.signup'))
            
        # Create new user
        c.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                 (username, email, generate_password_hash(password)))
        conn.commit()
        conn.close()
        #update on signup success
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    #render signup template
    return render_template('signup.html', form=form)
#Logout route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    #redirect to login page
    return redirect(url_for('auth.login'))
#End of authentication blueprint