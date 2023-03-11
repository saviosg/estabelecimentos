from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, session
from flask_security import Security, hash_password
from flask_babel import Babel
from models import user_datastore, db
from routes import routes

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("FLASK_SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_REGISTER_URL'] = '/signup'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'login.html';
app.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'signup.html';

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'pt_BR')

babel = Babel(app, locale_selector=get_locale)

app.register_blueprint(routes)

app.config["MONGODB_SETTINGS"] = [
    {
        "db": os.environ.get('MONGODB_DB'),
        "host": os.environ.get('MONGODB_HOST'),
        "port": int(os.environ.get('MONGODB_PORT')),
    }
]
db.init_app(app)
app.security = Security(app, user_datastore)

with app.app_context():
    if not app.security.datastore.find_user(email="usuario@teste.com"):
        app.security.datastore.create_user(email="usuario@teste.com", password=hash_password("teste"))

if __name__ == '__main__':
    app.run(host=os.environ.get('FLASK_HOST'), port=os.environ.get('FLASK_PORT'))
