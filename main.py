# Imports
from fastapi import FastAPI
from routers import book, user
from fastapi.middleware.cors import CORSMiddleware

# Instance of FastAPI
app = FastAPI()

# Allowed "origins" list
origins = [
    "http://localhost",
    "http://localhost:8080",
]

# "CORS" Policy Parameters
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Grabbing "router" Object From "book.py"
app.include_router(book.router)
# Grabbing "router" Object From "user.py"
app.include_router(user.router)

# Route Path
@app.get("/")
def root():
    return {"message":"Welcome to Library Management System using FastAPI"}