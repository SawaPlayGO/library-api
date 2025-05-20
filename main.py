from fastapi import FastAPI
from routes import auth, book, reader, borrow

app = FastAPI()

routers = [auth.router, book.router, reader.router, borrow.router]

for router in routers:
    app.include_router(router)

