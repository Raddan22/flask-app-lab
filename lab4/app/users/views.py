from flask import Blueprint, render_template, request, redirect, url_for, flash, session

users_bp = Blueprint('users', __name__, template_folder="templates/users", url_prefix='/users')

# Заглушка для автентифікації
USER_DATA = {"username": "admin", "password": "12345"}

@users_bp.route('/hi/<string:name>')
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)

@users_bp.route('/admin')
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45)
    print(to_url)
    return redirect(to_url)

# --- НОВЕ ДЛЯ ЛАБИ 4 ---

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USER_DATA['username'] and password == USER_DATA['password']:
            session['username'] = username
            flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Wrong data! Try again!', 'danger')
            return redirect(url_for('users.login'))
            
    return render_template('login.html')

@users_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть у систему.', 'warning')
        return redirect(url_for('users.login'))
        
    user_cookies = session.get('user_cookies', {})
    theme = session.get('theme', 'light')
    return render_template('profile.html', username=session['username'], cookies=user_cookies, theme=theme)

@users_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    key = request.form.get('key')
    value = request.form.get('value')
    if key and value:
        cookies = session.get('user_cookies', {})
        cookies[key] = value
        session['user_cookies'] = cookies
        flash(f'Кукі "{key}" додано!', 'success')
    return redirect(url_for('users.profile'))

@users_bp.route('/delete_cookie/<key>')
def delete_cookie(key):
    if 'username' not in session:
        return redirect(url_for('users.login'))
    cookies = session.get('user_cookies', {})
    if key in cookies:
        del cookies[key]
        session['user_cookies'] = cookies
        flash(f'Кукі "{key}" видалено!', 'success')
    return redirect(url_for('users.profile'))

@users_bp.route('/delete_all_cookies')
def delete_all_cookies():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    session.pop('user_cookies', None)
    flash('Всі кукі видалено!', 'success')
    return redirect(url_for('users.profile'))

@users_bp.route('/set_theme/<theme_name>')
def set_theme(theme_name):
    if theme_name in ['light', 'dark']:
        session['theme'] = theme_name
        flash(f'Тему змінено на {theme_name}!', 'success')
    return redirect(url_for('users.profile'))