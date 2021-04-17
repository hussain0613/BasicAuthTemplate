from __future__ import annotations

import sqlalchemy as sa
from pydantic import BaseModel, Field
import typing
import bcrypt


#from sqlalchemy.ext.declarative import declarative_base

#from ..config import get_env_vars
class UserOut(BaseModel):
    __tablename__:str = "users"

    id: int
    name: str
    username: str
    email: str
    
    role: str

    #created: float
    #created_by: int
    #last_modified: float
    #last_modified_by: int

#Base = sa.ext.declarative.declarative_base()
#Base = declarative_base()

class User(BaseModel):
    __tablename__:str = "users"

    ## flag = 0 means nothing's changed, 1 new entry, 2 name, 4 username and so on
    flag: typing.Optional[int] = 0

    id: int
    name: str = Field(regex="^[a-zA-Z0-9 ]{1,200}$")
    username: str = Field(regex="^[a-zA-Z0-9_.]{1,200}$")
    email: str = Field(regex="^[a-zA-Z0-9_.-]+@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]+$")
    password: str

    role: str

    #created: float
    #created_by: int
    #last_modified: float
    #last_modified_by: int


    def update_name(self, new_name:str):
        self.name = new_name
        self.flag = self.flag
    
    def update_username(self, new_uname:str, password:str):
        if(bcrypt.checkpw(password, self.password)):
            self.username = new_uname
            self.flag = self.flag | 4
            return True
        else:
            print("[!] Wrong password")
            return False
    
    def update_email(self, new_email:str, password:str):
        if(bcrypt.checkpw(password, self.password)):
            self.email = new_email
            self.flag = self.flag | 8
            return True
        else:
            print("[!] Wrong password")
            return False

    def update_password(self, new_passowrd:str, password:str):
        if(bcrypt.checkpw(password.encode(), self.password.encode())):
            self.password = bcrypt.hashpw(new_passowrd.encode(), bcrypt.gensalt()).decode()
            self.flag = self.flag | 16
            return True
        else:
            print("[!] Wrong password")
            return False

    def update_role(self, new_role:str):
        self.role = new_role
        self.flag = self.flag | 32
    
    
    def save(self, engine:sa.engine.base.Engine) -> None:
        user = User.getUSerById(self.id, engine)
        
        to_be_updated = {}
        if(self.flag & 1): return User.create_user(self.dict(), engine)
        if(self.flag & 2): to_be_updated["name"] = self.name
        if(self.flag & 4): to_be_updated["username"] = self.username
        if(self.flag & 8): to_be_updated["email"] = self.email
        if(self.flag & 16): to_be_updated["passowrd"] = self.password
        if(self.flag & 32): to_be_updated["role"] = self.role

        user_table = User.get_table_obj(engine)
        sa.update(user_table).where(user_table.c.id == self.id).values(**to_be_updated)


    def updet_self_obj(self, engine:sa.engine.base.Engine) -> None:
        user = User.getUSerById(self.id, engine)
        self.name = user.name
        self.username = user.username
        self.email = user.email
        self.password = user.password
        self.email = user.email
        self.email = user.email


    def get_reset_password_token(email: str, engine: sa.engine.base.Engine):
        user = User.getUserByEmail(email)

    def reset_password(new_passowrd, token:str, engine: sa.engine.base.Engine):
        self.passowrd = bcrypt.hashpw(new_passowrd, bcrypt.gensalt())

    
    def getUSerById(id:int, engine: sa.engine.base.Engine) -> User:
        
        user = list(engine.connect().execute(f"select * from {User.__tablename__} where id = '{id}'"))
        if(len(user) == 0): return None
        else: user = user[0]
        user = User.from_row_to_obj(user)
        return user
    
    def getUserByUsername(username:str, engine: sa.engine.base.Engine) -> User:
        ## should check username validity
        user = list(engine.connect().execute(f"select * from {User.__tablename__} where username = '{username}'"))
        if(len(user) == 0): return None
        else: user = user[0]
        user = User.from_row_to_obj(user)
        return user
    
    def getUserByEmail(email:str, engine: sa.engine.base.Engine) -> User:
        ## should check username validity
        user = list(engine.connect().execute(f"select * from {User.__tablename__} where email = '{email}'"))
        if(len(user) == 0): return None
        else: user = user[0]
        user = User.from_row_to_obj(user)
        return user

    
    def create_user(info:dict, engine:sa.engine.base.Engine) -> bool:
        user_table = User.get_table_obj(engine)
        ins = user_table.insert()
        conn = engine.connect()
        ## incomplete fields check integrity hashing, email/uname/pass format validation etc
        try:
            #user = list(
            conn.execute(ins.values(
                name = info['name'],
                username = info['username'],
                email = info['email'],
                password = bcrypt.hashpw(info['password'].encode(), bcrypt.gensalt()).decode(),
                role = info['role'],
            ))#.returning(sa.literal_column('*'))))
            #if(len(user) == 0): return False
            #else: user = User.from_row_to_obj(engine)
            #print(user)
            return True
        except sa.exc.IntegrityError as err:
            if(engine.echo):
                print(f"[!] {err._message()}")
            return False

    def from_row_to_obj(row: sa.engine.result.RowProxy) -> User:
        return User(id = row[0], name = row[1], username= row[2], email= row[3], password = row[4], role = row[5])
        

    def get_table_obj(engine: sa.engine.base.Engine) -> sa.sql.schema.Table:
        metadata = sa.MetaData(engine)
        user_table = sa.Table(
            User.__tablename__,
            metadata,
            sa.Column("id", sa.Integer, primary_key = True, autoincrement = True),
            sa.Column("name", sa.String(200)),
            sa.Column("username", sa.String(200), unique=True, nullable = True),
            sa.Column("email", sa.String(200), unique=True, nullable = True),
            sa.Column("password", sa.String(300)),
            sa.Column("role", sa.String(50))
        )
        return user_table

    def create_table(engine: sa.engine.base.Engine) -> bool:
        user_table = User.get_table_obj(engine)
        try:
            user_table.create()
            return True
        except sa.exc.OperationalError as err:
            if f"table {User.__tablename__} already exists" in err._message():
                if engine.echo:
                    print(f"[!] table '{User.__tablename__}' already exists!")
                return False
            else:
                raise err
    
    def delete_table(engine: sa.engine.base.Engine) -> bool:
        conn = engine.connect()
        try:
            conn.execute(f"drop table {User.__tablename__}")
            return True
        except sa.exc.OperationalError as err:
            if f"no such table: {User.__tablename__}" in err._message():
                if(engine.echo):
                    print(f"[!] Table '{User.__tablename__}' does not exist!")
                return False
            else:
                raise err

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

    engine = sa.create_engine(get_env_vars()["DATABASE_URI"], echo= False)
    User.__engine__ = engine
    

    #User.create_table(engine)
    n = 4
    User.create_user({"name": f"Test User{n}", "username":f"tuser{n}", "email": f"tuser{n}@mail.com", "password": "pass", "role": "guest"}, engine)

    #user = UserOut.parse_obj(User.getUserByUsername("matha", engine))
    #user = User.getUserByUsername("matha", engine)
    #user.update_password("new_pass", "pass")
    #user.save(engine)
    #print(user)
    #print(user.__password__)
    #user.updet_self_obj(engine)

    #print(User.getUSerById(2, engine))
    
    