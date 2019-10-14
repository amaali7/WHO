from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from flask_ckeditor import CKEditor
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jsdg99d09g09ggdf0909dfgkgkldfg9dfg09dgkldgkldg09dg9gdkdg09g0909dg09dgkdgkdg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8vf1Qws!23456@127.0.0.1/whodb'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
# app.config['SECURITY_PASSWORD_SALT'] = None
app.config['MAIL_SERVER'] = 'smtp.google.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'who9est@gmail.com'
app.config['MAIL_PASSWORD'] = '8vf1qwert'

Net_CDN = True
# if not Net_CDN:

mail =Mail(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'waring'
login_manager.login_message ='Pleas login first'
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
ckeditor = CKEditor(app)


from Server.models import User, Role, AddNews, State, Locality

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


from Server.main.route import main
from Server.users.route import users
from Server.manager.route import manager
from Server.dashboard.route import dashboard
from Server.errors.handlers import errors
app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(manager)
app.register_blueprint(dashboard)
app.register_blueprint(errors)

security = Security(app, user_datastore)

@app.before_first_request
def create_user():
    # db.drop_all()
    db.create_all()
    a_user = User.query.filter_by(email='admin@who.int').first()
    if a_user is None:
        state = State(state_name="Khartoum")
        db.session.add(state)
        db.session.commit()
        locality = Locality(locality_name="Khartoum", state_in_id=1)
        db.session.add(locality)
        db.session.commit()
        with app.app_context():
            user_role = Role(name='user')
            super_user_role = Role(name='superuser')
            s_manager_role = Role(name='state_manager')
            l_manager_role = Role(name='locality_manager')
            db.session.add(super_user_role)
            db.session.add(s_manager_role)
            db.session.add(l_manager_role)
            db.session.add(user_role)
            db.session.commit()

            user_datastore.create_user(
                first_name='Admin',
                email='admin@who.int',
                password=bcrypt.generate_password_hash('admin').decode('utf-8'),
                locality = 'Khartoum',
                state = 'Khartoum',
                roles=[super_user_role]
            )
            db.session.commit()
        news1 = AddNews(title="First News",discription="First News",content="First News", user_id=1)
        news2 = AddNews(title="Second News",discription="Second News",content="Second News", user_id=1)
        news3 = AddNews(title="Third News",discription="Third News",content="Third News", user_id=1)
        db.session.add(news1)
        db.session.add(news2)
        db.session.add(news3)
        db.session.commit()



