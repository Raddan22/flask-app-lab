from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import ContactForm

@app.route('/')
def resume():
    return render_template('resume.html', title="Моє резюме")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Логування даних
        app.logger.info(f"Contact: Name={form.name.data}, Email={form.email.data}, Phone={form.phone.data}, Subject={form.subject.data}, Msg={form.message.data}")
        
        flash('Ваше повідомлення успішно відправлено!', 'success')
        return redirect(url_for('contact'))  # PRG-патерн
    
    return render_template('contacts.html', title="Контакти", form=form)

@app.route('/homepage')
def home():
    agent = request.user_agent.string
    return render_template('homepage.html', agent=agent, title="Homepage")