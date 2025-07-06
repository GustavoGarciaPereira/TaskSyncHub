import os, sys
import pytest
from fastapi import status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import MagicMock
from datetime import datetime


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Task
from app.schemas import TaskCreate
from app.crud import create_task

@pytest.fixture
def mock_db_session():
    """Fixture que fornece uma sessão mockada do banco de dados"""
    session = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    session.rollback = MagicMock()
    return session

def test_create_task_success(mock_db_session):
    """Testa a criação bem-sucedida de uma tarefa"""
    # Dados de entrada
    task_data = TaskCreate(
        title="  Tarefa de Teste  ",
        description="  Descrição com espaços  "
    )
    

    mock_task = MagicMock(spec=Task)
    mock_task.id = 1
    mock_task.title = "Tarefa de Teste"
    mock_task.description = "Descrição com espaços"
    
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    
    def refresh_mock(task):
        task.id = 1
    mock_db_session.refresh.side_effect = refresh_mock
    

    result = create_task(db=mock_db_session, task=task_data)
    
    # Verificações
    assert isinstance(result, Task)
    assert result.title == "Tarefa de Teste"
    assert result.description == "Descrição com espaços"
    assert result.id == 1  # Agora deve passar
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()

def test_create_task_with_empty_title(mock_db_session):
    """Testa a tentativa de criar uma tarefa com título vazio"""
    task_data = TaskCreate(title="  ", description="Descrição válida")
    
    with pytest.raises(HTTPException) as exc_info:
        create_task(db=mock_db_session, task=task_data)
    
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "O título da tarefa não pode estar vazio" in str(exc_info.value.detail)
    mock_db_session.add.assert_not_called()
    mock_db_session.commit.assert_not_called()

def test_create_task_with_null_description(mock_db_session):
    """Testa a criação de tarefa com descrição nula"""
    task_data = TaskCreate(title="Tarefa válida", description=None)
    
    mock_task = Task(id=1, title="Tarefa válida", description=None)
    mock_db_session.add.return_value = None
    
    result = create_task(db=mock_db_session, task=task_data)
    
    assert result.description is None
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

def test_create_task_database_error(mock_db_session):
    """Testa o tratamento de erro do banco de dados"""
    task_data = TaskCreate(title="Tarefa válida", description="Descrição")
    
    # Configura o mock para simular um erro no banco de dados
    mock_db_session.commit.side_effect = SQLAlchemyError("Erro de banco de dados")
    
    with pytest.raises(HTTPException) as exc_info:
        create_task(db=mock_db_session, task=task_data)
    
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Erro ao salvar a tarefa no banco de dados" in str(exc_info.value.detail)
    mock_db_session.rollback.assert_called_once()

def test_create_task_unexpected_error(mock_db_session):
    """Testa o tratamento de erros inesperados"""
    task_data = TaskCreate(title="Tarefa válida", description="Descrição")
    
    # Configura o mock para simular um erro inesperado
    mock_db_session.add.side_effect = Exception("Erro inesperado")
    
    with pytest.raises(HTTPException) as exc_info:
        create_task(db=mock_db_session, task=task_data)
    
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Erro inesperado ao criar tarefa" in str(exc_info.value.detail)
