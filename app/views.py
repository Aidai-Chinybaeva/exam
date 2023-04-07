import os

from flask import request, render_template, url_for, redirect, flash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required

from . import app, db
from .models import Position, Employee, User
from .forms import PositionForm, EmployeeForm, PositionUpdateForm, EmployeeUpdateForm, UserRegisterForm, UserLoginForm


STATIC_ROOT = os.path.join('app', 'static')




def index():
    title = 'Index'
    return render_template('index.html', title=title)


def employee_detail(employee_id):
    employee = Employee.query.get(employee_id)
    title = Employee.name
    return render_template('employee_detail.html', employee=employee, title=title)




@login_required
def employee_create():
    form = EmployeeForm(meta={'csrf': False})
    if request.method == 'POST':
        if form.validate_on_submit():
            new_employee = Employee(
                name=form.name.data,
                inn=form.inn.data,
                position_id=form.position_id.data
            )
            db.session.add(new_employee)
            db.session.commit()
            flash('Cотрудник успешно сохранен', 'Успешно!')
            return redirect(url_for('index'))
        else:
            print(form.errors)
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При сохранении должности произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('form.html', form=form)



@login_required
def employee_update(employee_id):
    employee = Employee.query.get(employee_id)
    form = EmployeeUpdateForm(obj=employee)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('employee_list'))
        else:
            print(form.errors)
    return render_template('form.html', form=form)



@login_required
def employee_delete(employee_id):
    employee = Employee.query.get(employee_id)
    if request.method == "POST":
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('employee_list'))
    return render_template('employee_delete.html', employee=employee)


def position_create():
    form = PositionForm(meta={'csrf': False})
    if request.method == 'POST':
        if form.validate_on_submit():
            new_position = Position(
                name=form.name.data,
                department=form.department.data
            )
            db.session.add(new_position)
            db.session.commit()
            flash('Должность успешно сохранена', 'Успешно!')
            return redirect(url_for('index'))
    else:
        print(form.errors)
        text_list = []
        for field, errors in form.errors.items():
            text_list.append(f'{field} : {", ".join(errors)}')
        flash(f'При сохранении должности произошла ошибка{". ".join(text_list)}', 'Ошибка!')
    return render_template('form.html', form=form)


@login_required
def position_update(position_id):
    position = Position.query.get(position_id)
    form = PositionUpdateForm(obj=position)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(position)
            db.session.add(position)
            db.session.commit()
            return redirect(url_for('position_list'))
        else:
            print(form.errors)
    return render_template('form.html', form=form)


@login_required
def position_delete(position_id):
    position = Position.query.get(position_id)
    if request.method == "POST":
        db.session.delete(position)
        db.session.commit()
        return redirect(url_for('position_list'))
    return render_template('position_delete.html', position=position)


@login_required
def position_list():
    p_list = Position.query.all()
    return render_template('position_list.html', p_list=p_list)



def employee_list():
    empl_list = Employee.query.all()
    return render_template('empl_list.html', empl_list=empl_list)

def user_register():
    form = UserRegisterForm()
    title = 'Регистрация'
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Пользователь {new_user.username} успешно зарегестрирован', 'Успех!')
            return redirect(url_for('user_login'))
        else:
            text_list = []
            for field, errors in form.errors.items():
                text_list.append(f'{field} : {", ".join(errors)}')
            flash(f'При регистрации пользователя произошла ошибка{". ".join(text_list)}', 'Ошибка!')

    return render_template('account/index.html', form=form, title=title)



def user_login():
    form = UserLoginForm()
    title = 'Авторизация'
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему', 'Успех!')
                return redirect(url_for('index'))
            else:
                flash('Неверные логин и пароль', 'Ошибка!')

    return render_template('accounts/form.html', form=form, title=title)


def user_logout():
    logout_user()
    return redirect(url_for('user_login'))