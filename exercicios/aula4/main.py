from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

class Usuario(BaseModel):
    nome: str
    idade: int

app = FastAPI()

users = []

@app.get('/', response_class=HTMLResponse)
async def show_page():
    return HTMLResponse(content=open('pagina.html').read())

@app.post('/users')
async def add_user(usuario : Usuario):
    users.append(usuario)
    return users

@app.get('/users')
async def get_users(index : int | None = None):
    if index is None:
        return users
    else:
        return users[index]

@app.delete('/users')
async def delete_users():
    users.clear()
    return users