from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, length, Email, EqualTo
import json
from flaskSwoll import User, Exes, Comp, db

choices = [('situps','Situps'),('pushups','Pushups'),('pullups','Pullups'),('lunges','Lunges'),('walking','Walking'),('running','Running'),('swimming','Swimming'),('curls','Curls'),('squat','Squat'),('plank(60s)','plank(60s)'),('plank(120s)','plank(120s)'),('curl(10lbs)','curl(10lbs)'),('curl(15lbs)','curl(15lbs)'),('curl(20lbs)','curl(20lbs)'),('curl(25lbs)','curl(25lbs)'),('curl(30lbs)','curl(30lbs)')]
members = [('Luke','Luke'),('DuBose','DuBose'),('Andrew','Andrew'),('Nico','Nico'),('Molly','Molly'),('Ava','Ava'),('Caroline','Caroline'),('Olivia','Olivia'),('Jack C','Jack C'),('Sydney','Sydney')]


usersF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsUsers.json"
exesF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsExes.json"
compsF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsComps.json"
users = []
exes = []
comps = []
def upVars():
    global comps,users,exes
    with open(usersF, "r") as read_file:
        users = json.load(read_file)
    with open(exesF, "r") as read_file:
        exes = json.load(read_file)
    with open(compsF, "r") as read_file:
        comps = json.load(read_file)
upVars()


class test:
    def getExes(self):
        return choices
    def getPeople(self):
        return members

class LoginForm(FlaskForm):
    upVars()
    email = StringField('email')
    password = PasswordField('Password')
    remember = BooleanField('remember me')
    submit = SubmitField('Log in')

class regestrationForm(FlaskForm):
    upVars()
    username = StringField('username',validators=[DataRequired(), length(min=2,max=20)])
    email = StringField('email',validators=[DataRequired(), Email()])
    phone = StringField('phone number')
    color = StringField('Enter your color')
    password = PasswordField('password', validators=[DataRequired()])
    passwordConfirm = PasswordField('passwordConfirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('sign up')

class exerciseForm(FlaskForm):
    exerciseNames = []
    for e in Exes.query.all():
        exerciseNames.append((e.name,e.name))
    exercise = SelectField('What exercise do you want to add?', choices=exerciseNames)
    qty = FloatField('Quantity', validators=[DataRequired()])
    weight = FloatField('Modifier, (lbs, seconds, etc.)',default=0)
    submitL = SubmitField('Done',id='1')
    submitF = SubmitField('Send Another Exercise',id='2')

class compForm(FlaskForm):
    userNames = []
    for u in User.query.all():
        userNames.append((u.username,u.username))
    exerciseNames = []
    for e in Exes.query.all():
        exerciseNames.append((e.name,e.name))
    people = SelectMultipleField('What people do you want to compete with?', choices=userNames)
    exercises = SelectMultipleField('What exercises do you want to compete in?', choices=exerciseNames)
    autoRenew = BooleanField('Should this comp renew when someone wins? If so dont put a number at the end')
    goal = FloatField('Goal')
    name = StringField('Name')
    submit = SubmitField('Start!')

class reqAdmin(FlaskForm):
    upVars()
    pas = StringField('Enter the admin password to edit exercises')
    submit = SubmitField('confirm admin')

class addEx(FlaskForm):
    upVars()
    newName = StringField('what is this exercise called?')
    mod = BooleanField('Does this exercise require a modifier?')
    val = FloatField('what is it worth, or what is its slope?')
    desc = StringField('Enter the description of the new exercise')
    pas = PasswordField('Enter the administrator password')
    submit = SubmitField('Confirm new exercise')

class EditEx(FlaskForm):
    upVars()
    exerciseNames = []
    for e in Exes.query.all():
        exerciseNames.append((e.name,e.name))
    exercise = SelectField('What exercise do you want to modifiy?', choices=exerciseNames)
    #desc = StringField('Enter the new description, or leave blank')
    val = FloatField('Enter the new Value, or leave blank')
    submit = SubmitField('Confirm edits')

class RemoveEx(FlaskForm):
    upVars()
    exerciseNames = []
    for e in exes:
        exerciseNames.append((e['name'],e['name']))
    exercise = SelectField('What exercise do you want to Remove?', choices=exerciseNames)
    submit = SubmitField('Confirm removal')

class RemoveUser(FlaskForm):
    upVars()
    userNames = []
    for u in User.query.all():
        userNames.append((u.username,u.username))
    userR = SelectField('who would you like to remove?', choices=userNames)
    submit = SubmitField('Confirm removal')

class nonRequest(FlaskForm):
    upVars()
    name = StringField("Enter the name of the proposed exercise")
    val = FloatField("Enter the proposed Value")
    desc = StringField("Enter a short description")
    submit = SubmitField('Submit Request')

class profileForm(FlaskForm):
    upVars()
    cPassword = PasswordField('Current password')
    #username = StringField('New username')
    password = PasswordField('New password')
    dark = BooleanField('Would you like to use dark mode?')
    submit = SubmitField('submit')

class joinComp(FlaskForm):
    code = StringField('Enter the competition code')
    submit = SubmitField('submit')

class endComp(FlaskForm):
    code = StringField('Enter the competition code, you must be the creator or an admin.')
    submit = SubmitField('submit')