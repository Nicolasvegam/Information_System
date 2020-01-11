from flask import Flask,render_template,redirect,session, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import exc, func
from sqlalchemy.orm import aliased
import math
from wtforms import StringField,PasswordField,validators,SubmitField,ValidationError, IntegerField, BooleanField


# I have to do:
# Make a lot of fake data (not mine)
# Separate Hardskills - Softskills x (every role)
# Improve html/design - repair (same field that doesn't permit spaces - not mine)
# That everyone has worker profile (just button) x
# Put logout button - x
# Put change mode to worker for PM and HR  - x
# HTML error with new_users - not mine
# - Evolution -> not possible, we have to change all database, and search a graph that permit that (html) -> not mine


# Worker
# Done

# PM
# - almost everything

# HR
# Submited change in workers, done. Skills change missing (Change or Add)

app = Flask(__name__)
app.config['SECRET_KEY']='ldjashfjahef;jhasef;jhase;jfhae;'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'

Bootstrap(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

## Worker
class Worker(db.Model):

    __tablename__= 'worker'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=True)
    first_name = db.Column(db.String(64),nullable=True)
    surename = db.Column(db.String(64),nullable=True)
    date_of_birth = db.Column(db.String(128),nullable=True)
    email = db.Column(db.String(64),nullable=True)
    mobile = db.Column(db.String(64),nullable=True)
    address = db.Column(db.String(128),nullable=True)
    starting_date = db.Column(db.String(128),nullable=True)
    wage = db.Column(db.Integer,nullable=True)
    available = db.Column(db.String(64),nullable=True)
    plant = db.Column(db.String(64),nullable=True)

    username = db.Column(db.String(64),index=True,unique=True)
    password = db.Column(db.String(128),nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))

    def __repr__(self):
        return '<Worker %s>'% self.username


class Role(db.Model):

    __tablename__='role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True)
    users = db.relationship('Worker',backref='role')

    def __repr__(self):
        return 'Role %s'% self.name


class Project(db.Model):

    __tablename__='project'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True)
    duration = db.Column(db.Integer,index=True)
    description = db.Column(db.String(1280),index=True)
    starting_date = db.Column(db.String(128),index=True)
    active = db.Column(db.String(64),nullable=True)
    users = db.relationship('Worker',backref='project')

    def __repr__(self):
        return 'Project %s'% self.name


class Project_to_Worker(db.Model):

    __tablename__='project_to_worker'
    id = db.Column(db.Integer,primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'))
    worker_id = db.Column(db.Integer,db.ForeignKey('worker.id'))


class Training(db.Model):

    __tablename__='training'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True)
    duration = db.Column(db.Integer,index=True)
    description = db.Column(db.String(1280),index=True)
    starting_date = db.Column(db.String(128),index=True)
    active = db.Column(db.String(64),nullable=True)
    responsible_id = db.Column(db.Integer,db.ForeignKey('worker.id'))


class Training_to_Worker(db.Model):

    __tablename__='training_to_worker'
    id = db.Column(db.Integer,primary_key=True)
    training_id = db.Column(db.Integer,db.ForeignKey('training.id'))
    worker_id = db.Column(db.Integer,db.ForeignKey('worker.id'))


class Competence(db.Model):

    __tablename__='competence'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True)
    short_name = db.Column(db.String(64),index=True)
    type = db.Column(db.String(64),index=True)
    description = db.Column(db.String(1280),index=True)

    def __repr__(self):
        return '%s'% self.name


class Competence_to_Worker(db.Model):

    __tablename__='competence_to_worker'
    id = db.Column(db.Integer,primary_key=True)
    competence_id = db.Column(db.Integer,db.ForeignKey('competence.id'))
    worker_id = db.Column(db.Integer,db.ForeignKey('worker.id'))
    score = db.Column(db.Integer,index=True)

    def __repr__(self):
        return '<Worker id {0} \n Competence id {1} Score {2}\n   >'.format(self.worker_id, self.competence_id, self.score)


class Evaluation_to_Competence(db.Model):

    __tablename__='evaluation_to_competence'
    id = db.Column(db.Integer,primary_key=True)
    competence_id = db.Column(db.Integer,db.ForeignKey('competence.id'))
    evaluation_id = db.Column(db.Integer,db.ForeignKey('evaluation.id'))
    score = db.Column(db.Integer,index=True)


class Evaluation(db.Model):

    __tablename__='evaluation'
    id = db.Column(db.Integer,primary_key=True)
    id_worker = db.Column(db.Integer,index=True)
    id_worker_ev = db.Column(db.Integer,index=True)
    id_project = db.Column(db.Integer,index=True)
    date = db.Column(db.String(1280),index=True)
    active = db.Column(db.String(128),index=True)


from form import loginForm, WorkerForm, CreateEvaluationForm, SubmitEvaluationForm, EditWokerForm, FinishProject, CreateProjectForm, ManageProjectForm

# Creating fake real data / first running app
@app.before_first_request
def create_all():

    db.create_all()
    db.session.add(Role(name='HR'))
    db.session.add(Role(name='PM'))
    db.session.add(Role(name='Worker'))

    #Creating fake users, be care abput integrity issues
    try:
        # Creating fake workers
        worker_role = Role.query.filter_by(name='Worker').first()
        worker_role2 = Role.query.filter_by(name='PM').first()
        worker_role3 = Role.query.filter_by(name='HR').first()

        description_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"

        new_projectHR = Project(name='HR', duration = 10000 , description = description_text, starting_date = '02/02/2019', active = 'Y')
        new_project = Project(name='Ferrari Project', duration = 10000 , description = description_text, starting_date = '02/02/2019', active = 'Y')
        new_project2 = Project(name='Fiat Project', duration = 15000 , description = description_text, starting_date = '15/03/2019', active = 'Y')
        new_project3 = Project(name='Alfa Romeo Project', duration = 15050 , description = description_text, starting_date = '05/11/2019', active = 'Y')
        new_project4 = Project(name='Hardware Development', duration = 10000 , description = description_text, starting_date = '02/02/2019', active = 'N')

        db.session.add(new_projectHR)
        db.session.add(new_project)
        db.session.add(new_project2)
        db.session.add(new_project3)
        db.session.add(new_project4)
        db.session.flush()

        w_user = Worker(name='Nicolas Vega', first_name = 'Nicolas', surename = 'Vega', date_of_birth= '23/04/1997',
        email = 'ndvega@uc.cl', mobile = '983743848', address = 'Amerigo Vespucci 60', starting_date = '02/12/1998',
        wage = 100000, available = 'N', username='nicovega',password='1234567', role_id = worker_role.id, project_id = new_project.id, plant = 'Plant 1')

        pm_user = Worker(name='Juan Pablo Fernandez', first_name = 'Juan', surename = 'Fernandez', date_of_birth= '23/05/1987',
        email = 'jpfernadez@uc.cl', mobile = '847839848', address = 'via Ferruci 34', starting_date = '08/09/2000',
        wage = 150000, available = 'N', username='jpfernandez',password='1234567', role_id = worker_role2.id, project_id = new_project.id, plant = 'Plant 1')

        hr_user = Worker(name='Jose Vila', date_of_birth= '23/07/1967', first_name = 'Jose', surename = 'Vila',
        email = 'josevila@uc.cl', mobile = '938474943', address = 'Corso di Duca 45', starting_date = '12/11/2009',
        wage = 170000, available = 'N', username='josevila',password='1234567', role_id = worker_role3.id, project_id = new_projectHR.id, plant = 'Plant 2')

        db.session.add(w_user)
        db.session.add(pm_user)
        db.session.add(hr_user)
        db.session.flush()

        r_project_worker = Project_to_Worker(project_id = new_project.id , worker_id = w_user.id)
        r_project_worker2 = Project_to_Worker(project_id = new_project.id , worker_id = pm_user.id)
        r_project_worker3 = Project_to_Worker(project_id = new_project4.id , worker_id = w_user.id)


        db.session.add(r_project_worker)
        db.session.add(r_project_worker2)
        db.session.add(r_project_worker3)

        new_training = Training(name='Soft skills training', duration = 3 , description = 'Insert description', starting_date = '03/03/2020', active = 'N',
        responsible_id = hr_user.id)

        db.session.add(new_training)
        db.session.flush()

        r_training_worker = Training_to_Worker(training_id = new_training.id, worker_id = w_user.id)
        r_training_worker2 = Training_to_Worker(training_id = new_training.id, worker_id = pm_user.id)

        db.session.add(r_training_worker)
        db.session.add(r_training_worker2)

        new_competence = Competence(name='Python', short_name='PY', type = 'Programming', description = 'Insert description')
        new_competence2 = Competence(name='C++', short_name='C++', type = 'Programming', description = 'Insert description')
        new_competence3 = Competence(name='Ruby', short_name='RB', type = 'Programming', description = 'Insert description')
        new_competence4 = Competence(name='Leadership', short_name='LD', type = 'Soft skills', description = 'Insert description')
        new_competence5 = Competence(name='iOs', short_name='iOS', type = 'Programming', description = 'Insert description')
        new_competence6 = Competence(name='Flask', short_name='FK', type = 'Programming', description = 'Insert description')
        new_competence7 = Competence(name='Matlab', short_name='ML', type = 'Programming', description = 'Insert description')
        new_competence8 = Competence(name='Android', short_name='AND', type = 'Programming', description = 'Insert description')
        new_competence9 = Competence(name='JavaScript', short_name='JS', type = 'Programming', description = 'Insert description')
        new_competence10 = Competence(name='C', short_name='C', type = 'Programming', description = 'Insert description')
        new_competence11 = Competence(name='SQL', short_name='SQL', type = 'Programming', description = 'Insert description')
        new_competence12 = Competence(name='Attitude', short_name='AT', type = 'Soft skills', description = 'Insert description')
        new_competence13 = Competence(name='Communication', short_name='CM', type = 'Soft skills', description = 'Insert description')
        new_competence14 = Competence(name='Creative Thinking', short_name='CT', type = 'Soft skills', description = 'Insert description')
        new_competence15 = Competence(name='Teamwork', short_name='TW', type = 'Soft skills', description = 'Insert description')
        new_competence16 = Competence(name='Problem-solving', short_name='PS', type = 'Soft skills', description = 'Insert description')
        new_competence17 = Competence(name='Time Management', short_name='TM', type = 'Soft skills', description = 'Insert description')


        db.session.add(new_competence)
        db.session.add(new_competence2)
        db.session.add(new_competence3)
        db.session.add(new_competence4)
        db.session.add(new_competence5)
        db.session.add(new_competence6)
        db.session.add(new_competence7)
        db.session.add(new_competence8)
        db.session.add(new_competence9)
        db.session.add(new_competence10)
        db.session.add(new_competence11)
        db.session.add(new_competence12)
        db.session.add(new_competence13)
        db.session.add(new_competence14)
        db.session.add(new_competence15)
        db.session.add(new_competence16)
        db.session.add(new_competence17)
        db.session.flush()

        r_competence_worker = Competence_to_Worker(competence_id = new_competence.id, worker_id = w_user.id, score = 78)
        r_competence_worker2 = Competence_to_Worker(competence_id = new_competence2.id, worker_id = w_user.id, score = 86)
        r_competence_worker3 = Competence_to_Worker(competence_id = new_competence4.id, worker_id = w_user.id, score = 57)
        r_competence_worker10 = Competence_to_Worker(competence_id = new_competence3.id, worker_id = w_user.id, score = 57)
        r_competence_worker13 = Competence_to_Worker(competence_id = new_competence5.id, worker_id = w_user.id, score = 70)
        r_competence_worker14 = Competence_to_Worker(competence_id = new_competence6.id, worker_id = w_user.id, score = 99)
        r_competence_worker15 = Competence_to_Worker(competence_id = new_competence7.id, worker_id = w_user.id, score = 79)
        r_competence_worker16 = Competence_to_Worker(competence_id = new_competence8.id, worker_id = w_user.id, score = 59)
        r_competence_worker17 = Competence_to_Worker(competence_id = new_competence9.id, worker_id = w_user.id, score = 39)
        r_competence_worker18 = Competence_to_Worker(competence_id = new_competence10.id, worker_id = w_user.id, score = 69)
        r_competence_worker19 = Competence_to_Worker(competence_id = new_competence11.id, worker_id = w_user.id, score = 49)
        r_competence_worker20 = Competence_to_Worker(competence_id = new_competence12.id, worker_id = w_user.id, score = 69)
        r_competence_worker21 = Competence_to_Worker(competence_id = new_competence13.id, worker_id = w_user.id, score = 89)

        r_competence_worker4 = Competence_to_Worker(competence_id = new_competence.id, worker_id = pm_user.id, score = 65)
        r_competence_worker5 = Competence_to_Worker(competence_id = new_competence2.id, worker_id = pm_user.id, score = 45)
        r_competence_worker6 = Competence_to_Worker(competence_id = new_competence4.id, worker_id = pm_user.id, score = 80)
        r_competence_worker11 = Competence_to_Worker(competence_id = new_competence3.id, worker_id = pm_user.id, score = 57)
        r_competence_worker22 = Competence_to_Worker(competence_id = new_competence14.id, worker_id = w_user.id, score = 29)
        r_competence_worker23 = Competence_to_Worker(competence_id = new_competence15.id, worker_id = w_user.id, score = 59)
        r_competence_worker24 = Competence_to_Worker(competence_id = new_competence16.id, worker_id = w_user.id, score = 79)
        r_competence_worker25 = Competence_to_Worker(competence_id = new_competence17.id, worker_id = w_user.id, score = 79)

        r_competence_worker7 = Competence_to_Worker(competence_id = new_competence.id, worker_id = hr_user.id, score = 0)
        r_competence_worker8 = Competence_to_Worker(competence_id = new_competence2.id, worker_id = hr_user.id, score = 0)
        r_competence_worker9 = Competence_to_Worker(competence_id = new_competence4.id, worker_id = hr_user.id, score = 70)
        r_competence_worker12 = Competence_to_Worker(competence_id = new_competence3.id, worker_id = hr_user.id, score = 57)

        db.session.add(r_competence_worker)
        db.session.add(r_competence_worker2)
        db.session.add(r_competence_worker3)
        db.session.add(r_competence_worker4)
        db.session.add(r_competence_worker5)
        db.session.add(r_competence_worker6)
        db.session.add(r_competence_worker7)
        db.session.add(r_competence_worker8)
        db.session.add(r_competence_worker9)
        db.session.add(r_competence_worker10)
        db.session.add(r_competence_worker11)
        db.session.add(r_competence_worker12)
        db.session.add(r_competence_worker13)
        db.session.add(r_competence_worker14)
        db.session.add(r_competence_worker15)
        db.session.add(r_competence_worker16)
        db.session.add(r_competence_worker17)
        db.session.add(r_competence_worker18)
        db.session.add(r_competence_worker19)
        db.session.add(r_competence_worker20)
        db.session.add(r_competence_worker21)
        db.session.add(r_competence_worker22)
        db.session.add(r_competence_worker23)
        db.session.add(r_competence_worker24)
        db.session.add(r_competence_worker25)


        new_evaluation = Evaluation( id_worker = w_user.id, id_worker_ev = pm_user.id, id_project = new_project.id, date = '21/01/2020', active = 'N')
        new_evaluation2 = Evaluation( id_worker = pm_user.id, id_worker_ev = w_user.id, id_project = new_project.id, date = '21/01/2020', active = 'N')
        new_evaluation3 = Evaluation( id_worker = pm_user.id, id_worker_ev = w_user.id, id_project = new_project.id, date = '21/06/2020', active = 'Y')

        db.session.add(new_evaluation)
        db.session.add(new_evaluation2)
        db.session.add(new_evaluation3)
        db.session.flush()


        r_evaluation_competence = Evaluation_to_Competence( competence_id = new_competence.id, evaluation_id = new_evaluation.id, score = 100)
        r_evaluation_competence2 = Evaluation_to_Competence( competence_id = new_competence2.id, evaluation_id = new_evaluation.id, score = 80)
        r_evaluation_competence3 = Evaluation_to_Competence( competence_id = new_competence4.id, evaluation_id = new_evaluation.id, score = 20)

        r_evaluation_competence4 = Evaluation_to_Competence( competence_id = new_competence.id, evaluation_id = new_evaluation2.id, score = 50)
        r_evaluation_competence5 = Evaluation_to_Competence( competence_id = new_competence2.id, evaluation_id = new_evaluation2.id, score = 50)
        r_evaluation_competence6 = Evaluation_to_Competence( competence_id = new_competence4.id, evaluation_id = new_evaluation2.id, score = 90)

        db.session.add(r_evaluation_competence)
        db.session.add(r_evaluation_competence2)
        db.session.add(r_evaluation_competence3)
        db.session.add(r_evaluation_competence4)
        db.session.add(r_evaluation_competence5)
        db.session.add(r_evaluation_competence6)
        db.session.commit()



    except exc.IntegrityError as err:

        db.session.rollback()

# Creating one worker by app
def create_worker(name, first_name, surename, date_of_birth, email, mobile,
address, starting_date, wage, available, username, password, role, project,
plant, soft1, sscore1, soft2, sscore2, soft3, sscore3, soft4, sscore4):#, hard1,
#hscore1, hard2, hscore2, hard3, hscore3, hard4, hscore4):

    try:

        user = Worker(name= name, first_name = first_name, surename = surename, date_of_birth= date_of_birth,
        email = email, mobile = mobile, address = address, starting_date = starting_date,
        wage = wage, available = available, username = username,password = password, role_id = role.id,
        project_id = project.id, plant = plant)

        db.session.add(user)
        db.session.flush()

        project_worker = Project_to_Worker(project_id = project.id , worker_id = user.id)

        db.session.add(project_worker)

        competence_worker1 = Competence_to_Worker(competence_id = soft1.id, worker_id = user.id, score = sscore1)
        competence_worker2 = Competence_to_Worker(competence_id = soft2.id, worker_id = user.id, score = sscore2)
        competence_worker3 = Competence_to_Worker(competence_id = soft3.id, worker_id = user.id, score = sscore3)
        competence_worker4 = Competence_to_Worker(competence_id = soft4.id, worker_id = user.id, score = sscore4)

        #competence_worker5 = Competence_to_Worker(competence_id = hard1.id, worker_id = user.id, score = hscore1)
        #competence_worker6 = Competence_to_Worker(competence_id = hard2.id, worker_id = user.id, score = hscore2)
        #competence_worker7 = Competence_to_Worker(competence_id = hard3.id, worker_id = user.id, score = hscore3)
        #competence_worker8 = Competence_to_Worker(competence_id = hard4.id, worker_id = user.id, score = hscore4)

        db.session.add(competence_worker1)
        db.session.add(competence_worker2)
        db.session.add(competence_worker3)
        db.session.add(competence_worker4)
        #db.session.add(competence_worker5)
        #db.session.add(competence_worker6)
        #db.session.add(competence_worker7)
        #db.session.add(competence_worker8)
        db.session.commit()

    except exc.IntegrityError as err:

        print("Not possible user creation")
        db.session.rollback()

def create_evaluation(name, project, date):

    try:
        #Search for every worker in the project
        project_workers = db.session.query(Worker).filter(Worker.project_id == project.id).all()

        for worker in project_workers:
            team = db.session.query(Worker).filter(Worker.project_id == project.id).filter(Worker.id != worker.id).all()
            for teammate in team:
                ev = Evaluation( id_worker = worker.id, id_worker_ev = teammate.id, id_project = project.id, date = date, active = 'Y')
                db.session.add(ev)

        db.session.flush()
        db.session.commit()


    except exc.IntegrityError as err:

        print("Not possible evalution creation")
        db.session.rollback()


def active_evaluations():
    query = db.session.query(Project, Evaluation, func.count(Evaluation.id_project)).filter(Evaluation.active == 'Y').filter(Project.id == Evaluation.id_project).group_by(Evaluation.id_project).all()
    return query


def getting_my_evaluations(user):
    query = db.session.query(Project, Evaluation, Project_to_Worker, Worker).filter(Project.id == Evaluation.id_project).filter(Project_to_Worker.worker_id == Evaluation.id_worker).filter(Evaluation.id_worker == user.id).filter(Evaluation.id_worker_ev == Worker.id).filter(Project_to_Worker.project_id == Project.id).filter(Evaluation.active == 'Y').all()
    return query


@app.route('/submitEvaluation<id>',methods=['POST','GET'])
def submit_evaluation(id):

    query = db.session.query(Evaluation).filter(Evaluation.id == id).first()

    id_user = query.id_worker
    idev_user = query.id_worker_ev
    id_worker = query.id_project

    user = db.session.query(Worker).filter(Worker.id == id_user).first()
    user_ev = db.session.query(Worker).filter(Worker.id == idev_user).first()
    user_skills = db.session.query(Worker, Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).all()
    user_ev_skills = db.session.query(Worker, Competence).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == idev_user).filter(Competence.id == Competence_to_Worker.competence_id).all()
    role_user = db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Worker.id == id_user).first()
    project_user = db.session.query(Worker,Project).filter(Project.id == Worker.project_id).filter(Worker.id == id_user).first()

    av = db.session.query(Worker, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).first()

    average = av[2]

    for skill in user_ev_skills:
        setattr(SubmitEvaluationForm, skill[1].name, StringField('Skill'))
        setattr(SubmitEvaluationForm, skill[1].name + 'score', IntegerField('Score'))

    Submit_EvaluationForm = SubmitEvaluationForm()

    if request.method == 'GET':

        Submit_EvaluationForm.name.data = user_ev.name #prepopulate
        Submit_EvaluationForm.project.data = project_user[1].name #prepopulate

        for skill in user_ev_skills:
            name = getattr(Submit_EvaluationForm, skill[1].name)
            name.data = skill[1].name #prepopulate

    elif request.method == 'POST' and Submit_EvaluationForm.validate_on_submit():

        ev = {}
        for skill in user_ev_skills:
            sk = getattr(Submit_EvaluationForm, skill[1].name)
            sc = getattr(Submit_EvaluationForm, skill[1].name + 'score')
            ev[sk.data] = sc.data


        for sk, sc in ev.items():
            skills =  db.session.query(Competence_to_Worker, Competence).filter(Competence_to_Worker.worker_id == idev_user).filter(Competence.id == Competence_to_Worker.competence_id).filter(Competence.name == sk).first()
            skills[0].score = round(skills[0].score*0.9 + sc*0.1 , 2) #this is the algorithm

        query.active = 'N'
        db.session.commit()

        return redirect('home')



    return render_template('gtemplates/submitReport.html', user=user, role = role_user, user_ev = user_ev, user_ev_skills = user_ev_skills,
    project=project_user, formReg = Submit_EvaluationForm, average = average, top_4 = top_4skills(id_user))


@app.route('/seeReports<id>',methods=['GET'])
def see_more(id):
    sub_query = db.session.query(Worker).subquery()
    evaluations = db.session.query(Project, Evaluation, Worker, sub_query).filter(Evaluation.active == 'Y').filter(Project.id == id).filter(Project.id == Evaluation.id_project).filter(Worker.id == Evaluation.id_worker).filter(sub_query.c.id == Evaluation.id_worker_ev).all()

    return render_template('gtemplates/seeMore.html', ev = evaluations, len = len(evaluations))

@app.route('/editWorker<id>',methods=['POST','GET'])
def edit_worker(id):

    user = db.session.query(Worker).filter(Worker.id == id).first()
    user_skills = db.session.query(Worker, Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id).filter(Competence.id == Competence_to_Worker.competence_id).order_by(Competence_to_Worker.score.desc()).all()
    role_user = db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Worker.id == id).first()
    project_user = db.session.query(Worker,Project).filter(Project.id == Worker.project_id).filter(Worker.id == id).first()

    Worker_Form = EditWokerForm()

    my_query = db.session.query(Project).all()
    my_query2 = db.session.query(Role).all()
    my_query3 = db.session.query(Competence).all()
    my_query4 = db.session.query(Competence).order_by(Competence.id.asc()).all()

    Worker_Form.editingSkills.query = my_query4
    Worker_Form.project.query = my_query
    Worker_Form.role.query = my_query2
    av = db.session.query(Worker, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id).first()

    average = av[2]

    if request.method == 'GET':
        Worker_Form.name.data = user.name
        Worker_Form.first_name.data = user.first_name
        Worker_Form.surename.data = user.surename
        Worker_Form.date_of_birth.data = user.date_of_birth
        Worker_Form.email.data = user.email
        Worker_Form.mobile.data = user.mobile
        Worker_Form.address.data = user.address
        Worker_Form.starting_date.data = user.starting_date
        Worker_Form.wage.data = user.wage
        Worker_Form.available.data = user.available
        Worker_Form.plant.data = user.plant
        Worker_Form.username.data = user.username
        Worker_Form.password.data = user.password


    elif request.method == 'POST' and Worker_Form.validate_on_submit():

        user.name = Worker_Form.name.data
        user.first_name = Worker_Form.first_name.data
        user.surename = Worker_Form.surename.data
        user.date_of_birth = Worker_Form.date_of_birth.data
        user.email = Worker_Form.email.data
        user.mobile = Worker_Form.mobile.data
        user.address = Worker_Form.address.data
        user.starting_date = Worker_Form.starting_date.data
        user.wage = Worker_Form.wage.data
        user.available = Worker_Form.available.data
        user.plant = Worker_Form.plant.data
        user.username = Worker_Form.username.data
        user.password = Worker_Form.password.data
        user.role_id = Worker_Form.role.data.id
        user.project_id = Worker_Form.project.data.id

        if Worker_Form.editingScore.data:
            query = db.session.query(Competence_to_Worker).filter(id == Competence_to_Worker.worker_id).filter(Worker_Form.editingSkills.data.id == Competence_to_Worker.competence_id).first()
            if query:
                query.score = Worker_Form.editingScore.data
            else:
                competence_worker = Competence_to_Worker(competence_id = Worker_Form.editingSkills.data.id, worker_id = id, score = Worker_Form.editingScore.data)
                db.session.add(competence_worker)

        db.session.commit()
        db.session.flush()

    return render_template('gtemplates/editWorker.html', user=user, skills=user_skills,
    len_skills=len(user_skills), role = role_user, project=project_user, formReg = Worker_Form,
    average = average, top_4 = top_4skills(id))


@app.route('/manageProject<id>', methods=['POST', 'GET'])
def manageProject(id):

    project = db.session.query(Project).filter(Project.id == id).first()

    #project_users =  db.session.query(Worker, Role, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Role.id == Worker.role_id).filter(Worker.id == Competence_to_Worker.worker_id).filter(Worker.project == id).group_by(Worker.id).all()
    project_users = db.session.query(Worker, Role, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Role.id == Worker.role_id).filter(Worker.id == Competence_to_Worker.worker_id).group_by(Worker.id).filter(Worker.project_id == id).filter(Worker.available == 'N').all()
    not_project_users = db.session.query(Worker, Role, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Role.id == Worker.role_id).filter(Worker.id == Competence_to_Worker.worker_id).group_by(Worker.id).filter(Worker.available == 'Y').all()
    #print(proj)
    #not_project_users =  db.session.query(Worker, Role, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Role.id == Worker.role_id).filter(Worker.id == Competence_to_Worker.worker_id).group_by(Worker.id).all()

    for user in project_users:
        setattr(ManageProjectForm, user[0].name, StringField('Name'))
        setattr(ManageProjectForm, user[0].name + 'check', BooleanField('Bool'))

    for user in not_project_users:
        setattr(ManageProjectForm, user[0].name, StringField('Name'))
        setattr(ManageProjectForm, user[0].name + 'check', BooleanField('Bool'))

    ProjectForm = ManageProjectForm()

    if request.method == 'GET':

        ProjectForm.name.data = project.name
        ProjectForm.description.data = project.description
        ProjectForm.duration.data = project.duration
        ProjectForm.starting_date.data = project.starting_date

        for user in project_users:
            name = getattr(ProjectForm, user[0].name)
            name.data = user[0].name

        for user in not_project_users:
            name = getattr(ProjectForm, user[0].name)
            name.data = user[0].name

    elif request.method == 'POST' and ProjectForm.validate_on_submit():

        ev1 = {}
        for user in project_users:
            us = getattr(ProjectForm, user[0].name)
            bl = getattr(ProjectForm, user[0].name + 'check')
            ev1[us.data] = bl.data

        ev2 = {}
        for user in not_project_users:
            us = getattr(ProjectForm, user[0].name)
            bl = getattr(ProjectForm, user[0].name + 'check')
            ev2[us.data] = bl.data

        project.name = ProjectForm.name.data
        project.duration = ProjectForm.duration.data
        project.description = ProjectForm.description.data
        project.starting_date = ProjectForm.starting_date.data

        #Agregar
        for sk, sc in ev2.items():

            if sc:
                user_ =  db.session.query(Worker).filter(Worker.name == sk).first()
                project_worker = Project_to_Worker(project_id = project.id , worker_id = user_.id)
                db.session.add(project_worker)
                user_.project_id = project.id
                user_.available = 'N'

        #Quitar
        for sk, sc in ev1.items():

            if not sc:
                user_ =  db.session.query(Worker).filter(Worker.name == sk).first()
                user_.available = 'Y'

        db.session.flush()
        db.session.commit()

        return redirect('home')

    return render_template('gtemplates/manageProject.html', project = project, ProjectForm = ProjectForm,
    project_users = project_users, not_project_users = not_project_users)


@app.route('/createProject', methods=['POST', 'GET'])
def createProject():

    active_users =  db.session.query(Worker, Role, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Role.id == Worker.role_id).filter(Worker.id == Competence_to_Worker.worker_id).filter(Worker.available == 'Y').group_by(Worker.id).all()

    for user in active_users:
        setattr(CreateProjectForm, user[0].name, StringField('Name'))
        setattr(CreateProjectForm, user[0].name + 'check', BooleanField('Bool'))

    ProjectForm = CreateProjectForm()

    if request.method == 'GET':

        for user in active_users:
            name = getattr(ProjectForm, user[0].name)
            name.data = user[0].name

    elif request.method == 'POST' and ProjectForm.validate_on_submit():

        ev = {}
        for user in active_users:
            us = getattr(ProjectForm, user[0].name)
            bl = getattr(ProjectForm, user[0].name + 'check')
            ev[us.data] = bl.data


        new_project = Project(name= ProjectForm.name.data, duration = ProjectForm.duration.data , description = ProjectForm.description.data, starting_date = ProjectForm.starting_date.data, active = 'Y')
        db.session.add(new_project)

        for sk, sc in ev.items():

            if sc:
                user_ =  db.session.query(Worker).filter(Worker.name == sk).first()
                project_worker = Project_to_Worker(project_id = new_project.id , worker_id = user_.id)
                db.session.add(project_worker)
                user_.project_id = new_project.id
                user_.available = 'N'

        db.session.flush()
        db.session.commit()

        return redirect('home')

    return render_template('gtemplates/createProject.html', ProjectForm = ProjectForm,
    active_users = active_users, len_active = len(active_users))


@app.route('/workerProfile', methods=['POST', 'GET'])
def workerProfile():

    if session.get('username'):

        user_selected=Worker.query.filter_by(username=session['username']).first()
        worker_role = Role.query.filter_by(id=user_selected.role_id).first()
        id_user = user_selected.id
        user_skills = (db.session.query(Worker,Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).filter(Competence.type == 'Soft skills').all())
        user_skills2 = (db.session.query(Worker,Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).filter(Competence.type == 'Programming').all())
        role_user = (db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Worker.id == id_user).all())
        project_user = (db.session.query(Worker,Project).filter(Project.id == Worker.project_id).filter(Worker.id == id_user).all())
        projects_user = (db.session.query(Project, Project_to_Worker).filter(Project_to_Worker.project_id == Project.id).filter(Project_to_Worker.worker_id == id_user).filter(Project.active == 'N').all())
        myskills = db.session.query(Worker,Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).order_by(Competence.name).all()
        all = db.session.query(Competence, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Competence.id == Competence_to_Worker.competence_id).group_by(Competence.name).order_by(Competence.name).all()
        av = db.session.query(Worker, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).first()

        average = av[2]

        my_evaluations = getting_my_evaluations(user_selected)

        _My = [[],[]]
        _Av = [[],[]]

        for h in myskills:
            _My[0].append(h[1].name) #Skill
            _My[1].append(h[2].score) #Skill

        for s in all:
            if s[0].name in _My[0]:
                _Av[0].append(s[0].name) #Skill
                _Av[1].append(s[2]) #Skill

        print(_My , _Av)

        n_rows = math.ceil(len(user_skills)/4)

        return render_template('gtemplates/index_edited_2.html', user=user_selected, top_4 = top_4skills(id_user),
        skills=user_skills, skills2 = user_skills2, len2 = len(user_skills2), len=len(user_skills), role = role_user[0][1].name, project=project_user,
        average=average, rows=n_rows, projects=projects_user, len_projects=len(projects_user),
        my_evaluations = my_evaluations, len_evaluations = len(my_evaluations), _My = _My[0], _Mys = _My[1],
        _Avs = _Av[1])

    else:
        return redirect('login')

@app.route('/home',methods=['POST','GET'])
def home():

    if session.get('username'):

        user_selected=Worker.query.filter_by(username=session['username']).first()
        worker_role = Role.query.filter_by(id=user_selected.role_id).first()
        id_user = user_selected.id

        if worker_role.name == "HR":

            formRed = WorkerForm()
            formEv = CreateEvaluationForm()

            my_query = db.session.query(Project).all()
            formRed.project.query = my_query
            formEv.project.query = my_query

            my_query2 = db.session.query(Role).all()
            formRed.role.query = my_query2

            my_query3 = db.session.query(Competence).all()

            formRed.soft1.query = my_query3
            formRed.soft2.query = my_query3
            formRed.soft3.query = my_query3
            formRed.soft4.query = my_query3


            projects_pm = db.session.query(Project, Worker, Role,func.count(Role.name)).filter(Project.id == Worker.project_id).filter(Worker.role_id == Role.id).filter(Project.active == 'Y').group_by(Project.id).all()

            total_projects = len(projects_pm)

            workers = db.session.query(Worker).all()
            total_workers = len(workers)

            workersP1 = len(db.session.query(Worker).filter(Worker.plant == 'Plant 1').all())
            workersP2 = len(db.session.query(Worker).filter(Worker.plant == 'Plant 2').all())
            workersP3 = len(db.session.query(Worker).filter(Worker.plant == 'Plant 3').all())

            role_workers = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'Worker').all())
            role_workersP1 = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'Worker').filter(Worker.plant == 'Plant 1').all())
            role_workersP2 = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'Worker').filter(Worker.plant == 'Plant 2').all())
            role_workersP3 = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'Worker').filter(Worker.plant == 'Plant 3').all())


            role_pms = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'PM').all())
            role_pmsP1 = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'PM').filter(Worker.plant == 'Plant 1').all())
            role_pmsP2 = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'PM').filter(Worker.plant == 'Plant 2').all())
            role_pmsP3 = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'PM').filter(Worker.plant == 'Plant 3').all())

            role_hrs = len(db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Role.name == 'HR').all())
            table = overall_competence_table()


            soft_skills = table[0]
            hard_skills = table[1]
            tophard = table[2]
            topsoft = table[3]

            sum_wage = total_wage()
            evaluations = active_evaluations()


            everything = db.session.query(Worker, Role, Project, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Role.id == Worker.role_id).filter(Project.id == Worker.project_id).filter(Worker.id == Competence_to_Worker.worker_id).group_by(Worker.name).all()


            if formRed.validate_on_submit():

                create_worker(formRed.name.data, formRed.first_name.data, formRed.surename.data,
                formRed.date_of_birth.data, formRed.email.data, formRed.mobile.data, formRed.address.data,
                formRed.starting_date.data, formRed.wage.data, formRed.available.data, formRed.username.data,
                formRed.password.data, formRed.role.data, formRed.project.data,formRed.plant.data, formRed.soft1.data,
                formRed.sscore1.data, formRed.soft2.data, formRed.sscore2.data, formRed.soft3.data, formRed.sscore3.data,
                formRed.soft4.data, formRed.sscore4.data)

            elif formEv.validate_on_submit():

                create_evaluation(formEv.name.data, formEv.project.data, formEv.starting_date.data)

            return render_template('gtemplates/hr_index.html', user=user_selected,
            projects_pm = projects_pm, len_projects = total_projects, workers = workers,
            len_workers = total_workers, workersP1 = workersP1, workersP2 = workersP2,
            workersP3 = workersP3, role_workers = role_workers, role_workersP1 = role_workersP1,
            role_workersP2 = role_workersP2, role_workersP3 = role_workersP3, role_pms = role_pms,
            role_pmsP1 = role_pmsP1, role_pmsP2 = role_pmsP2, role_pmsP3 = role_pmsP3,
            role_hrs = role_hrs, softskills = soft_skills, len_softskills = len(soft_skills), hardskills = hard_skills,
            len_hardskills = len(hard_skills), sum_wage = sum_wage, everything = everything, len_everything = len(everything),
            formReg = formRed,
            formEv = formEv, active_evaluations = evaluations, len_active_evaluations = len(evaluations),
            tophard = tophard[0], tophards = tophard[1], topsoft = topsoft[0], topsofts = topsoft[1]
            )


        elif worker_role.name == "PM":

            finishForm = FinishProject()

            project = True
            my_project = db.session.query(Project, Worker, func.count(Worker.project_id)).filter(Project.id == Worker.project_id).filter(Project.id == user_selected.project_id).filter(Project.active == 'Y').filter(Worker.available == 'N').group_by(Project.id).first()
            other_projects = db.session.query(Project, Worker, func.count(Worker.project_id)).filter(Project.id == Worker.project_id).filter(Project.id != user_selected.project_id).filter(Project.active == 'Y').filter(Worker.available == 'N').group_by(Project.id).all()

            my_workers = db.session.query(Worker, Role, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Role.id == Worker.role_id).filter(Worker.id == Competence_to_Worker.worker_id).filter(Worker.project_id == user_selected.project_id).group_by(Worker.name).filter(Worker.available == 'N').all()
            print(my_workers)

            my_past_projects = db.session.query(Project_to_Worker).filter(Project_to_Worker.worker_id == user_selected.id).all()
            my_past_projects_id = []

            for project in my_past_projects:
                my_past_projects_id.append(project.project_id)

            myPP = db.session.query(Project, Project_to_Worker, func.count(Project_to_Worker.worker_id)).filter(Project.id == Project_to_Worker.project_id).filter(Project_to_Worker.project_id.in_(my_past_projects_id)).group_by(Project_to_Worker.project_id).all()

            if not my_project:
                project = False

            if finishForm.validate_on_submit():
                my_project[0].active = 'N'
                db.session.commit()
                db.session.flush()


            return render_template('gtemplates/pm_index.html', user=user_selected, my_project = my_project,
            other_projects = other_projects, len_projects = len(other_projects), my_workers = my_workers,
            len_workers = len(my_workers), myPP = myPP, len_PP = len(myPP), formReg = finishForm, project = project)

        elif worker_role.name == "Worker":

            user_skills = (db.session.query(Worker,Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).filter(Competence.type == 'Soft skills').all())
            user_skills2 = (db.session.query(Worker,Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).filter(Competence.type == 'Programming').all())
            role_user = (db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Worker.id == id_user).all())
            project_user = (db.session.query(Worker,Project).filter(Project.id == Worker.project_id).filter(Worker.id == id_user).all())
            projects_user = (db.session.query(Project, Project_to_Worker).filter(Project_to_Worker.project_id == Project.id).filter(Project_to_Worker.worker_id == id_user).filter(Project.active == 'N').all())
            myskills = db.session.query(Worker,Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).order_by(Competence.name).all()
            all = db.session.query(Competence, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Competence.id == Competence_to_Worker.competence_id).group_by(Competence.name).order_by(Competence.name).all()
            av = db.session.query(Worker, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2)).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).first()

            average = av[2]
            my_evaluations = getting_my_evaluations(user_selected)

            _My = [[],[]]
            _Av = [[],[]]

            for h in myskills:
                _My[0].append(h[1].name) #Skill
                _My[1].append(h[2].score) #Skill

            for s in all:
                if s[0].name in _My[0]:
                    _Av[0].append(s[0].name) #Skill
                    _Av[1].append(s[2]) #Skill

            print(_My , _Av)

            n_rows = math.ceil(len(user_skills)/4)

            return render_template('gtemplates/index_edited_2.html', user=user_selected, top_4 = top_4skills(id_user),
            skills=user_skills, skills2 = user_skills2, len2 = len(user_skills2), len=len(user_skills), role = role_user[0][1].name, project=project_user,
            average=average, rows=n_rows, projects=projects_user, len_projects=len(projects_user),
            my_evaluations = my_evaluations, len_evaluations = len(my_evaluations), _My = _My[0], _Mys = _My[1],
            _Avs = _Av[1])

    else:

        return redirect('login')



def overall_competence_table():
    #[0]: Name of the competence / [1]:Avg / [2]: N_workers
    all_competences = []
    all_sums = []
    all_workers = []

    todas = db.session.query(Competence, Competence_to_Worker).filter(Competence.id == Competence_to_Worker.competence_id).all()

    soft = db.session.query(Competence, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2), func.count(Competence_to_Worker.worker_id)).filter(Competence.type == 'Soft skills').filter(Competence.id == Competence_to_Worker.competence_id).group_by(Competence.name).order_by(func.avg(Competence_to_Worker.score).desc()).all()
    hard = db.session.query(Competence, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2), func.count(Competence_to_Worker.worker_id)).filter(Competence.type == 'Programming').filter(Competence.id == Competence_to_Worker.competence_id).group_by(Competence.name).order_by(func.avg(Competence_to_Worker.score).desc()).all()
    hard_first = db.session.query(Competence, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2), func.count(Competence_to_Worker.worker_id)).filter(Competence.type == 'Programming').filter(Competence.id == Competence_to_Worker.competence_id).group_by(Competence.name).order_by(func.avg(Competence_to_Worker.score).desc()).limit(7)
    soft_first = db.session.query(Competence, Competence_to_Worker, func.round(func.avg(Competence_to_Worker.score),2), func.count(Competence_to_Worker.worker_id)).filter(Competence.type == 'Soft skills').filter(Competence.id == Competence_to_Worker.competence_id).group_by(Competence.name).order_by(func.avg(Competence_to_Worker.score).desc()).limit(7)

    _Hard = [[],[], []]
    _Soft = [[],[], []]

    for h in hard_first:
        _Hard[0].append(h[0].name) #Skill
        _Hard[1].append(h[2]) #Skill

    for s in soft_first:
        _Soft[0].append(s[0].name) #Skill
        _Soft[1].append(s[2]) #Skill

    return soft, hard, _Hard, _Soft


def overall_all():

    new = []
    workers = db.session.query(Worker).all()
    for w in workers:
        user_skills = (db.session.query(Worker,Project,Competence,Competence_to_Worker, Role).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == w.id).filter(Competence.id == Competence_to_Worker.competence_id).filter(Project.id == Worker.project_id).filter(Role.id == Worker.role_id).all())
        user = db.session.query(Worker, Project, Role).filter(Worker.id == w.id).filter(Project.id == Worker.project_id).filter(Worker.role_id == Role.id).all()
        overall = 0
        for skill in user_skills:
            overall += skill[3].score
        overall = round(overall / len(user_skills), 2)
        new.append((user,overall))
    return new


def total_wage():

    all = db.session.query(Worker).all()
    wage = 0
    for w in all:
        wage += w.wage

    return wage


def top_4skills(id_user):

    user_skills = db.session.query(Worker,Project,Competence,Competence_to_Worker, Role).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).filter(Project.id == Worker.project_id).filter(Role.id == Worker.role_id).order_by(Competence_to_Worker.score.desc()).limit(4).all()
    return user_skills


#working
@app.route('/logout')
def logout():
    session.clear() #logout
    return redirect('login')


#working
@app.route('/login',methods=['POST','GET'])
def login():

    formRed = loginForm()

    if session.get('username'):
        return redirect('home')
    else:
        formRed = loginForm()
        if formRed.validate_on_submit():

            user_selected=Worker.query.filter_by(username=formRed.username.data).first()

            if user_selected.password == formRed.password.data:
                session['username']=user_selected.username
                return redirect('home')
        return render_template('gtemplates/login.html', formReg = formRed)


if __name__ == '__main__':
    app.run(debug=True)
