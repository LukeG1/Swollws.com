# from forms import User, Exes, Comp, db
# #from flaskSwoll import User, Exes, Comp, db
# import random
# import json
# usersF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsUsers.json"
# exesF = "C:\\Users\\lmgab\\PycharmProjects\\tensorenv\\webDevolpment\\MovementBeta\\formatingTestsExes.json"

# with open(usersF, "r") as read_file:
#     users = json.load(read_file)
# with open(exesF, "r") as read_file:
#     exes = json.load(read_file)

import math
def calcEq(num,eq):
    t = 0
    c1 = len(eq)-1
    for c in eq:
        t+=c*(math.pow(num, c1  ))
        c1-=1
    return t
    
eq1 = [1,0]
print(calcEq(
    num=1,
    eq=eq1
))




# for c in Comp.query.all():
#     db.session.delete(c)
#     db.session.commit()
# for c in Exes.query.all():
#     db.session.delete(c)
#     db.session.commit()
# for c in User.query.all():
#     db.session.delete(c)
#     db.session.commit()
# for u in User.query.all():
#     if('new' in u.username):
#         print(u.username)
#         db.session.delete(u)
#         db.session.commit()

# db.create_all()

# for u in users:
#     user_1 = User(
#         username=u['usermame'],
#         email = u['email'],
#         password = u['password'],
#         color = u['color'],
#         phonenumber = u['phonenumber'],
#         exes = '',
#         currentView='',
#         comps = '',
#         admin=False,
#         dark=False
#     )
#     db.session.add(user_1)
#     db.session.commit()

# for e in exes[:-2]:
#     if(e['mod'] == False):
#         e_1 = Exes(
#             name=e['name'],
#             mod=False,
#             value=e['value'],
#             desc=e['desc']
#         )
#         db.session.add(e_1)
#         db.session.commit()
#     else:
#         e_1 = Exes(
#             name=e['name'],
#             mod=True,
#             value=e['eq'],
#             desc=e['desc']
#         )
#         db.session.add(e_1)
#         db.session.commit()

# User.query.filter_by(email='lmgabel@gmail.com').first().admin=True
# User.query.filter_by(email='wpdtjr@gmail.com').first().admin=True
# db.session.commit()
# for u in User.query.all():
#     if(u.admin):
#         print(u)

# def genRandom(l):
#     lets = "1234567890abcdefghijklmnopqrstuvwxyz"
#     tempLoc = ""
#     for x in range(l):
#         tempLoc+=lets[random.randint(0,len(lets)-1)]
#     return tempLoc

# for c in Comp.query.all():
#     c.code = genRandom(8)
#     db.session.commit()

#print(Comp.query.all())

# for e in Exes.query.all():
#     print(e.name)


# for e in Exes.query.all():
#     if('Test' in e.name or 'test' in e.name):
#         print(e.name)
#         db.session.delete(e)
#         db.session.commit()