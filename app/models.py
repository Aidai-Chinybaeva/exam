from flask_login import UserMixin

from . import db, bcrypt, login_manager

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    department = db.Column(db.String(100))
    wage = db.Column(db.Integer)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inn = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String(100))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    position = db.relationship('Position', backref=db.backref('positions', lazy='dynamic'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)



    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)