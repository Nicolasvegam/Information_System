from flask import Flask,render_template,redirect,session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import exc
import math


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


from form import loginForm, WorkerForm

# Creating fake real data

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
        wage = 100000, available = 'Y', username='nicovega',password='1234567', role_id = worker_role.id, project_id = new_project.id, plant = 'Plant 1')

        pm_user = Worker(name='Juan Pablo Fernandez', first_name = 'Juan', surename = 'Fernandez', date_of_birth= '23/05/1987',
        email = 'jpfernadez@uc.cl', mobile = '847839848', address = 'via Ferruci 34', starting_date = '08/09/2000',
        wage = 150000, available = 'Y', username='jpfernandez',password='1234567', role_id = worker_role2.id, project_id = new_project.id, plant = 'Plant 1')

        hr_user = Worker(name='Jose Vila', date_of_birth= '23/07/1967', first_name = 'Jose', surename = 'Vila',
        email = 'josevila@uc.cl', mobile = '938474943', address = 'Corso di Duca 45', starting_date = '12/11/2009',
        wage = 170000, available = 'Y', username='josevila',password='1234567', role_id = worker_role3.id, project_id = new_projectHR.id, plant = 'Plant 2')

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

        db.session.add(new_competence)
        db.session.add(new_competence2)
        db.session.add(new_competence3)
        db.session.add(new_competence4)
        db.session.add(new_competence5)
        db.session.add(new_competence6)


        db.session.flush()

        r_competence_worker = Competence_to_Worker(competence_id = new_competence.id, worker_id = w_user.id, score = 78)
        r_competence_worker2 = Competence_to_Worker(competence_id = new_competence2.id, worker_id = w_user.id, score = 86)
        r_competence_worker3 = Competence_to_Worker(competence_id = new_competence4.id, worker_id = w_user.id, score = 57)
        r_competence_worker10 = Competence_to_Worker(competence_id = new_competence3.id, worker_id = w_user.id, score = 57)
        r_competence_worker13 = Competence_to_Worker(competence_id = new_competence5.id, worker_id = w_user.id, score = 70)
        r_competence_worker14 = Competence_to_Worker(competence_id = new_competence6.id, worker_id = w_user.id, score = 99)

        r_competence_worker4 = Competence_to_Worker(competence_id = new_competence.id, worker_id = pm_user.id, score = 65)
        r_competence_worker5 = Competence_to_Worker(competence_id = new_competence2.id, worker_id = pm_user.id, score = 45)
        r_competence_worker6 = Competence_to_Worker(competence_id = new_competence4.id, worker_id = pm_user.id, score = 80)
        r_competence_worker11 = Competence_to_Worker(competence_id = new_competence3.id, worker_id = pm_user.id, score = 57)

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


        new_evaluation = Evaluation( id_worker = w_user.id, id_worker_ev = pm_user.id, id_project = new_project.id, date = '21/01/2020', active = 'N')
        new_evaluation2 = Evaluation( id_worker = pm_user.id, id_worker_ev = w_user.id, id_project = new_project.id, date = '21/01/2020', active = 'N')

        db.session.add(new_evaluation)
        db.session.add(new_evaluation2)
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

##############################

@app.route('/')
@app.route('/home')
@app.route('/index')
@app.route('/main')
def home():

    if session.get('username'):
        user_selected=Worker.query.filter_by(username=session['username']).first()
        worker_role = Role.query.filter_by(id=user_selected.role_id).first()
        id_user = user_selected.id

        if worker_role.name == "HR":

            formRed = WorkerForm()
            my_query = db.session.query(Project).all()
            formRed.project.query = my_query
            my_query2 = db.session.query(Role).all()
            formRed.role.query = my_query2

            if formRed.validate_on_submit():

                user_selected=Worker.query.filter_by(username=formRed.username.data).first()

                if user_selected.password == formRed.password.data:
                    session['username']=user_selected.username


            projects = db.session.query(Project).filter(Project.active == 'Y').all()
            total_projects = len(projects)

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

            skills_table = overall_competence_table()
            sum_wage = total_wage()
            overall_all()

            return render_template('gtemplates/hr_index.html', user=user_selected,
            projects = projects, len_projects = total_projects, workers = workers,
            len_workers = total_workers, workersP1 = workersP1, workersP2 = workersP2,
            workersP3 = workersP3, role_workers = role_workers, role_workersP1 = role_workersP1,
            role_workersP2 = role_workersP2, role_workersP3 = role_workersP3, role_pms = role_pms,
            role_pmsP1 = role_pmsP1, role_pmsP2 = role_pmsP2, role_pmsP3 = role_pmsP3,
            role_hrs = role_hrs, skills_table = skills_table, len_skills = len(skills_table),
            sum_wage = sum_wage, everything = overall_all(), formReg = formRed)


        elif worker_role.name == "PM":
            return render_template('gtemplates/pm_index.html', user=user_selected)

        elif worker_role.name == "Worker":

            user_skills = (db.session.query(Worker,Competence, Competence_to_Worker).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == id_user).filter(Competence.id == Competence_to_Worker.competence_id).all())
            role_user = (db.session.query(Worker,Role).filter(Role.id == Worker.role_id).filter(Worker.id == id_user).all())
            project_user = (db.session.query(Worker,Project).filter(Project.id == Worker.project_id).filter(Worker.id == id_user).all())
            projects_user = (db.session.query(Project, Project_to_Worker).filter(Project_to_Worker.project_id == Project.id).filter(Project_to_Worker.worker_id == id_user).filter(Project.active == 'N').all())
            my_evaluations = (db.session.query(Evaluation, Project, Worker).filter(Evaluation.id_project == Project.id).filter(Worker.id == id_user).filter(Project.active == 'N').filter(Evaluation.id_worker == id_user).all())
            print(my_evaluations)
            average = overall(user_skills)
            n_rows = math.ceil(len(user_skills)/4)

            return render_template('gtemplates/index_edited_2.html', user=user_selected, top_4 = top_4(user_skills), skills=user_skills, len=len(user_skills), role = role_user[0][1].name, project=project_user, average=average, rows=n_rows, projects=projects_user, len_projects=len(projects_user))

    else:

        return redirect('login')


def overall_competence_table():
    #[0]: Name of the competence / [1]:Avg / [2]: N_workers
    all_competences = []
    all_sums = []
    all_workers = []

    todas = db.session.query(Competence, Competence_to_Worker).filter(Competence.id == Competence_to_Worker.competence_id).all()

    for t in todas:
        if t[0].name not in all_competences:
            all_competences.append(t[0].name)
            all_sums.append(t[1].score)
            all_workers.append(1)
        else:
            index = all_competences.index(t[0].name)
            all_sums[index] += t[1].score
            all_workers[index] += 1

    #print(str(all_competences) + '\n' + str(all_sums) + '\n' + str(all_workers))
    final_table = []
    for i in range(0, len(all_competences)):
        final_table.append([all_competences[i], all_sums[i]/all_workers[i], all_workers[i]])

    return final_table


def overall(user_skills):

    overall = 0
    for skill in user_skills:
        overall += skill[2].score
    overall = overall / len(user_skills)
    return overall

def overall_all():

    new = []
    workers = db.session.query(Worker).all()
    for w in workers:
        user_skills = (db.session.query(Worker,Project,Competence,Competence_to_Worker, Role).filter(Competence_to_Worker.worker_id == Worker.id).filter(Worker.id == w.id).filter(Competence.id == Competence_to_Worker.competence_id).filter(Project.id == Worker.project_id).filter(Role.id == Worker.role_id).all())
        user = db.session.query(Worker, Project, Role).filter(Worker.id == w.id).filter(Project.id == Worker.project_id).filter(Worker.role_id == Role.id).all()
        overall = 0
        for skill in user_skills:
            overall += skill[3].score
        overall = overall / len(user_skills)
        new.append((user,overall))
    return new

def total_wage():

    all = db.session.query(Worker).all()
    wage = 0
    for w in all:
        wage += w.wage

    return wage


def top_4(user_skills):

    matches = []
    best_one = 0
    for i in range(0,4):
        select_one = None
        for element in user_skills:
            if element[2].score > best_one and element not in matches:
                select_one = element
        matches.append(select_one)

    return matches

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

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run()
