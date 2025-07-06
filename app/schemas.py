from pydantic import BaseModel, ConfigDict
from datetime import datetime

# Esquema para a criação de uma tarefa (dados de entrada)
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

# Esquema para a leitura de uma tarefa (dados de saída)
class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)