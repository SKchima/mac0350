from sqlmodel import SQLModel, Field

class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    senha: str
    estacao_em_uso_id: int | None = Field(default=None, foreign_key="estacao.id")
    
class Estacao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    usuario_em_uso_id: int | None = Field(default=None, foreign_key="usuario.id")

class Reserva(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    estacao_id: int = Field(foreign_key="estacao.id")
    data_inicio: str
    data_fim: str
    hora_inicio: str
    hora_fim: str

class EmUso(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    estacao_id: int = Field(foreign_key="estacao.id")
    data_inicio: str
    data_fim: str
    hora_inicio: str
    hora_fim: str
