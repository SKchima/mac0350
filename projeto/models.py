from sqlmodel import SQLModel, Field, Relationship

class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    senha: str
    estacao_em_uso_id: int | None = Field(default=None, foreign_key="estacao.id")
    reservas: list["Reserva"] = Relationship(back_populates="usuario")
    
class Estacao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    usuario_em_uso_id: int | None = Field(default=None, foreign_key="usuario.id")
    reservas: list["Reserva"] = Relationship(back_populates="estacao")

class Reserva(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    estacao_id: int = Field(foreign_key="estacao.id")
    dia: int
    horario: int
    usuario: "Usuario" = Relationship(back_populates="reservas")
    estacao: "Estacao" = Relationship(back_populates="reservas")

class EmUso(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    estacao_id: int = Field(foreign_key="estacao.id")