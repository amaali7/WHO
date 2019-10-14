from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError
from flask_wtf.file import FileField, FileAllowed
from Server.models import User, State, Locality
from flask_ckeditor import CKEditorField

class AddUser(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                       validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    active = BooleanField('Active User', default=True)
    roles = SelectField('Roles', choices=[], validators=[DataRequired()])
    state = SelectField('State', choices=[], validators=[DataRequired()])
    locality = SelectField('Locality', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class AddRole(FlaskForm):
    name = StringField('First Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    description = StringField('Last Name',
                       validators=[DataRequired()])

    submit = SubmitField('Add Role')

class Add_News(FlaskForm):
    title = StringField('Title',validators=[DataRequired(), Length(min=2, max=50)])
    discription = StringField('Discription',validators=[DataRequired(), Length(min=2, max=250)])
    content = CKEditorField('content', validators=[DataRequired()])
    image = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add News')

class Update_News(FlaskForm):
    title = StringField('Title',validators=[DataRequired(), Length(min=2, max=250)])
    discription = StringField('Discription',validators=[DataRequired(), Length(min=2, max=250)])
    content = CKEditorField('content', validators=[DataRequired()])
    image = FileField('Update Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update News')

class StateForm(FlaskForm):
    state_name = StringField('State Name', validators=[DataRequired(), Length(min=2, max=20)])
    st_submit = SubmitField('Add')

    def validate_state_name(self, state_name):
        state = State.query.filter_by(state_name=state_name.data).first()
        if state:
            raise ValidationError('That State is already in system. Please choose a different one.')



class LocalityForm(FlaskForm):
    l_state_name = SelectField('State Name', choices=[])
    locality_name = StringField('Locality Name', validators=[DataRequired(), Length(min=2, max=20)])
    l_submit = SubmitField('Add')

    def validate_locality_name(self, locality_name):
        locality = Locality.query.filter_by(locality_name=locality_name.data).first()
        if locality:
            raise ValidationError('That Locality is already in system. Please choose a different one.')

class StateDeleteForm(FlaskForm):
    stateslist = SelectField('State Name', choices=[])
    dst_submit = SubmitField('Delete')

class LocalityDeleteForm(FlaskForm):
    localityslist = SelectField('Locality Name', choices=[])
    dstateslist = SelectField('State Name', choices=[])
    dl_submit = SubmitField('Delete')

class ImportDataForm(FlaskForm):
    file = FileField("Excel", validators=[FileAllowed(['xlsx'], message="Upload Xlsx file Only !!")])
    sheet = StringField("Sheet Name", validators=[DataRequired()])
    skiprows = IntegerField("Skip Rows", validators=[DataRequired()])
    submit = SubmitField("Import Data")

