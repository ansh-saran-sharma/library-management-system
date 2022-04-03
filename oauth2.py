# Imports
import schemas
from jose import JWSError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

# Oauth2 Scheme on "/login" URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

# Secret Key
SECRET_KEY = "Q938FHQO3F7HQO3I4F7HQ3I47FHQ3P948FHQP3IF7HQP3IR7FGHQIP34"
# Algorithm
ALGORITHM = "HS256"
# Expiration Time
EXPIRATION_TIME_MINUTES = 30

# Creating JWT Token
def create_access_token(data: dict):
   to_encode = data.copy()
   # Calculating Expiration Time
   expiration_time = datetime.utcnow() + timedelta(minutes = EXPIRATION_TIME_MINUTES)
   # Adding New Property "exp"
   to_encode.update({"exp":expiration_time})
   # Creating/Encoding Token
   token = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
   return token

# Verifying JWT Access Token (Provided by User)
def verify_access_token(token: str, credentials_exception):
    try:
        # Decoding Token
        token_payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        email: str = token_payload.get("email")
        role: str = token_payload.get("role")
        if not role:
            raise credentials_exception
        # Validating Token Data using Pydantic Schema
        token_data = schemas.TokenPayLoad(email = email, role = role)
    except JWSError:
        raise credentials_exception
    # Returning Role Property/Field
    return token_data

# Getting Logged-In User Role
def get_current_user_role(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could Not Validate Credentials", headers = {"WWW-Autheticate":"Bearer"})
    return verify_access_token(token, credentials_exception)