#from forms import LoginForm, regestrationForm, exerciseForm, compForm, reqAdmin, addEx, EditEx, RemoveEx, RemoveUser, nonRequest, profileForm, joinComp, endComp
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint as pp
from flask_bcrypt import Bcrypt
from groupy import attachments
from datetime import datetime
from pprint import pprint
from groupy import Client
import random as rand
from forms import *
import smtplib
import hashlib
import decimal
import random
import time
import json

D=decimal.Decimal
app = Flask(__name__)
app.config['SECRET_KEY'] = '8c97ffcd72439fe7362f78a1f64c8423'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site16.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# from flask import ListConverter
# app.url_map.converters['list'] = ListConverter

###################################################################################################

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    color = db.Column(db.String(), nullable=False)
    phonenumber = db.Column(db.String(), nullable=False)
    pts = db.Column(db.Float, nullable=False, default=0)
    exes = db.Column(db.String(), nullable=False)
    currentView = db.Column(db.String(), nullable=False, default='')
    comps = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean, default=0)
    dark = db.Column(db.Boolean, default=0)
    def __repr__(self):
        return "user: ("+self.username+" / "+self.email+" / "+self.color+")"

class Exes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    mod = db.Column(db.Boolean, default=0)
    uses = db.Column(db.Integer, default=0)
    value = db.Column(db.Float, nullable=False)
    exp = db.Column(db.Integer, default=1, nullable=False)
    desc = db.Column(db.String(), nullable=False)

class Comp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    datePosted = db.Column(db.String(), nullable=False)
    autoRenew = db.Column(db.Boolean, default=0, nullable=False)
    exes = db.Column(db.String(), nullable=False)
    members = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    creator = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(), nullable=False)


###################################################################################################

group = ""
def setGroup(name):
    global group
    groupClient = Client.from_token("KOT8jfdmw8ny42YkOyEE62hiPgkdOWbbD8QZeYu7")
    groups = list(groupClient.groups.list_all())
    for x in groups:
        if(str(x.name) == name):
            group = x

setGroup("Swoll Council")

#group._bots.post("fa19b1e8ca5c87cf923721595a","----INSERT TEXT HERE----")

###################################################################################################

#jU = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\tutorial\\users.json"
usersF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsUsers.json"
exesF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsExes.json"
compsF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsComps.json"
users = []
exes = []
comps = []
testUser = 0
def upVars():
    global comps,users,exes
    with open(exesF, "r") as read_file:
        exes = json.load(read_file)
    with open(compsF, "r") as read_file:
        comps = json.load(read_file)
upVars()
users = []
cUser = {}

def saveVars():
    global comps, exes, compsF, exesF
    with open(exesF, 'w') as outfile:
        json.dump(exes, outfile, indent=4)
    with open(compsF, 'w') as outfile:
        json.dump(comps, outfile, indent=4)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

 
#################################################################################

def addUserToComp(comp):
    if(current_user.id not in json.loads(comp.members)):
        print("No Go")
        #add to user comps
        try:
            tempComps = json.loads(current_user.comps)
        except:
            tempComps = []
        tempComps.append(comp.id)
        current_user.comps=json.dumps(tempComps)
        db.session.commit()

        #add user to members
        compMembers = json.loads(comp.members)
        compMembers.append(current_user.id)
        comp.members=json.dumps(compMembers)
        db.session.commit()

        #add user to content
        cContent = json.loads(comp.content)
        eT = {}
        for e in json.loads(comp.exes):
            eT.update({Exes.query.get(e).name:[0,0]})
        cContent.append({
            'name':current_user.username,
            'pts':0,
            'percent':0,
            'exes':eT
        })
        comp.content=json.dumps(cContent)
        db.session.commit()

        #double check
        for u in User.query.all():
            t = []
            for c in Comp.query.all():
                if(u.id in json.loads(c.members)):
                    t.append(c.id)
            u.comps=json.dumps(t)
            db.session.commit()

    else:
        print(current_user.id)
        print(comp.members)

def genRandom(l):
    lets = "1234567890abcdefghijklmnopqrstuvwxyz"
    tempLoc = ""
    for x in range(l):
        tempLoc+=lets[rand.randint(0,len(lets)-1)]
    return tempLoc

def sendEmail(reciver,subject,body):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login('fastfrisbees@gmail.com','whiteboards')
        sub = subject
        bod = body
        msg = f'Subject: {sub}\n\n{bod}'
        smtp.sendmail('fastfrisbees@gmail.com',reciver,msg)

def getExMod():
    global exes
    t = []
    for e in Exes.query.all():
        if(e.mod==True):
            t.append(e.name)
    return t


def showUserExes():
    global exes
    if(current_user.is_authenticated):
        temp = []
        try:
            c = Comp.query.filter_by(name=current_user.currentView).first()
            for u in json.loads(c.content):
                #pp(u['name'])
                if(u['name']==current_user.username):
                    for e in u['exes']:
                        if(u['exes'][e][0]>0):
                            temp.append([e,  float(int(u['exes'][e][0]*10)/10)  ,  float(int(u['exes'][e][1]*10)/10)  ])
                    #pp(sorted(temp,key=lambda l:l[1], reverse=True))
                    return sorted(temp,key=lambda l:l[2], reverse=True)
        except:
            return []
    else:
        return []

def getExByName(eN):
    for e in range(len(exes)):
        if(exes[e]['name']==eN):
            return e

def genContent(comp):
    contentT = [] 
    for p in json.loads(comp.members):
        eT = {}
        for e in json.loads(comp.exes):
            eT.update({Exes.query.get(e).name:[0,0]})
        contentT.append({
            'name':User.query.get(p).username,
            'pts':0,
            'percent':0,
            'exes':eT
        })
    comp.content=json.dumps(contentT)
    db.session.commit()
    #pp(contentT)

def compsForHome():
    t = []
    for c in Comp.query.all():
        cT = json.loads(c.content)
        cT.sort(key=lambda i:i['pts'], reverse=True)
        t.append({
            'name':c.name,
            'members':json.loads(c.members),
            'datePosted':c.datePosted,
            'goal':c.goal,
            'content':cT,
            'code':c.code
        })
    return sorted(t,key=lambda l:len(l['members']), reverse=True)

def getUserComps():
    cS = json.loads(current_user.comps)
    t = []
    for c in cS:
        t.append(Comp.query.get(c).name)
    return t


###################################################################################################
#In Progress
@app.route('/') 
def home():
    global comps,users,exes,compName, current_user
    if(current_user.is_authenticated==False):
        return redirect(url_for('login'))

    # print(current_user.id)
    # print(Comp.query.get(1).members)
    # print(getUserComps())
    
    try:
        len(request.args.get('type'))
        if(request.args.get('type')!="None"):
            tempName = str(request.args.get('type'))
            if("|" in tempName):
                tempName=tempName.split("|")[0]+" | "+tempName.split("|")[1]
            current_user.currentView = tempName
            db.session.commit()
    except:
        pass
        # if(current_user.currentView==""):
        #     current_user.currentView=Comp.query.get(json.loads(current_user.comps)[0]).name
    db.session.commit()
    try:
        return render_template("home.html", comps=compsForHome(), title='Movement', exes=exes, users=User.query.all(), date=str(datetime.utcnow())[0:str(datetime.utcnow()).index(' ')], exesU=showUserExes(), userComps=getUserComps(),compN=request.args.get('compN'))
    except:
        return render_template("home.html", comps=compsForHome(), title='Movement', exes=exes, users=User.query.all(), date=str(datetime.utcnow())[0:str(datetime.utcnow()).index(' ')])#, exesU=showUserExes(current_user.currentView), userComps=json.loads(current_user.comps))

###################################################################################################


#Done
@login_required
@app.route('/exercises', methods=['GET', 'POST']) 
def exercises():
    global comps,users,exes, D
    if(current_user.is_authenticated==False):
        return redirect(url_for('login'))
    form = exerciseForm()
    upVars()
    compsInText = ""
    if form.validate_on_submit():
        user = current_user
        for c in Comp.query.all():
            if(user.id in json.loads(c.members)):
                if(Exes.query.filter_by(name=form.exercise.data).first().id in json.loads(c.exes)):
                    print(c.name)
                    compsInText+=c.name+", "
                    for p in json.loads(c.content):
                        if(p['name']==user.username):
                            userExes = p['exes']
                            if(Exes.query.filter_by(name=form.exercise.data).first().mod==False):
                                userExes[form.exercise.data][0]+= float(int(form.qty.data*100))/100
                                userExes[form.exercise.data][1]+= float(int((form.qty.data*Exes.query.filter_by(name=form.exercise.data).first().value)*100))/100
                            else:
                                userExes[form.exercise.data][0]+= float(int(form.qty.data*100))/100
                                userExes[form.exercise.data][1]+= float(int((form.qty.data*(form.weight.data*Exes.query.filter_by(name=form.exercise.data).first().value))*100))/100
                            tempContent = json.loads(c.content)
                            for u in tempContent:
                                if(u['name']==user.username):
                                    u['exes']=userExes
                            c.content=json.dumps(tempContent)
                            db.session.commit()
                            tempContent = []
                            for p in json.loads(c.content):
                                p['pts']=0
                                for e in p['exes']:
                                    p['pts']+=  float(int(p['exes'][e][1]*10)/10)
                                    p['percent']= round(float(int(((p['pts']/c.goal)*100)*10)/10),2)
                                tempContent.append(p)
                            c.content=json.dumps(tempContent)
                            #CHECK COMPS %AGES
                            for u in User.query.all():
                                t = []
                                for c in Comp.query.all():
                                    if(u.id in json.loads(c.members)):
                                        t.append(c.id)
                                u.comps=json.dumps(t)
                            db.session.commit()
                            break
        if(form.qty.data>0):
            Exes.query.filter_by(name=form.exercise.data).first().uses+=1
            db.session.commit()
        if(compsInText[-2]==","):
            compsInText=compsInText[:-2]
        flash('Sucessful logged '+str(form.qty.data)+' of '+form.exercise.data+' for '+user.username+' for '+compsInText,'success')
        news = []
        olds = []
        for c in Comp.query.all():
            for u in json.loads(c.content):
                if(u['pts']>=c.goal):
                    if(c.autoRenew):
                        c_2 = Comp(
                            name=c.name.split(" | ")[0]+" | "+str(int(c.name.split(" | ")[1])+1),
                            goal=c.goal,
                            autoRenew=c.autoRenew,
                            members=c.members,
                            exes=c.exes,
                            datePosted=str(datetime.utcnow())[0:str(datetime.utcnow()).index(' ')],
                            content='',
                            code=c.code,
                            creator=c.creator
                        )
                        genContent(c_2)
                        news.append(c_2)    

                    #########SEND RECAP EMAIL###########

                    # for m in json.loads(c.content):
                    #     placeT = sorted(json.loads(c.content),key=lambda l:l['pts'], reverse=True).index(m)+1
                    #     if(placeT>1):
                    #         sendEmail(
                    #             reciver=User.query.filter_by(username=m['name']).first().email,
                    #             subject=c.name+" Has Ended!",
                    #             body=f"The competition {c.name} has been completed, here is your recap. The winner is {u['name']}, and you got {m['percent']}%, your place was {placeT}. Well Done!"
                    #             )     
                    #     else:  
                    #         sendEmail(
                    #             reciver=User.query.filter_by(username=m['name']).first().email,
                    #             subject=c.name+" Has Ended! You Won!",
                    #             body=f'The competition {c.name} has been completed, you Won!'
                    #         )     

                    ####################################              
                    olds.append(c)                    
                    break

        for c in news:
            db.session.add(c)
            db.session.commit()
        for c in olds:
            db.session.delete(c)
            db.session.commit()

        for u in User.query.all():
            t = []
            for c in Comp.query.all():
                if(u.id in json.loads(c.members)):
                    t.append(c.id)
            u.comps=json.dumps(t)
            db.session.commit()

        if(form.submitL.data==True):
            return redirect(url_for('home'))
        elif(form.submitF.data==True):
            return redirect(url_for('exercises'))  


    return render_template("exercises.html",exes=exes, title='Log Exercise',form=form,users=User.query.all(), exesU=showUserExes(), exesMod=getExMod(), userComps=getUserComps())


#Done
@app.route('/exerciseData', methods=['GET', 'POST']) 
def exerciseData():
    global comps,users,exes
    if(current_user.is_authenticated==False):
        return redirect(url_for('login'))
    upVars()
    form = nonRequest()
    if form.validate_on_submit():
        message = "A Plebe has requested that we add "+form.name.data+". Their provided description is as follows: \""+form.desc.data+"\". They propose it be worth "+str(form.val.data)+" pts. If this message is liked by a majority of the council it will be added."
        group._bots.post("fa19b1e8ca5c87cf923721595a",message)
    return render_template("requests.html",exes=exes, title='Exercise Data', users=User.query.all(), form=form, exesU=showUserExes(),Exes=Exes, userComps=getUserComps())

################################################################################################

@app.route('/register', methods=['GET', 'POST']) 
def register():
    global comps,users,exes, current_user
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    upVars()
    formR = regestrationForm()
    if formR.validate_on_submit():
        if(len(User.query.filter_by(email=formR.email.data).all())>0):
            flash('Email is already in use','danger')
            return redirect(url_for('register'))
        if(len(User.query.filter_by(username=formR.username.data).all())>0):
            flash('Username is already in use','danger')
            return redirect(url_for('register'))

        exesT = '{'
        for e in Exes.query.all():
            exesT+= "\""+e.name+"\"" +':'+ "[0,0]" +','
        exesT=exesT[:-1]+"}"

        user_1 = User(
            username=formR.username.data,
            email = formR.email.data,
            password = bcrypt.generate_password_hash(formR.password.data).decode('utf-8'),
            color = request.form.get('color', ''),
            phonenumber = formR.phone.data,
            exes = '',
            currentView='',
            comps = '',
            admin=False,
            dark=False
        )
        db.session.add(user_1)
        db.session.commit()

        flash('Your account has been created!','success')
        return redirect(url_for('login'))
    try:
        return render_template("register.html", title='register',formR=formR,users=User.query.all(), exesU=showUserExes(), userComps=getUserComps())
    except:
        return render_template("register.html", title='register',formR=formR,users=User.query.all(), exesU=showUserExes())#, userComps=json.loads(current_user.comps))

@app.route('/login', methods=['GET', 'POST']) 
def login():
    global comps,users,exes
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    upVars()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user,remember=form.remember.data)
            print(current_user)
            for c in Comp.query.all():
                if('Global |' in c.name):
                    addUserToComp(c)
                    break

            flash('Logged in as '+current_user.username,'success')
            return redirect(url_for('home'))
        else:
            pass
            flash('Incorrect email or password','danger')

    #print(bcrypt.check_password_hash(pw_hash, 'hunter2'))
    try:
        return render_template("login.html",exes=exes, title='about', users=User.query.all(), form=form, exesU=showUserExes(), userComps=json.loads(current_user.comps))
    except:
        return render_template("login.html",exes=exes, title='about', users=User.query.all(), form=form, exesU=showUserExes())


@login_required
@app.route('/profile', methods=['GET', 'POST']) 
def profile():
    if(current_user.is_authenticated==False):
        return redirect(url_for('login'))
    form = profileForm()
    if form.validate_on_submit():
        if(bcrypt.check_password_hash(current_user.password, form.cPassword.data)):
            # if(len(form.username.data)>0):
            #     if(len(User.query.filter_by(username=form.username.data).all())==0):
            #         current_user.username=form.username.data
            #         db.session.commit()
            #         flash('changed username to: '+form.username.data, 'success')
            if(len(form.password.data)>0):
                current_user.password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                db.session.commit()
                flash('Changed password', 'success')
        else:
            if(len(form.password.data)>0):
                flash('Incorrect password!','danger')
        if(request.form.get('color', '')!="#000000"):
            current_user.color=request.form.get('color', '')
            db.session.commit()
            flash('changed color to: : '+request.form.get('color', ''),'success')
        current_user.dark=form.dark.data
        db.session.commit()
    return render_template("profile.html",exes=exes, title='Profile', users=User.query.all(), form=form, exesU=showUserExes(), userComps=getUserComps())

@app.route('/logout') 
def logout():
    global comps,users,exes
    logout_user()
    return redirect(url_for('login'))


################################################################################################

#Done
@app.route('/usersdata') 
def usersdata():
    global comps,users,exes
    if(current_user.is_authenticated==False):
        return redirect(url_for('login'))
    upVars()

    fullBigger = []
    full2dForm = []
    for c in Comp.query.all():
        full2dForm = []
        temp = ["Name"]
        for e in json.loads(c.content)[0]['exes']:
            temp.append(e)
        full2dForm.append(temp)
        for u in json.loads(c.content):
            eT = u['exes']
            temp=[u['name']]
            for e in eT:
                temp.append(u['exes'][e][1])
            full2dForm.append(temp)
        fullBigger.append([c.name,full2dForm])
    return render_template("friends.html",exes=exes, full2dForm=full2dForm, title='Users',users=User.query.all(), exesU=showUserExes(), userComps=getUserComps(), fullBigger=fullBigger)


#Done
@app.route('/about') 
def about():
    global comps,users,exes
    upVars()
    return render_template("about.html",exes=exes, title='about',users=User.query.all(), exesU=showUserExes(), userComps=json.loads(current_user.comps))


#Done
@app.route('/about/faqs') 
def faqs():
    return render_template("faqs.html",exes=exes, title='about',users=User.query.all(), exesU=showUserExes(), userComps=json.loads(current_user.comps))


#Done
@app.route('/about/rules') 
def rules():
    return render_template("rules.html",exes=exes, title='about',users=User.query.all(), exesU=showUserExes(), userComps=json.loads(current_user.comps))

###################################################################################################

#Not for α
@app.route('/stats') 
def stats():
    global comps,users,exes
    upVars()
    return render_template("about.html",exes=exes, title='about',users=User.query.all(), exesU=showUserExes(), userComps=json.loads(current_user.comps))


@app.route('/start', methods=['GET', 'POST']) 
def start():
    global comps,users,exes
    if(current_user.is_authenticated==False):
        return redirect(url_for('login'))
    upVars()
    form = compForm(prefix='startNew')
    if form.validate_on_submit():
        peopleC = []
        for p in form.people.data:
            peopleC.append(User.query.filter_by(username=p).first().id)
        exesC = []
        for e in form.exercises.data:
            exesC.append(Exes.query.filter_by(name=e).first().id)

        if(form.autoRenew.data):
            nameT = form.name.data.replace(" ","_")+" | 0"
        else:
            nameT = form.name.data.replace(" ","_")
        c_1 = Comp(
            name=nameT,
            goal=form.goal.data,
            autoRenew=form.autoRenew.data,
            members=json.dumps(peopleC),
            exes=json.dumps(exesC),
            datePosted=str(datetime.utcnow())[0:str(datetime.utcnow()).index(' ')],
            content='',
            code=str(genRandom(8)),
            creator=int(current_user.id)
        )
        db.session.add(c_1)
        for u in User.query.all():
            t = []
            for c in Comp.query.all():
                if(u.id in json.loads(c.members)):
                    t.append(c.id)
            u.comps=json.dumps(t)
        db.session.commit()
        genContent(c_1)
        flash('Created new competition: '+c_1.name,'success')
        return redirect(url_for('home'))

    formJ = joinComp(prefix='joinComp')
    if formJ.validate_on_submit():
        for c in Comp.query.all():
            if(formJ.code.data==c.code):
                addUserToComp(c)
                flash('Youve been added to '+c.name,'success')
                break

    formD = endComp(prefix='endComp')
    if formD.validate_on_submit():
        for c in Comp.query.all():
            if(formD.code.data==c.code):
                if(current_user.admin==True or current_user.id==c.creator):
                    for u in User.query.all():
                        uComps = json.loads(u.comps)
                        try:
                            uComps.remove(c.id)
                        except:
                            pass
                        u.comps=json.dumps(uComps)
                    db.session.delete(c)
                    db.session.commit()
                    flash('Deleted Competition','success')
    try:
        return render_template("start.html",exes=exes, title='about', form=form, formJ=formJ, formD=formD, users=users, userComps=getUserComps())
    except:
        return render_template("start.html",exes=exes, title='about', form=form, formJ=formJ, formD=formD, users=users)#,  userComps=getUserComps())


##################################################################################################
#ADMIN


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global comps,users,exes,exesF,usersF,compsF
    if(current_user.is_authenticated==False):
        return redirect(url_for('login'))
    upVars()
    if(current_user.admin == False):
        return redirect(url_for('home'))
    formExMod = addEx(prefix="formExMod")
    formComp = compForm(prefix="formComp")
    formExModR = EditEx(prefix="formExModR")
    formRU = RemoveUser(prefix="formRU")
    formREX = RemoveEx(prefix="formREX")

    #ADD EXERCISE
    if formExMod.validate_on_submit():
        print("ADDED EXERCISE")
        if(formExMod.mod.data == False):
            e_1 = Exes(
                name=formExMod.newName.data,
                mod=False,
                value=formExMod.val.data,
                desc=formExMod.desc.data
            )
            db.session.add(e_1)
            db.session.commit()
        else:
            e_1 = Exes(
                name=formExMod.newName.data,
                mod=True,
                value=formExMod.val.data,
                desc=formExMod.desc.data
            )
            db.session.add(e_1)
            db.session.commit()
        
        for c in Comp.query.all():
            if("Global |" in c.name):
                cContent = json.loads(c.content)
                for u in cContent:
                    u['exes'].update({e_1.name:[0,0]})
                cExes = json.loads(c.exes)
                cExes.append(e_1.id)
                c.exes=json.dumps(cExes)
                c.content=json.dumps(cContent)
                db.session.commit()
                break
        
        saveVars()
        db.session.commit()

    #MODIFIY EXERCISE
    if formExModR.validate_on_submit():
        print("MODIFIED EXERCISE")
        e = Exes.query.filter_by(name=formExModR.exercise.data).first()
        if(len(str(formExModR.val.data))>0):
            e.value=formExModR.val.data
        db.session.commit()

    #REMOVE USER
    if formRU.validate_on_submit():
        print("REMOVED USER")
        user = User.query.filter_by(username=formRU.userR.data).first()

        for c in Comp.query.all():
            if(user.id in json.loads(c.members)):
                cMembers = json.loads(c.members)
                cMembers.remove(user.id)
                c.members=json.dumps(cMembers)
                cContent = json.loads(c.content)
                for u in cContent:
                    if(u['name']==user.username):
                        cContent.remove(u)
                        break
                c.content=json.dumps(cContent)
                db.session.commit()

        db.session.delete(user)
        db.session.commit()

    print("ADD WSGI UPDATER")
    return render_template("adminPage.html",exes=exes, title='ADMIN PAGE',users=users, formExMod=formExMod, formComp=formComp, formExModR=formExModR, formRU=formRU, formREX=formREX, exesU=showUserExes(), userComps=getUserComps())




@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        traits = []
        try:
            for x in range(0,100):
                traits.append(request.form[str(x)])
        except:
            pass
        print(traits)

    return render_template('table.html')



###################################################################################################

if __name__ == "__main__":
    app.run(debug=True)



