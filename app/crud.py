from fastapi import HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """
    Cria uma nova tarefa no banco de dados.
    
    Args:
        db: Sessão do banco de dados
        task: Dados da tarefa a ser criada (validados pelo esquema TaskCreate)
        
    Returns:
        Task: A tarefa criada com todos os dados (incluindo ID gerado)
    """
    try:
        
        if not task.title or not task.title.strip():
            raise ValueError("O título da tarefa não pode estar vazio")
            
        
        db_task = models.Task(
            title=task.title.strip(),
            description=task.description.strip() if task.description else None
        )
        
        
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        return db_task
        
    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar a tarefa no banco de dados: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao criar tarefa: {str(e)}"
        )
def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Task]:
    """
    Retorna uma lista paginada de tarefas do banco de dados.
    
    Args:
        db: Sessão do banco de dados
        skip: Número de registros a pular (para paginação)
        limit: Número máximo de registros a retornar (para paginação)
        
    Returns:
        List[models.Task]: Lista de tarefas encontradas
        
    Raises:
        HTTPException: Se ocorrer algum erro ao acessar o banco de dados
    """
    try:
        if skip < 0:
            raise ValueError("O parâmetro 'skip' não pode ser negativo")
        if limit <= 0 or limit > 1000:  # Definimos um limite máximo razoável
            raise ValueError("O parâmetro 'limit' deve estar entre 1 e 1000")
            
        tasks = db.query(models.Task)\
                 .order_by(models.Task.id)\
                 .offset(skip)\
                 .limit(limit)\
                 .all()
                 
        return tasks
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar o banco de dados: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao recuperar tarefas: {str(e)}"
        )

def get_task(db: Session, task_id: int) -> models.Task:
    """
    Retorna uma tarefa específica pelo seu ID.
    
    Args:
        db: Sessão do banco de dados
        task_id: ID da tarefa a ser recuperada
        
    Returns:
        models.Task: A tarefa encontrada
        
    Raises:
        HTTPException: 
            - 400: Se o ID for inválido
            - 404: Se a tarefa não for encontrada
            - 500: Se ocorrer um erro no banco de dados
    """
    try:
        # Validação do ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("ID da tarefa deve ser um número inteiro positivo")
        
        # Busca a tarefa no banco de dados
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarefa com ID {task_id} não encontrada"
            )
            
        return task
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar o banco de dados: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao buscar tarefa: {str(e)}"
        )

def update_task(db: Session, task_id: int, task: schemas.TaskCreate) -> models.Task:
    """
    Atualiza uma tarefa existente no banco de dados.
    
    Args:
        db: Sessão do banco de dados
        task_id: ID da tarefa a ser atualizada
        task: Dados atualizados da tarefa (validados pelo esquema TaskCreate)
        
    Returns:
        models.Task: A tarefa atualizada
        
    Raises:
        HTTPException:
            - 400: Se os dados ou ID forem inválidos
            - 404: Se a tarefa não for encontrada
            - 500: Se ocorrer erro no banco de dados
    """
    try:
        # Validação do ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("ID da tarefa deve ser um número inteiro positivo")
            
        # Validação dos dados de entrada
        if not task.title or not task.title.strip():
            raise ValueError("O título da tarefa não pode estar vazio")
            
        # Busca a tarefa existente
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarefa com ID {task_id} não encontrada"
            )
            
        # Atualiza os campos
        db_task.title = task.title.strip()
        db_task.description = task.description.strip() if task.description else None
        
        try:
            db.commit()
            db.refresh(db_task)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar a tarefa no banco de dados: {str(e)}"
            )
            
        return db_task
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao atualizar tarefa: {str(e)}"
        )

def delete_task(db: Session, task_id: int) -> models.Task:
    """
    Exclui uma tarefa do banco de dados.
    
    Args:
        db: Sessão do banco de dados
        task_id: ID da tarefa a ser excluída
        
    Returns:
        models.Task: A tarefa que foi excluída
        
    Raises:
        HTTPException:
            - 400: Se o ID for inválido
            - 404: Se a tarefa não for encontrada
            - 500: Se ocorrer erro no banco de dados
    """
    try:
        # Validação do ID
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("ID da tarefa deve ser um número inteiro positivo")
        
        # Busca a tarefa no banco de dados
        db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
        
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarefa com ID {task_id} não encontrada"
            )
            
        try:
            # Remove a tarefa e confirma a transação
            db.delete(db_task)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao excluir a tarefa do banco de dados: {str(e)}"
            )
            
        return db_task
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao excluir tarefa: {str(e)}"
        )