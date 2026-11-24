from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.posts.models import User
from app.users.forms import RegistrationForm, LoginForm

users_bp = Blueprint('users', __name__, template_folder='templates/users', url_prefix='/users')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form, title='Register')

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Error: Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form, title='Login')

@users_bp.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@users_bp.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/users_list')
@login_required
def users_list():
    users = User.query.all()
    return render_template('users_list.html', users=users, title='Users List')