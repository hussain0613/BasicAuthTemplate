import typing
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import SignatureExpired, BadSignature
import bcrypt

## ei duita .env e rakhte hobe
#alpha1 = "`1234567890-=~!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}|asdfghjkl;'ASDFGHJKL:\"zxcvbnm,./ZXCVBNM<>? "
#alpha2 = " /.,mnbvcxzqwertyuiop[]ASDFGHJKL:\"QWERTYUIOP{}|~!@#$%^&*()_+=-0987654321`?><MNBVCXZasdfg';lkjh"


alpha1 = '|OZwX.$mV2?63Dqgt1]=G~7&a!f}\'*k>MeI(y ,cKU9pE#)-Y0B_S/^sd4HL[<uhx\\;%CJ5iNTzjFbWRl+P"Ao`{8rQv:n@'
alpha2 = '9n|A}[G.=?V);DXYb!-gIPc2CKrB/Z~v4E*Tf@60iLk"#`>zOxpu\'t{:]ewdl&8N(^JHQs%jRW+,_FoUm<5$1qy \\h73aSM'

fd = dict(zip(alpha1, alpha2))
fd_ = dict(zip(alpha2, alpha1))


def create_token(payload: dict, secret_key: str, headers:typing.Optional[dict] = None)->str:
    if not headers:
        headers = {"alg": "BCRYPT",
                   "type": "JWT"
                   }
        
    hj = json.dumps(headers)
    pj = json.dumps(payload)
    token = ".our_server.".join([
        hj, # it would've been better if some encryption was userd
        pj, # same here
        bcrypt.hashpw(secret_key.encode(),bcrypt.gensalt()).decode(),
        ])
    token = "".join(list(map(f, token)))
    return token

def verify_token(token:str, secret_key:str, headers:typing.Optional[dict] = None) -> dict:
    token = "".join(list(map(f_, token)))

    if not headers:
        headers = {"alg": "BCRYPT",
                   "type": "JWT"
                   }

    hj = json.dumps(headers)
    pj = json.dumps(payload)

    rhj, rpj, rsk = token.split(".our_server.")
    rh = json.loads(rhj)
    rp = json.loads(rpj)

    if bcrypt.checkpw(secret_key.encode(), rsk.encode()):
        ## this means the signature is right
        return rp
    else:
        return {}





from . import env, Session
from .models import User
def check_n_set_auth_head(request, response) -> dict:
    """
    checks the request for authorization header, if found validates it, and if validated then returns user dict
    otherwise returns None
    """
    auth_head = request.headers.get('authorization')
    if auth_head:
        tk = auth_head.split()
        if(len(tk) ==2):
            token = tk[1]
            r = User.verify_login_token(token, Session(), env['SECRET_KEY'])
            if r.get('user'):
                response.headers['authorization'] = auth_head
                return r['user']
    return None
            

def create_timed_token(scope:str, payload:dict, signature:str, duration:int = 300):
    s = Serializer(signature, duration)
    payload['scope'] = bcrypt.hashpw(scope.encode(), bcrypt.gensalt())
    return s.dumps(payload).decode()

def verify_timed_token(scope:str, token:str, signature:str):
    s = Serializer(signature)
    try:
        payload = s.loads(token.encode())
        if(payload.get('scope') and bcrypt.checkpw(scope, payload['scope'])): return {'message': 'verified', 'payload': payload}
        else: return {'message': 'invalid token', 'payload': None}
    except SignatureExpired as err:
        return {"message": 'token expired', 'payload': None}
    except BadSignature as err:
        return {"message": 'invalid token', 'payload': None}