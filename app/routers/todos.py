from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import crud, schemas, dependencies
from ..database import get_db

# Cria um "roteador" para agrupar as rotas relacionadas a tarefas
router = APIRouter(
    prefix="/tasks",  # Prefixo para todas as rotas neste arquivo
    tags=["Tasks"]    # Tag para agrupar na documentação automática (/docs)
)

@router.post(
    "/", 
    response_model=schemas.Task, 
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    _ = Depends(dependencies.verify_token)
):
    """
    Cria uma nova tarefa.

    - **title**: O título da tarefa (obrigatório).
    - **description**: A descrição da tarefa (opcional).

    É necessário enviar um header `token` com o valor correto para autenticação.
    """
    return crud.create_task(db=db, task=task)


@router.get("/", response_model=list[schemas.Task])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    _ = Depends(dependencies.verify_token)
):
    """
    Retorna uma lista de todas as tarefas.
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


from fastapi import HTTPException

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int, 
    db: Session = Depends(get_db),
    _ = Depends(dependencies.verify_token)
):
    """
    Retorna os detalhes de uma tarefa específica.
    """
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, 
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db),
    _ = Depends(dependencies.verify_token)
):
    """
    Atualiza o título e a descrição de uma tarefa existente.
    """
    db_task = crud.update_task(db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=schemas.Task)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    _ = Depends(dependencies.verify_token)
):
    """
    Exclui uma tarefa específica.
    """
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task