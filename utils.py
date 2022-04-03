from passlib.context import CryptContext

# Defining Hashng Algo
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

# Hashing the Password
def hash_password(password: str):
    return pwd_context.hash(password)

# Comapring the User-Input Password and Saved Hashed Password
def compare_hashes(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)