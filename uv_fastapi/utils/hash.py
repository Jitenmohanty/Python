from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Truncate password to 72 characters for bcrypt compatibility
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain: str, hashed):
    # Truncate password to 72 characters for bcrypt compatibility
    if len(plain) > 72:
        plain = plain[:72]
    return pwd_context.verify(plain, hashed)
