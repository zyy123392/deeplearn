from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    output = StringField('识别结果为：', validators=[Length(min=0, max=140)])


