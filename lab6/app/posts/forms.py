from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=3, max=150)])
    content = TextAreaField('Контент', validators=[DataRequired()])
    category = SelectField('Категорія', choices=[
        ('news', 'Новини'),
        ('publication', 'Публікація'),
        ('tech', 'Технології'),
        ('other', 'Інше')
    ], default='other')
    publish_date = DateTimeLocalField('Дата публікації', format='%Y-%m-%dT%H:%M', default=None)
    enabled = BooleanField('Активний', default=True)
    submit = SubmitField('Зберегти')