from pydantic import BaseModel, Field


class DireccionCreate(BaseModel):
    Id_Ciudad: int = 1  # Ajusta al id_ciudad por defecto en tu BD si no lo mandan desde el front
    colonia: str = Field(..., min_length=1, max_length=50)
    calle: str | None = Field(default=None, max_length=50)
    referencia: str = Field(..., min_length=1, max_length=200)
    nombre_destinatario: str | None = Field(default=None, max_length=50)


class DireccionOut(BaseModel):
    Id_Direccion: int
    Id_Ciudad: int
    colonia: str
    calle: str | None = None
    referencia: str
    nombre_destinatario: str | None = None

    class Config:
        from_attributes = True  # En Pydantic v1 usa orm_mode = True