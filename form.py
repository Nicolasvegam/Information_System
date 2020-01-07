from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators,SubmitField,ValidationError
from wtforms.validators import DataRequired,Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class loginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    submit=SubmitField('Register')

class WorkerForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    first_name = StringField('First name',validators=[DataRequired()])
    surename = StringField('Surename',validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth (dd/mm/yyyy)',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    mobile = StringField('Mobile',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    starting_date = StringField('Starting Date (dd/mm/yyyy)',validators=[DataRequired()])
    wage = StringField('Wage',validators=[DataRequired()])
    available = StringField('Available (Y/N)',validators=[DataRequired()])
    plant = StringField('Plant',validators=[DataRequired()])

    username = StringField('Username',validators=[DataRequired()])
    password = StringField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    role =  QuerySelectField('Role', validators=[DataRequired()])
    project = QuerySelectField('Project', validators=[DataRequired()])

    submit = SubmitField('Create')
