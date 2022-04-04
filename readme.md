A Library Management System using FastAPI

========== USER ROUTES ==========
SIGN-UP ==>
request type : POST
url : http://127.0.0.1:8000/users/create-user
request body :
{
    "email":"",
    "password":"",
    "role":""
}

LOGIN ==>
request type : POST
url : http://127.0.0.1:8000/users/login
request body :
{
    "email":"",
    "password":""
}

FETCH ALL USERS ==>
request type : GET
url : http://127.0.0.1:8000/users/
headers : 
    key = Authentication
    Value = Bearer <token>

FETCH SPECIFIC USER ==>
request type : GET
url : http://127.0.0.1:8000/users/id
headers : 
    key = Authentication
    Value = Bearer <token>

UPDATE USER ==>
request type : PUT
url : http://127.0.0.1:8000/users/update-user/id
request body :
{
    "email":"",
    "password":""
}
headers : 
    key = Authentication
    Value = Bearer <token>

DELETE USER ==>
request type : DELETE
url : http://127.0.0.1:8000/users/delete-user/id
headers : 
    key = Authentication
    Value = Bearer <token>
========== ==========

========== BOOK ROUTES ==========
ADD BOOK ==>
request type : POST
url : http://127.0.0.1:8000/books/add-book
request body :
{
    "title":"",
    "author":"",
    "status":"",
    "price":"",
    "publisher":"",
    "page_count":"",
    "debut_year":""
}
headers : 
    key = Authentication
    Value = Bearer <token>

FETCH ALL BOOKS ==>
request type : GET
url : http://127.0.0.1:8000/books/
headers : 
    key = Authentication
    Value = Bearer <token>

FETCH SPECIFIC BOOK ==>
request type : GET
url : http://127.0.0.1:8000/books/id
headers : 
    key = Authentication
    Value = Bearer <token>

UPDATE A BOOK ==>
request type : PUT
url : http://127.0.0.1:8000/books/update-book/id
request body :
{
    "title":"",
    "author":"",
    "price":"",
    "publisher":"",
    "page_count":"",
    "debut_year":""
}
headers : 
    key = Authentication
    Value = Bearer <token>

DELETE A BOOK ==>
request type : DELETE
url : http://127.0.0.1:8000/books/delete-book/id
headers : 
    key = Authentication
    Value = Bearer <token>

BORROW A BOOK ==>
request type : POST
url : http://127.0.0.1:8000/books/borrow-book/id
headers : 
    key = Authentication
    Value = Bearer <token>

UPDATE A BOOK ==>
request type : POST
url : http://127.0.0.1:8000/books/return-book/id
headers : 
    key = Authentication
    Value = Bearer <token>
========== ==========