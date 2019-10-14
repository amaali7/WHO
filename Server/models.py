from datetime import datetime
from Server import db, login_manager
from flask_security import UserMixin, RoleMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from Server import app
import json

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    locality = db.Column(db.String(255), nullable=False,)
    state = db.Column(db.String(255), nullable=False, )
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    ws_data = db.relationship('WS_Data', backref='editor', lazy=True)
    news = db.relationship('AddNews', backref='author', lazy=True)

    def __str__(self):
        return self.email

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.load(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class WS_Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_commet = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    state = db.Column(db.String(80), nullable=False)
    locality = db.Column(db.String(80), nullable=False)
    settlement = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80))
    status = db.Column(db.String(80))
    manage_by = db.Column(db.String(80))
    longitude = db.Column(db.String(80))
    latitude = db.Column(db.String(80))
    date = db.Column(db.String(80))
    e_coli = db.Column(db.String(80))
    sis = db.Column(db.String(80))
    risk_analysis = db.Column(db.String(80))
    action_take = db.Column(db.String(80))
    if_yes_or_ongoing = db.Column(db.String(80))
    turbidity = db.Column(db.String(80))
    frc = db.Column(db.String(80))
    ph = db.Column(db.String(80))
    tds = db.Column(db.String(80))
    ec = db.Column(db.String(80))
    f = db.Column(db.String(80))
    no3 = db.Column(db.String(80))
    cl2 = db.Column(db.String(80))
    fe = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class State(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    state_name = db.Column(db.String(80), unique=True)
    localitys = db.relationship('Locality', backref='state_in', lazy=True)

    def __repr__(self):
        return f"State('{self.state_name}')"

class Locality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    locality_name = db.Column(db.String(80), unique=True)
    state_in_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    def __repr__(self):
        return f"Locality('{self.locality_name}')"

class AddNews(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(50))
    discription = db.Column(db.String(250))
    content = db.Column(db.String(5000), )
    image = db.Column(db.String(20), nullable=False, default='n1.jpg')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Dashboard(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(500))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    charts = db.relationship('Chart', backref='chart_in', lazy=True)

class Chart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    startdate = db.Column(db.String(80))
    enddate = db.Column(db.String(80))
    statefilter = db.Column(db.String(80))
    localityfilter = db.Column(db.String(80))
    typefilter = db.Column(db.String(80))
    riskfilter = db.Column(db.String(80))
    actionfilter = db.Column(db.String(80))
    status = db.Column(db.String(80))

    series1 = db.Column(db.String(80))
    series1_background = db.Column(db.String(80))
    series1_border = db.Column(db.String(80))

    series2 = db.Column(db.String(80))
    series2_background = db.Column(db.String(80))
    series2_border = db.Column(db.String(80))

    series3 = db.Column(db.String(80))
    series3_background = db.Column(db.String(80))
    series3_border = db.Column(db.String(80))

    series4 = db.Column(db.String(80))
    series4_background = db.Column(db.String(80))
    series4_border = db.Column(db.String(80))

    chart_type = db.Column(db.String(80))


    dashboard_in = db.Column(db.Integer, db.ForeignKey('dashboard.id'), nullable=False)

    def __repr__(self):
        return f"Locality('{self.locality_name}')"