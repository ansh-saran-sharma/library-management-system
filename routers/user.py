# Imports
from uuid import UUID
from typing import List
import schemas, utils, oauth2
from fastapi import HTTPException, status, Depends, APIRouter, Response

# Initializing APIRouter object
# Replacing "@app." with "@router."
router = APIRouter(
    prefix = "/users", # To Replace Recurring Prefix in URL
    tags=["User Operations"] # Grouping of Routes 
)

# User Repository
users = []

# Logging In & Generating JWT Token
@router.post("/login")
async def login(user_credentials: schemas.Login):
    for user in users:
        # Checking whether User-Input Email exists
        if user["email"] == user_credentials.email:
            # Comparing Saved and User-Input Passwords
            if utils.compare_hashes(user_credentials.password, user["password"]):
                # Generating Token
                token = oauth2.create_access_token(data = {"email":user["email"], "role":user["role"]})
                # Returning JWT Token and Token Type
                return {"access_token":token, "token_type":"bearer"}
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials!")
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Invalid Credentials!")

# To Fetch All Users Information
@router.get("/", response_model = List[schemas.UserOut])
async def get_all_users(current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    if current_user.role == "Librarian":
        return users
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}' is Not Authorized to View all Users Information!")

# To Fetch Particular User Information
@router.get("/{id}", response_model = schemas.UserOut)
async def get_user(id: UUID, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    for user in users:
        if user["id"] == id:
            if user["email"] == current_user.email or current_user.role == "Librarian":
                return user
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}', email: {current_user.email} is Not Authorized to View User Information!")
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exists!")

# To Create New User
@router.post("/create-user", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
async def create_user(user_data: schemas.CreateUser):
    user_data.password = utils.hash_password(user_data.password)
    users.append(user_data.dict())
    return user_data

# To Update a User
@router.put("/update-user/{id}", response_model = schemas.UserOut)
async def update_user(id: UUID, updated_data: schemas.UpdateUser, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    if current_user.role == "Librarian":
        for user in users:
            if user["id"] == id:
                user["email"] = updated_data.email
                user["password"] = utils.hash_password(updated_data.password)
                return user
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exists!")
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}', id: '{id}' is Not Authorized to Update the User Information!")

# To Delete a User
@router.delete("/delete-user/{id}")
async def delete_user(id: UUID, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    for user in users:
        if user["id"] == id:
            if current_user.email == user["email"] or current_user.role == "Librarian":
                users.remove(user)
                return Response(status_code = status.HTTP_204_NO_CONTENT)
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}', email: '{current_user.email}' is Not Authorized to Update the User Information!")
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"User with id: {id} does not exists!")