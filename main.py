from fastapi import FastAPI
from routes import auth, books

app = FastAPI()

app.include_router(auth.router)
app.include_router(books.router)

