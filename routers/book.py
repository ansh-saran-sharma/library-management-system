# Imports
import schemas, oauth2
from uuid import UUID
from typing import List
from fastapi import HTTPException, status, Depends, APIRouter, Response

# Initializing APIRouter object
# Replacing "@app." with "@router."
router = APIRouter(
    prefix = "/books", # To Replace Recurring Prefix in URL
    tags=["Book Operations"] # Grouping of Routes 
)

# Book Repository
books = []

# To Fetch All Books Information
@router.get("/", response_model = List[schemas.BookOut])
async def get_all_books(current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    return books

# To Fetch Particular Book Information
@router.get("/{id}", response_model = schemas.BookOut)
async def get_book(id: UUID, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    for book in books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with id: {id} does not exists!")

# To Add a Book
@router.post("/add-book", status_code = status.HTTP_201_CREATED, response_model = schemas.BookOut)
async def add_book(book_data: schemas.Book, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    if current_user.role == "Librarian":
        books.append(book_data.dict())
        return book_data
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}' is Not Authorized to Add a Book!")

# To Update a Book
@router.put("/update-book/{id}", response_model = schemas.BookOut)
async def update_book(id: UUID, updated_data: schemas.UpdateBook, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    if current_user.role == "Librarian":
        for book in books:
            if book["id"] == id:
                book["title"] = updated_data.title
                book["price"] = updated_data.price
                book["publisher"] = updated_data.publisher
                book["page_count"] = updated_data.page_count
                return book
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with id: {id} does not exists!")
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}' is Not Authorized to Update a Book!")

# To Delete a Book
@router.delete("/delete-book/{id}")
async def delete_book(id: UUID, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    if current_user.role == "Librarian":
        for book in books:
            if book["id"] == id:
                books.remove(book)
                return Response(status_code = status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with id: {id} does not exists!")
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}' is Not Authorized to Delete/Remove a Book!")

# To Borrow a Book
@router.post("/borrow-book/{id}", status_code = status.HTTP_200_OK, response_model = schemas.BookOut)
async def borrow_book(id: UUID, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    if current_user.role == "Member":
        for book in books:
            if book["id"] == id:
                if book["status"] == "AVAILABLE":
                    book["status"] = "BORROWED"
                    return book
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with id: {id} is already BORROWED!")
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with id: {id} does not exists!")
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}' is Not Authorized to Borrow a Book!")

# To Return a Book
@router.post("/return-book/{id}", status_code = status.HTTP_200_OK, response_model = schemas.BookOut)
async def return_book(id: UUID, current_user: schemas.TokenPayLoad = Depends(oauth2.get_current_user_role)):
    if current_user.role == "Member":
        for book in books:
            if book["id"] == id:
                if book["status"] == "BORROWED":
                    book["status"] = "AVAILABLE"
                    return book
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with id: {id} is already AVAILABLE!")
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Book with id: {id} does not exists!")
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"The current user with role: '{current_user.role}' is Not Authorized to Borrow a Book!")