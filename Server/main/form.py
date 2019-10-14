from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError
from Server.models import User

class WForm(FlaskForm):
    state = StringField('State', validators=[DataRequired()])
    locality = StringField('Locality', validators=[DataRequired()])
    settlement = StringField('Settlement', validators=[Length(min=2, max=20)])
    name = StringField('Name of the Water Source', validators=[DataRequired(), Length(min=2, max=14)])
    type = SelectField('Type', choices=[('Borehole', 'Borehole'), ('O.D.W', 'O.D.W'), ('O.H.D.W', 'O.H.D.W'), ('Strong Tank', 'Strong Tank'), ('Water tap', 'Water tap'), ('Station', 'Station'), ('H.P', 'H.P'),  ('Surface water', 'Surface water'),  ('Other', 'Other')])
    other_type = StringField('If Other Type')
    status = SelectField('Status', choices=[('F', 'F'), ('NF', 'NF')])
    manage_by = StringField('Managed By', validators=[DataRequired(), Length(min=2, max=14)])
    longitude = StringField('Longitude', validators=[DataRequired(), Length(min=2, max=14)])
    latitude = StringField('Latitude', validators=[DataRequired(), Length(min=2, max=14)])
    date = StringField('Date')#, validators=[DataRequired(), Length(min=2, max=14)])
    e_coli = SelectField('E-Coli', choices=[('Category A', 'Category A'), ('Category B', 'Category B'),
                                            ('Category C', 'Category C'), ('Category D', 'Category D'),
                                            ('Category E', 'Category E')])
    sis = SelectField('Sanitary Inspection Score', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                            ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')])
    risk_analysis = StringField('Risk Analysis')
    action_take = SelectField('Action Taken', choices=[('No', 'No'), ('Yes', 'Yes'), ('On Going', 'On Going')])
    if_yes = StringField('If Yes or Ongoing Specify Action')
    frc= StringField('FRC', validators=[DataRequired()])
    turbidity= StringField('Turbidity', validators=[DataRequired()])
    ph= StringField('pH', validators=[DataRequired()])
    tds = StringField('TDS', validators=[DataRequired()])
    ec = StringField('E.C', validators=[DataRequired()])
    f = StringField('F', validators=[DataRequired()])
    no3 = StringField('NO3', validators=[DataRequired()])
    cl2 = StringField('Cl2', validators=[DataRequired()])
    fe = StringField('Fe', validators=[DataRequired()])

    submit = SubmitField('Submit')

class StateForm(FlaskForm):
    state_name = StringField('State Name', validators=[DataRequired(), Length(min=2, max=20)])
    st_submit = SubmitField('Add')

class LocalityForm(FlaskForm):
    l_state_name = SelectField('State Name', choices=[])
    locality_name = StringField('Locality Name', validators=[DataRequired(), Length(min=2, max=20)])
    l_submit = SubmitField('Add')

class WFormUpdate(FlaskForm):
    state = StringField('State', validators=[DataRequired()])
    locality = StringField('Locality', validators=[DataRequired()])
    settlement = StringField('Settlement', validators=[Length(min=2, max=20)])
    name = StringField('Name of the Water Source', validators=[DataRequired(), Length(min=2, max=14)])
    type = SelectField('Type', choices=[('Borehole', 'Borehole'), ('O.D.W', 'O.D.W'), ('O.H.D.W', 'O.H.D.W'), ('Strong Tank', 'Strong Tank'), ('Water tap', 'Water tap'), ('Station', 'Station'), ('H.P', 'H.P'),  ('Surface water', 'Surface water'),  ('Other', 'Other')])
    other_type = StringField('If Other Type')
    status = SelectField('Status', choices=[('F', 'F'), ('NF', 'NF')])
    manage_by = StringField('Managed By', validators=[DataRequired(), Length(min=2, max=14)])
    longitude = StringField('Longitude', validators=[DataRequired(), Length(min=2, max=14)])
    latitude = StringField('Latitude', validators=[DataRequired(), Length(min=2, max=14)])
    date = DateField('Data', format='%y/%m/%d', validators=[DataRequired()])
    e_coli = SelectField('E-Coli', choices=[('Category A', 'Category A'), ('Category B', 'Category B'),
                                            ('Category C', 'Category C'), ('Category D', 'Category D'),
                                            ('Category E', 'Category E')])
    sis = SelectField('Sanitary Inspection Score', choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                            ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')])
    risk_analysis = StringField('Risk Analysis')
    action_take = SelectField('Action Taken', choices=[('No', 'No'), ('Yes', 'Yes'), ('On Going', 'On Going')])
    if_yes = StringField('If Yes or Ongoing Specify Action')
    frc= StringField('FRC', validators=[DataRequired()])
    turbidity= StringField('Turbidity', validators=[DataRequired()])
    ph= StringField('pH', validators=[DataRequired()])
    tds = StringField('TDS', validators=[DataRequired()])
    ec = StringField('E.C', validators=[DataRequired()])
    f = StringField('F', validators=[DataRequired()])
    no3 = StringField('NO3', validators=[DataRequired()])
    cl2 = StringField('Cl2', validators=[DataRequired()])
    fe = StringField('Fe', validators=[DataRequired()])

    submit = SubmitField('Updete')