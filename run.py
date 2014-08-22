from flask import Flask, redirect, url_for, session, request,g
from flask_oauth import OAuth
import sqlite3

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '684346394988556'
FACEBOOK_APP_SECRET = '82d89d321bc9eeefd7e6db5e011bd855'


DATABASE = 'db.sqlite.sqlite'
SECRET_KEY = 'development key'


app = Flask(__name__)
app.config.from_object(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():

    return redirect(url_for('login'))


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    g.db.execute('insert into User ( name, fb_id) values (?, ?)',
                 [me.data['id'], me.data['name'] ])
    g.db.commit()
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


if __name__ == '__main__':
    app.run()