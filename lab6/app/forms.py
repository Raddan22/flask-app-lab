from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Поле обов'язкове"),
        Length(min=4, max=10, message="Довжина від 4 до 10 символів")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Поле обов'язкове"),
        Email(message="Невірний формат email")
    ])
    phone = StringField('Phone', validators=[
        DataRequired(message="Поле обов'язкове"),
        Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")
    ])
    subject = SelectField('Subject', choices=[
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('feedback', 'Відгук'),
        ('other', 'Інше')
    ], validators=[DataRequired()])
    message = TextAreaField('Message', validators=[
        DataRequired(message="Поле обов'язкове"),
        Length(max=500, message="Максимум 500 символів")
    ])
    submit = SubmitField('Send Message')