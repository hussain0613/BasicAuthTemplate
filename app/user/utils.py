import typing

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

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}