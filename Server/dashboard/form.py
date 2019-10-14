from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import Email, EqualTo, Length, DataRequired, ValidationError
from Server.models import User

class ChartPrepare(FlaskForm):
    name =StringField('Chart name', validators=[DataRequired()])
    startdate = StringField('Start at')
    enddate = StringField('End at')
    statefilter = SelectField('Filter By State', choices=[('None', 'None')])
    localityfilter = SelectField('Filter By Locality', choices=[('None', 'None')])
    typefilter = SelectField('Filter By Type', choices=[('None', 'None'), ('Borehole', 'Borehole'), ('O.D.W', 'O.D.W'), ('O.H.D.W', 'O.H.D.W'), ('Strong Tank', 'Strong Tank'), ('Water tap', 'Water tap'), ('Station', 'Station'), ('H.P', 'H.P'),  ('Surface water', 'Surface water'),  ('Other', 'Other')])
    riskfilter = SelectField('Filter By Risk Analysis', choices=[('None', 'None'), ('N.A.R', 'N.A.R'), ('L.A.P', 'L.A.P'), ('H.A.P', 'H.A.P'), ('U.A', 'U.A')])
    actionfilter = SelectField('Filter By Action Take', choices=[('None', 'None'), ('Yes', 'Yes'), ('No', 'No'), ('On Going', 'On Going')])

    status = SelectField('Status', choices=[('None', 'None'), ('F', 'F'), ('NF', 'NF'), ])
    series1 = SelectField('Series 1', choices=[('None', 'None'), ('e_coli', 'E-Coli'),
                                               ('sis', 'Sanitary Inspection Score'),
                                               ('frc', 'FRC'), ('turbidity', 'Turbidity'), ('ph', 'pH'),
                                               ('tds', 'TDS'), ('e.c', 'E.C'), ('f', 'F'), ('no3', 'NO3'),
                                               ('cl2', 'Cl2'), ('fe', 'Fe')])
    series1_background = StringField('Background')
    series1_border = StringField('Border')

    series2 = SelectField('Series 2', choices=[('None', 'None'), ('e_coli', 'E-Coli'),
                                               ('sis', 'Sanitary Inspection Score'),
                                               ('frc', 'FRC'), ('turbidity', 'Turbidity'), ('ph', 'pH'),
                                               ('tds', 'TDS'), ('e.c', 'E.C'), ('f', 'F'), ('no3', 'NO3'),
                                               ('cl2', 'Cl2'), ('fe', 'Fe')])
    series2_background = StringField('Background')
    series2_border = StringField('Border')

    series3 = SelectField('Series 3', choices=[('None', 'None'), ('e_coli', 'E-Coli'),
                                               ('sis', 'Sanitary Inspection Score'),
                                               ('frc', 'FRC'), ('turbidity', 'Turbidity'), ('ph', 'pH'),
                                               ('tds', 'TDS'), ('e.c', 'E.C'), ('f', 'F'), ('no3', 'NO3'),
                                               ('cl2', 'Cl2'), ('fe', 'Fe')])
    series3_background = StringField('Background')
    series3_border = StringField('Border')

    series4 = SelectField('Series 4', choices=[('None', 'None'), ('e_coli', 'E-Coli'),
                                               ('sis', 'Sanitary Inspection Score'),
                                               ('frc', 'FRC'), ('turbidity', 'Turbidity'), ('ph', 'pH'),
                                               ('tds', 'TDS'), ('e.c', 'E.C'), ('f', 'F'), ('no3', 'NO3'),
                                               ('cl2', 'Cl2'), ('fe', 'Fe')])
    series4_background = StringField('Background')
    series4_border = StringField('Border')

    chart_type = SelectField('Chart Type', choices=[('bar','Bar'), ('line','Line'), ('radar','Radar'),
                                                    ('polarArea','Polar Area'), ('pie','Pie'), ('doughnut','Doughnut')])



    submit = SubmitField('Add')

class DashBoard(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length( max=80)])
    title = StringField('Title', validators=[DataRequired(), Length( max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])

    submit = SubmitField('Add')

