from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated

class usuario(BaseModel):
    nome: str
    senha: str
    bio: str

class LoginSchema(BaseModel):
    nome: str
    senha: str

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

users_db = []

def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(status_code=401, detail="Não logado")
    
    user = next((u for u in users_db if u.nome == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    return user

@app.get("/") 
def get_formulario(request: Request):
    return templates.TemplateResponse(request=request, name="formulario.html")

@app.post("/users")
def criar_usuario(u: usuario):
    users_db.append(u)
    return {"message": "Usuário criado com sucesso", "usuario": u.nome}

@app.get("/login")
def get_formulario_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")
def login(dados: LoginSchema, response: Response):
    usuario_encontrado = next((u for u in users_db if u.nome == dados.nome), None)
    
    if not usuario_encontrado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario_encontrado.senha != dados.senha:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    response.set_cookie(key="session_user", value=dados.nome)
    return {"message": "Logado com sucesso"}

@app.get("/home")
def show_profile(request: Request, user: usuario = Depends(get_active_user)):
    return templates.TemplateResponse(
        request=request, 
        name="perfil.html", 
        context={"user": {"nome": user.nome, "bio": user.bio}}
    )