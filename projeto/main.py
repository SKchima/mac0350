from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from typing import Annotated

from models import Usuario, Reserva, Estacao
from database import engine, create_db_and_tables

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(status_code=401, detail="Não logado")
    with Session(engine) as session:
        usuario_encontrado = session.exec(select(Usuario).where(Usuario.nome == session_user)).first()
        if not usuario_encontrado:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return usuario_encontrado


@app.get("/")
def show_home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

@app.get("/cadastro") 
def get_formulario(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro.html")

@app.get("/login")
def get_formulario_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/estacoes")
def get_estacoes(request: Request, user: Usuario = Depends(get_active_user)):
    return templates.TemplateResponse(
        request=request, 
        name="estacoes.html",
        context={"user": user}
    )

@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

@app.get("/usuarios")
def existe_usuario(nome: str):
    with Session(engine) as session:
        usuario_encontrado = session.exec(select(Usuario).where(Usuario.nome == nome)).first()
        if not usuario_encontrado:
            return False
        return True

@app.post("/reservas")
def criar_reserva(reserva: Reserva):
    with Session(engine) as session:
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        return reserva

@app.post("/login")
def login(usuario: Usuario, response: Response):
    with Session(engine) as session:
        usuario_encontrado = session.exec(select(Usuario).where(Usuario.nome == usuario.nome)).first()
        if not usuario_encontrado:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        if usuario_encontrado.senha != usuario.senha:
            raise HTTPException(status_code=401, detail="Senha incorreta")
        response.set_cookie(key="session_user", value=usuario_encontrado.nome)
        return {"message": "Login realizado com sucesso"}

@app.get("/logout")
def logout(response: Response):
    response.delete_cookie(key="session_user")
    return {"message": "Logout realizado com sucesso"}