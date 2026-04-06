from fastapi import FastAPI, Request, Depends, HTTPException, Cookie, Response, Form
from fastapi.responses import HTMLResponse
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
    with Session(engine) as session:
        estacoes = session.exec(select(Estacao)).all()
        if not estacoes:
            for i in range(1, 5):
                nova_estacao = Estacao(id=i, nome=f"Estação {i}")
                session.add(nova_estacao)
            session.commit()


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

#################################################
# Rotas de login

@app.get("/cadastro") 
def get_formulario(request: Request):
    return templates.TemplateResponse(request=request, name="cadastro.html")

@app.post("/usuarios", response_class=HTMLResponse)
def criar_usuario(request: Request, nome: str = Form(...), senha: str = Form(...)):
    with Session(engine) as session:
        usuario_existente = session.exec(select(Usuario).where(Usuario.nome == nome)).first()
        if usuario_existente:
            return HTMLResponse(content=f"<p>Erro: o nome '{nome}' já está em uso.</p>")
        novo_usuario = Usuario(nome=nome, senha=senha)
        session.add(novo_usuario)
        session.commit()
        return HTMLResponse(content=f"<p>Usuário '{nome}' cadastrado com sucesso! <a href='/login'>Faça o login</a>.</p>")

@app.get("/login")
def get_formulario_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login", response_class=HTMLResponse)
def login(nome: str = Form(...), senha: str = Form(...)):
    with Session(engine) as session:
        usuario_encontrado = session.exec(select(Usuario).where(Usuario.nome == nome)).first()
        if not usuario_encontrado or usuario_encontrado.senha != senha:
            return HTMLResponse(content="<p>Erro: usuário ou senha inválidos.</p>")
        resposta = HTMLResponse(content="<p>Redirecionando...</p>", headers={"HX-Redirect": "/estacoes"})
        resposta.set_cookie(key="session_user", value=usuario_encontrado.nome)
        return resposta

@app.get("/usuarios")
def existe_usuario(nome: str):
    with Session(engine) as session:
        usuario_encontrado = session.exec(select(Usuario).where(Usuario.nome == nome)).first()
        if not usuario_encontrado:
            return False
        return True

@app.get("/logout")
def logout():
    from fastapi.responses import RedirectResponse
    resposta = RedirectResponse(url="/", status_code=303)
    resposta.delete_cookie(key="session_user")
    return resposta

#################################################
# Rotas de estações

@app.get("/estacoes")
def get_estacoes(request: Request, user: Usuario = Depends(get_active_user)):
    with Session(engine) as session:
        estacoes = session.exec(select(Estacao)).all()
        usuarios = session.exec(select(Usuario)).all()
        nomes_usuarios = {u.id: u.nome for u in usuarios}
        
    return templates.TemplateResponse(
        request=request,
        name="estacoes.html",
        context={"user": user, "estacoes": estacoes, "nomes_usuarios": nomes_usuarios}
    )

@app.post("/utilizar", response_class=HTMLResponse)
def utilizar_estacao(estacao_id: int = Form(...), user: Usuario = Depends(get_active_user)):
    with Session(engine) as session:
        est = session.exec(select(Estacao).where(Estacao.id == estacao_id)).first()
        usr = session.exec(select(Usuario).where(Usuario.id == user.id)).first()
        
        if not est:
            return HTMLResponse(content="<p>Erro: Estação não encontrada.</p>")
        if est.usuario_em_uso_id:
            return HTMLResponse(content="<p>Erro: Estação já está em uso!</p>")
        if usr.estacao_em_uso_id:
            return HTMLResponse(content="<p>Erro: Você já está usando uma estação. Desocupe-a primeiro!</p>")
            
        est.usuario_em_uso_id = usr.id
        usr.estacao_em_uso_id = est.id
        session.add(est)
        session.add(usr)
        session.commit()
        return HTMLResponse(content=f"<p>Você começou a utilizar a Estação {estacao_id}!</p>")

@app.post("/desocupar", response_class=HTMLResponse)
def desocupar_estacao(estacao_id: int = Form(...), user: Usuario = Depends(get_active_user)):
    with Session(engine) as session:
        est = session.exec(select(Estacao).where(Estacao.id == estacao_id)).first()
        usr = session.exec(select(Usuario).where(Usuario.id == user.id)).first()
        
        if not est:
            return HTMLResponse(content="<p>Erro: Estação não encontrada.</p>")
        if est.usuario_em_uso_id != usr.id:
            return HTMLResponse(content="<p>Erro: Você não está ocupando esta estação!</p>")
            
        est.usuario_em_uso_id = None
        usr.estacao_em_uso_id = None
        session.add(est)
        session.add(usr)
        session.commit()
        return HTMLResponse(content=f"<p>Estação {estacao_id} liberada com sucesso!</p>")

#################################################
# Rotas de reservas

@app.post("/reservas", response_class=HTMLResponse)
def criar_reserva(request: Request, estacao_id: int = Form(...), dia: int = Form(...), horario: int = Form(...), user: Usuario = Depends(get_active_user)):
    with Session(engine) as session:
        if estacao_id < 1 or estacao_id > 4:
            return HTMLResponse(content="<p>Erro: Estação inválida. Escolha de 1 a 4.</p>")
        conflito = session.exec(select(Reserva).where(Reserva.estacao_id == estacao_id, Reserva.dia == dia, Reserva.horario == horario)).first()
        if conflito:
            return HTMLResponse(content="<p>Erro: Esta estação já está reservada nesse dia e horário!</p>")
        nova_reserva = Reserva(usuario_id=user.id, estacao_id=estacao_id, dia=dia, horario=horario)
        session.add(nova_reserva)
        session.commit()
        session.refresh(nova_reserva)
        return HTMLResponse(content=f"<p>Reserva criada com sucesso para a estação {estacao_id}!</p>")

@app.get("/reservas")
def get_reservas(request: Request, pagina: int = 1, user: Usuario = Depends(get_active_user)):
    maximo = 5
    minimo = (pagina - 1) * maximo
    with Session(engine) as session:
        todas = session.exec(select(Reserva).where(Reserva.usuario_id == user.id).offset(minimo).limit(maximo + 1)).all()
        tem_proxima = len(todas) > maximo
        reservas = todas[:maximo]
        return templates.TemplateResponse(
            request=request,
            name="reservas.html",
            context={"reservas": reservas, "pagina": pagina, "tem_proxima": tem_proxima, "user": user}
        )

@app.put("/reservas", response_class=HTMLResponse)
def atualizar_reserva(id: int = Form(...), estacao_id: int = Form(...), dia: int = Form(...), horario: int = Form(...), user: Usuario = Depends(get_active_user)):
    with Session(engine) as session:
        reserva_encontrada = session.exec(select(Reserva).where(Reserva.id == id)).first()
        if not reserva_encontrada:
            return HTMLResponse(content="<p>Erro: Reserva não encontrada!</p>")
        if reserva_encontrada.usuario_id != user.id:
            return HTMLResponse(content="<p>Erro: Você não tem permissão para atualizar uma reserva de outro usuário!</p>")
        if estacao_id < 1 or estacao_id > 4:
            return HTMLResponse(content="<p>Erro: Estação inválida. Escolha de 1 a 4.</p>")
        conflito = session.exec(select(Reserva).where(Reserva.estacao_id == estacao_id, Reserva.dia == dia, Reserva.horario == horario)).first()
        if conflito and conflito.id != id:
            return HTMLResponse(content="<p>Erro: Esta estação já está reservada nesse dia e horário!</p>")
        reserva_encontrada.estacao_id = estacao_id
        reserva_encontrada.dia = dia
        reserva_encontrada.horario = horario
        session.add(reserva_encontrada)
        session.commit()
        session.refresh(reserva_encontrada)
        return HTMLResponse(content=f"<p>Reserva {id} atualizada com sucesso!</p>")

@app.delete("/reservas", response_class=HTMLResponse)
def deletar_reserva(id: int, user: Usuario = Depends(get_active_user)):
    with Session(engine) as session:
        reserva_encontrada = session.exec(select(Reserva).where(Reserva.id == id)).first()
        if not reserva_encontrada:
            return HTMLResponse(content="<p>Erro: Reserva não encontrada!</p>")
        if reserva_encontrada.usuario_id != user.id:
            return HTMLResponse(content="<p>Erro: Você não pode deletar uma reserva de outro usuário!</p>")
        session.delete(reserva_encontrada)
        session.commit()
        return HTMLResponse(content=f"<p>Reserva {id} cancelada com sucesso!</p>")