from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_migrate import Migrate
from wtforms.validators import DataRequired, Length, Email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Registery(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")


class User(db.Model):  # 🔹 better capitalized
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@app.route('/')
def main():
    return f"<h1>Welcome to the Home Page</h1>"


@app.route('/Registery', methods=['GET','POST'])
def reg():
    form = Registery()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main'))  
    return render_template('reg.html', form=form)


@app.route('/users')
def users():
    user_list = User.query.all()
    return render_template('users.html', users=user_list)


if __name__ == "__main__":
    app.run(debug=True)



@app.route('/api/users', methods=['GET'])
def api_users():
    users = User.query.all()
    userData={}
    for user in users:
        userData[user.id] = {'username': user.username, 'email': user.email}
    return jsonify(userData)