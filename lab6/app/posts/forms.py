from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime as dt

CATEGORIES = [
    ('news', 'Новини'),
    ('publication', 'Публікація'),
    ('tech', 'Технології'),
    ('other', 'Інше')
]

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2)])
    content = TextAreaField('Content', render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField('Active Post', default=True)
    publish_date = DateTimeLocalField('Publish Date', format="%Y-%m-%dT%H:%M", default=dt.now)
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('Add Post')