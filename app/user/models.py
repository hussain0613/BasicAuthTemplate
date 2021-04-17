from __future__ import annotations

import sqlalchemy as sa
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
from . import Base

from sqlalchemy.ext.hybrid import hybrid_property

import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired

import re

from .utils import naming_convention

#Base = declarative_base(metadata=sa.MetaData(naming_convention=naming_convention))

class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key = True, autoincrement=True)
    _name = sa.Column("name", sa.String(200))
    _username = sa.Column("username",sa.String(200), unique=True)
    _email = sa.Column("email", sa.String(200), unique = True)
    
    _password = sa.Column("password", sa.String(300))

    _role = sa.Column("role", sa.String(50), server_default = "guest")

    created = sa.Column(sa.TIMESTAMP(timezone=True), server_default = sa.func.now())
    created_by = sa.Column(sa.Integer, sa.ForeignKey(f"{__tablename__}.id"))
    last_modified = sa.Column(sa.TIMESTAMP(timezone=True), server_default = sa.func.now(), server_onupdate=sa.func.now())
    last_modified_by = sa.Column(sa.Integer, sa.ForeignKey(f"{__tablename__}.id"))

    @hybrid_property
    def name(self) -> str:
        return self._name
    
    @hybrid_property
    def username(self) -> str:
        return self._username
    
    @hybrid_property
    def email(self) -> str:
        return self._email
    
    @hybrid_property
    def password(self) -> str:
        return self._password
    @hybrid_property
    def role(self) -> str:
        return self._role
    
    
    @name.setter
    def name(self, name:str):
        if(re.match("^[a-zA-Z0-9 -]{1,200}$", name)):
            self._name = name
        else:
            raise BaseException(f"name '{name}' got invalid charecter")
    @username.setter
    def username(self, username:str):
        if(re.match("^[a-zA-Z0-9_.]{1,200}$", username)):
            self._username = username
        else:
            raise TypeError(f"username '{username}' got invalid charecter")
    @email.setter
    def email(self, email:str):
        if(re.match("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+$", email)):
            self._email = email
        else:
            raise TypeError(f"email '{email}' got invalid charecter")
    @password.setter
    def password(self, password:str):
        if(re.match("^[a-zA-Z0-9_ -]{8,200}$", password)):
            self._password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        else:
            raise TypeError(f"invalid password. password must be at least 8 characters long and can have only alphanumeric characters and <space>,<.> and <->")
    @role.setter
    def role(self, role:str):
        if(re.match("^[a-zA-Z0-9_-]{1,50}$", role)):
            self._role = role
        else:
            raise TypeError(f"role '{role}' got invalid charecter")

    #@username.setter
    def set_username(self, username:str, password):
        if(self.check_password(passowrd)):
            #if(re.match("^[a-zA-Z0-9_.]{1,200}$", username)):
            #    self._username = username
            #    return {"Message": "username updated successfully, in queue for storage"}
            #else:
            #    return {"Message": "Invalid username format!"}
            self.username = username
        else:
            return {"Message": "Wrong password"}
        
    #@email.setter
    def set_email(self, email:str, passowrd:str):
        if(self.check_password(passowrd)):
        #    if(re.match("^[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+$", email)):
        #        self._email = email
        #        return {"Message": "email updated successfully, in queue for storage"}
        #    else:
        #        return {"Message": "Invalid email format!"}
            self.email = email
        else:
            return {"Message": "Wrong password"}
    #@password.setter
    #def _set_password(self, new_password:str):
    #    if re.match("^[a-zA-Z0-9_ -]{8,200}$", new_password):
    #        self._password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    #        return {"Message": "passowrd updated, in queue for saving"}
    #    else:
    #        return {"Message": "invalid charecter in password"}

    def set_password(self, new_password:str, old_password:str):
        if self.check_password(old_password):
            #return self._set_passowrd(new_password)
            self.password = new_password
        else:
            return {"Message": "Wrong old password"}
    

    def check_password(self, password:str) -> bool:
        #bcrypt.checkpw(pass, hashed_pass)
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def save(self, session):
        self.session = session
        try:
            session.add(self)
            session.commit()
            return {"Message": f"Information updated succesfully for user '{self.username}'"}
        except sa.exc.IntegrityError as err:
            return {"Message": err._message()}

    
    def get_reset_password_token(email: str, secret_key:str, session) -> str:
        user = User.get_user_by(session, email = email)
        if(user):
            s = Serializer(secret_key, 300)
            return {"Message": "Genereted token succesfully, need to implement mail to email",
            "Token":s.dumps({"email": email, "scope": "reset_password"}).decode()}
        else:
            return {"Message": f"User with email='{email}' does not exist"}

    def reset_password(new_password: str, token:str, secret_key: str, session) -> dict:
        s = Serializer(secret_key)
        try:
            payload = s.loads(token.encode())
        except SignatureExpired as err:
            return {"message": 'token expired'}
        email = payload['email']
        scope = payload['scope']
        user = User.get_user_by(session, email = email)
        if user and scope == "reset_password":
            user.password = new_password
            session.commit()
            return {"message": "password changed succesfully"}
        else:
            return {"message": "invalid token"}
        

    def get_user_by(session, **kwargs):
        user = session.query(User).filter_by(**kwargs).first()
        if(user):
            user.session = session
        return user
    

    def get_login_token(session, secret_key, password, **kwargs):
        user = User.get_user_by(session, **kwargs)
        if(user and user.check_password(password)):
            s = Serializer(secret_key, 15811200) # about 1/2 a year
            return {"message": f"Successfully logged in as {user.username}", 
            "token": s.dumps({"username": user.username, "scope": "login"}).decode()}
        else:
            return {"message": "wrong username/password", "token": None}
    
    def verify_login_token(token, session, secret_key):
        s = Serializer(secret_key)
        try:
            payload = s.loads(token.encode())
        except SignatureExpired as err:
            return {"message": 'token expired'}
        username = payload['username']
        scope = payload['scope']
        if username and scope == "login":
            user = User.get_user_by(session, username=username)
            return {"message": "verified", "user": user}
        else:
            return {"message": "invalid token", "user": None}
        

    def get_all(session):
        users = session.query(User).all()
        return users


    def create_user(session, **kwargs) -> dict:
        try:
            user = User(**kwargs)
            session.add(user)
            session.commit()
            return user.to_dict()
        except sa.exc.IntegrityError as err:
            if(session.bind.echo):
                print(f"[!] {err._message()}")
            return {"Message": err._message()}
        except TypeError as err:
            return {"Message": str(err)}
    
    def delete_user(session, **kwargs):
        user = User.get_user_by(**kwargs)
        if(user):
            session.delete(user)
            session.commit()
        else:
            return {"Message": "User does not exist"}

    def create_table(engine):
        User.__table__.create(bind = engine)
    def drop_table(engine):
        User.__table__.drop(bind=engine)

    def __repr__(self):
        return f"<User id={self.id},username={self.username}>"

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'username' : self.username,
            'email' : self.email,
            'password' : self.password,

            'role' : self.role,

            'created' : self.created,
            'created_by' : self.created_by,
            'last_modified' : self.last_modified,
            'last_modified_by' : self.last_modified_by
        }

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(BASEDIR, ".env"))

    def get_env_vars():
        config = {
            "SECRET_KEY" : os.getenv("SECRET_KEY"),
            "DATABASE_URI" : os.getenv("DATABASE_URI")
        }
        return config
    env = get_env_vars()
    engine = sa.create_engine(env["DATABASE_URI"], echo= False)
    
    #Base.metadata.reflect(engine)
    #Base.metadata.drop_all(engine)
    #Base.metadata.create_all(engine)
    #Session = sessionmaker(bind = engine)
    #session = Session()
    #user = User(name="not matha", username="not_matha", email="not_matha@mail.com", password="pass")
    #session.add(user)
    #session.commit()
    #user = session.query(User).filter_by(id = 1).first()
    #user.role = "admin"
    #session.commit()
    #print(user.to_dict())
    #print(UserOut.from_orm(user).dict())
    #u = User.get_user_by(session, email="matha@mail.com", id = 2)
    #print(u)
    #u = User.create_user(session, name="m matha", username="matha", email="matha@mail.com", password="pass", role = "admin")
    #print(u)
    #token = User.get_reset_password_token("matha@mail.com", env['SECRET_KEY'], session)
    #print(token)
    #print(User.reset_password("reset_pass", token['Token'], env["SECRET_KEY"], session))
    #print(User.get_all(session))
    
    #User.create_table(engine)
    #User.drop_table(engine)



