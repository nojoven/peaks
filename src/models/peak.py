from sqlmodel import Field, SQLModel


class Peak(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    lat: float
    lon: float
    altitude: float

