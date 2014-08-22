from flask import Flask, render_template
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


app = Flask(__name__)
app.config['DEBUG'] = True








from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore

# ... create the app ...

app.config['SECURITY_POST_LOGIN'] = '/profile'

db = SQLAlchemy(app)


app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '684346394988556',
    'consumer_secret': '82d89d321bc9eeefd7e6db5e011bd855'
}
# ... define user and role models ...

from flask.ext.security import UserMixin, RoleMixin

from . import db


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin):

    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(120))
    active = db.Column(db.Boolean())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
            backref=db.backref('users', lazy='dynamic'))
    connections = db.relationship('Connection',
            backref=db.backref('user', lazy='joined'), cascade="all")



class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)

Security(app, SQLAlchemyUserDatastore(db, User, Role))
Social(app, SQLAlchemyConnectionDatastore(db, Connection))






@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'

@app.route('/hello')
def yello():
    return "Hello"

@app.route('/search')
def search():
    return render_template('base.html', search = youtube_search())


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404



if __name__ == "__main__":
    app.run()