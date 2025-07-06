import os, sys
import pytest

from fastapi import status, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import MagicMock
from datetime import datetime


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Task
from app.schemas import TaskCreate
from app.crud import create_task, get_tasks, get_task, update_task, delete_task

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
    assert result.id == 1
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



def test_get_tasks_success(mock_db_session):
    """Testa a recuperação bem-sucedida de uma lista de tarefas"""
    # Arrange
    mock_tasks = [
        Task(id=1, title="Tarefa 1", description="Desc 1", created_at=datetime.now()),
        Task(id=2, title="Tarefa 2", description="Desc 2", created_at=datetime.now())
    ]
    # Simula a cadeia de chamadas do SQLAlchemy
    (mock_db_session.query.return_value
     .order_by.return_value
     .offset.return_value
     .limit.return_value
     .all.return_value) = mock_tasks

    # Act
    result = get_tasks(db=mock_db_session, skip=0, limit=10)

    # Assert
    assert len(result) == 2
    assert result[0].title == "Tarefa 1"
    assert result[1].id == 2
    mock_db_session.query.assert_called_once_with(Task)
    
    
def test_get_tasks_with_invalid_limit(mock_db_session):
    """Testa a falha ao tentar recuperar tarefas com um limite inválido"""
    # Arrange
    limit_invalido = -5

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_tasks(db=mock_db_session, skip=0, limit=limit_invalido)

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "O parâmetro 'limit' deve estar entre 1 e 1000" in str(exc_info.value.detail)
    mock_db_session.query.assert_not_called()
    
    
def test_get_task_success(mock_db_session):
    """Testa a busca bem-sucedida de uma única tarefa pelo ID"""
    # Arrange
    mock_task = Task(id=1, title="Tarefa Encontrada", description="Detalhes", created_at=datetime.now())
    (mock_db_session.query.return_value
     .filter.return_value
     .first.return_value) = mock_task

    # Act
    result = get_task(db=mock_db_session, task_id=1)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.title == "Tarefa Encontrada"
    mock_db_session.query.assert_called_once_with(Task)
    
def test_get_task_not_found(mock_db_session):
    """Testa o comportamento quando uma tarefa com o ID especificado não é encontrada"""
    # Arrange
    (mock_db_session.query.return_value
     .filter.return_value
     .first.return_value) = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_task(db=mock_db_session, task_id=999)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "Tarefa com ID 999 não encontrada" in str(exc_info.value.detail)


def test_update_task_success(mock_db_session):
    """Testa a atualização bem-sucedida de uma tarefa existente"""
    # Arrange
    existing_task = Task(id=1, title="Título Antigo", description="Descrição Antiga")
    update_data = TaskCreate(title="  Título Novo  ", description="Descrição Nova")
    
    (mock_db_session.query.return_value
     .filter.return_value
     .first.return_value) = existing_task

    # Act
    result = update_task(db=mock_db_session, task_id=1, task=update_data)

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.title == "Título Novo"  # Verifica se o .strip() funcionou
    assert result.description == "Descrição Nova"
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(existing_task)
    mock_db_session.rollback.assert_not_called()
    
    
def test_update_task_not_found(mock_db_session):
    """Testa a tentativa de atualizar uma tarefa que não existe"""
    # Arrange
    update_data = TaskCreate(title="Título Novo", description="Descrição Nova")
    (mock_db_session.query.return_value
     .filter.return_value
     .first.return_value) = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        update_task(db=mock_db_session, task_id=999, task=update_data)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "Tarefa com ID 999 não encontrada" in str(exc_info.value.detail)
    mock_db_session.commit.assert_not_called()
    mock_db_session.rollback.assert_not_called()
    
    
    
def test_delete_task_success(mock_db_session):
    """Testa a exclusão bem-sucedida de uma tarefa"""
    # Arrange
    task_to_delete = Task(id=1, title="Tarefa para deletar", description="Adeus")
    (mock_db_session.query.return_value
     .filter.return_value
     .first.return_value) = task_to_delete

    # Act
    result = delete_task(db=mock_db_session, task_id=1)

    # Assert
    assert result is not None
    assert result.id == 1
    mock_db_session.delete.assert_called_once_with(task_to_delete)
    mock_db_session.commit.assert_called_once()
    mock_db_session.rollback.assert_not_called()


def test_delete_task_database_error_on_commit(mock_db_session):
    """Testa o tratamento de erro do DB durante o commit da exclusão"""
    # Arrange
    task_to_delete = Task(id=1, title="Tarefa para deletar", description="Adeus")
    (mock_db_session.query.return_value
     .filter.return_value
     .first.return_value) = task_to_delete

    mock_db_session.commit.side_effect = SQLAlchemyError("Erro de integridade referencial")

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        delete_task(db=mock_db_session, task_id=1)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Erro ao excluir a tarefa do banco de dados" in str(exc_info.value.detail)
    mock_db_session.delete.assert_called_once_with(task_to_delete)
    mock_db_session.commit.assert_called_once()
    mock_db_session.rollback.assert_called_once()