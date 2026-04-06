from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

contador_curtidas = 0

abas_sequencia = ["curtidas", "jupiter", "professor"]
aba_atual = 0

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="layout.html", context={"pagina": "/tab/jupiter"})

@app.get("/tab/jupiter")
async def get_jupiter(request: Request):
    return templates.TemplateResponse(request=request, name="jupiter.html")

@app.post("/tab/jupiter")
async def post_jupiter(request: Request):
    return templates.TemplateResponse(request=request, name="jupiter.html")

@app.get("/tab/professor")
async def get_professor(request: Request):
    return templates.TemplateResponse(request=request, name="professor.html")

@app.get("/tab/curtidas")
async def get_curtidas(request: Request):
    return templates.TemplateResponse(request=request, name="curtidas.html", context={"likes": contador_curtidas})

@app.get("/tab/proxima")
async def proxima_aba(request: Request):
    global aba_atual
    aba_atual = (aba_atual + 1) % len(abas_sequencia)
    proxima = abas_sequencia[aba_atual]
    
    if proxima == "curtidas":
        return await get_curtidas(request)
    elif proxima == "jupiter":
        return await get_jupiter(request)
    else:
        return await get_professor(request)

@app.post("/curtir")
async def gerenciar_curtidas(request: Request, acao: str = "somar"):
    global contador_curtidas
    if acao == "somar":
        contador_curtidas += 1
    elif acao == "limpar":
        contador_curtidas = 0
    return templates.TemplateResponse(request=request, name="curtidas.html", context={"likes": contador_curtidas})