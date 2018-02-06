from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["sha512_crypt", "des_crypt"],

    deprecated="auto"
    )

def verify(pw, hash):
    return pwd_context.verify(pw, hash)

def hash(pw):
    return pwd_context.hash(pw)
