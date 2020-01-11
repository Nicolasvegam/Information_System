from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,validators,SubmitField,ValidationError, IntegerField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired,Length,Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField




class loginForm(FlaskForm):

    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    submit=SubmitField('Register')

class EditWokerForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    first_name = StringField('First name',validators=[DataRequired()])
    surename = StringField('Surename',validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth (dd/mm/yyyy)',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    mobile = IntegerField('Mobile',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    starting_date = StringField('Starting Date (dd/mm/yyyy)',validators=[DataRequired()])
    wage = IntegerField('Wage',validators=[DataRequired()])
    available = StringField('Available (Y/N)',validators=[DataRequired()])
    plant = StringField('Plant',validators=[DataRequired()])

    username = StringField('Username',validators=[DataRequired()])
    password = StringField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    role =  QuerySelectField('Role', validators=[DataRequired()])
    project = QuerySelectField('Project', validators=[DataRequired()])

    editingScore = IntegerField('', validators=[Optional()])
    editingSkills = QuerySelectField('', validators=[DataRequired()])

    submit2 = SubmitField('Change Worker')

class WorkerForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    first_name = StringField('First name',validators=[DataRequired()])
    surename = StringField('Surename',validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth (dd/mm/yyyy)',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    mobile = IntegerField('Mobile',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    starting_date = StringField('Starting Date (dd/mm/yyyy)',validators=[DataRequired()])
    wage = IntegerField('Wage',validators=[DataRequired()])
    available = StringField('Available (Y/N)',validators=[DataRequired()])
    plant = StringField('Plant',validators=[DataRequired()])

    username = StringField('Username',validators=[DataRequired()])
    password = StringField('Password',validators=[DataRequired(),Length(min=4,max=20)])
    role =  QuerySelectField('Role', validators=[DataRequired()])
    project = QuerySelectField('Project', validators=[DataRequired()])

    soft1 = QuerySelectField('', validators=[DataRequired()])
    sscore1 = IntegerField()
    soft2 = QuerySelectField('', validators=[DataRequired()])
    sscore2 = IntegerField()
    soft3 = QuerySelectField('', validators=[DataRequired()])
    sscore3 = IntegerField()
    soft4 = QuerySelectField('', validators=[DataRequired()])
    sscore4 = IntegerField()

    submit = SubmitField('Add Worker')

class CreateEvaluationForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    starting_date = StringField('Starting Date (dd/mm/yyyy)',validators=[DataRequired()])
    project = QuerySelectField('Project', validators=[DataRequired()])

    submit = SubmitField('Add Evaluation')

class CreateProjectForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    duration = IntegerField('Duration in weeks',validators=[DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    starting_date = StringField('Starting Date (dd/mm/yyyy)', validators = [DataRequired()])

    submit = SubmitField('Add Project')

class ManageProjectForm(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    duration = IntegerField('Duration in weeks',validators=[DataRequired()])
    description = StringField('Description', validators = [DataRequired()])
    starting_date = StringField('Starting Date (dd/mm/yyyy)', validators = [DataRequired()])

    submit = SubmitField('Manage Project')

class SubmitEvaluationForm(FlaskForm):

    name = StringField('Name', validators=[Optional()])
    starting_date = StringField('Starting Date (dd/mm/yyyy)', validators=[Optional()])
    project = StringField('Project', validators=[Optional()])


    submit = SubmitField('Finish')

class FinishProject(FlaskForm):

    submit = SubmitField('Finish Project')
