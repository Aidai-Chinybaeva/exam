from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
import wtforms as wf

from .models import Position, Employee, User
from . import app


class PositionForm(FlaskForm):
    name = wf.StringField(label='Введите должность', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(max=40)
    ])
    department = wf.StringField(label='Введите название отдела', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(max=100)
    ])
    wage = wf.IntegerField(label='Ставка заработной платы', validators=[
        wf.validators.DataRequired()
    ])


def position_choices():
    choices = []
    with app.app_context():
        positions = Position.query.all()
        for position in positions:
            choices.append((position.id, position.position_name))
    return choices



class EmployeeForm(FlaskForm):
    name = wf.StringField(label='Введите ФИО сотрудника', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(max=100)
    ])
    inn = wf.StringField(label='ИНН клиента', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(14)
    ])
    position_id = wf.SelectField(label='Должность',validators=[
        wf.validators.DataRequired(),
     ])


def validate_inn(self, field):
    if Employee.query.filter_by(inn=field.data).count() > 0:
        raise wf.ValidationError('Сотрудник с данным инн уже существует')


def validate(self, *args, **kwargs):
    if not super().validate():
        return False
    if self.wage.data < 0:
        self.wage.errors.append('Заработная плата не должна быть отрицательной')
        return False



class PositionUpdateForm(FlaskForm):
    position_name = wf.StringField(label='Введите должность', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(max=40)
    ])
    department = wf.StringField(label='Введите название отдела', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(max=100)
    ])

class EmployeeUpdateForm(FlaskForm):
    name = wf.StringField(label='Введите ФИО сотрудника', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(max=100)
    ])
    position_id = wf.SelectField(label='Должность',validators=[
        wf.validators.DataRequired(),
     ])


class UserLoginForm(FlaskForm):
    username = wf.StringField(label='Логин', validators=[
        wf.validators.DataRequired(),
        wf.validators.Length(min=3, max=20)
    ])
    password = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

def validate_password(self, field):
    if len(field.data) < 8:
        raise wf.ValidationError('Длина пароля должна быть минимум 8 символов')


class UserRegisterForm(UserLoginForm):
    password2 = wf.PasswordField(label='Пароль', validators=[
        wf.validators.DataRequired(),
    ])

def validate(self, *args, **kwargs):
    if not super().validate(*args, **kwargs):
        return False
    if self.password.data != self.password2.data:
        self.password2.errors.append('Пароли должны совпадать')
        return False
    return True

def validate_username(self, field):
    if User.query.filter_by(username=field.data).count() > 0:
        raise wf.ValidationError('Пользователь с таким username уже существует')

