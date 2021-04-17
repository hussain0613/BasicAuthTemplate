from app import engine, Session, User

#User.drop_table(engine)
#User.create_table(engine)

#s = Session()
#user = User.get_user_by(s,username="matha")
#print(user)
#user.save(Session.object_session(user))
u2 = User(username="not_matha", email = "not_matha@mail.com")

if(Session.object_session(u2)):
    u2.save(Session.object_session(u2))
else:
    u2.save(Session())

print(User.get_all(Session()))