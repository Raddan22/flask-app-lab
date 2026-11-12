from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Введіть назву"),
        Length(min=3, message="Мінімум 3 символи")
    ])
    content = TextAreaField('Опис', validators=[
        DataRequired(message="Введіть опис"),
        Length(min=5, max=2000, message="Від 5 до 2000 символів")
    ])
    price = DecimalField('Ціна', validators=[
        DataRequired(message="Введіть ціну"),
        NumberRange(min=0.01, message="Ціна має бути додатною")
    ], places=2)
    category = SelectField('Категорія', choices=[
        ('electronics', 'Електроніка'),
        ('clothing', 'Одяг'),
        ('food', 'Продукти'),
        ('other', 'Інше')
    ], validators=[DataRequired()])
    quantity = IntegerField('Кількість', validators=[
        DataRequired(message="Введіть кількість"),
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ])
    image = FileField('Зображення', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], message="Тільки PNG, JPG, JPEG!")
    ])
    submit = SubmitField('Зберегти')