import pytest
from fastapi.testclient import TestClient
from src.fastapi.app import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    """Limpa a lista de tarefas antes de cada teste"""
    from src.fastapi.app import tasks
    tasks.clear()
    yield
    tasks.clear()


def test_create_task():
    """Testa a criação de uma nova tarefa"""
    response = client.post(
        "/tasks/",
        json={"name": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Task"


def test_create_duplicate_task():
    """Testa se não é possível criar tarefas duplicadas"""
    client.post(
        "/tasks/",
        json={"name": "Test Task", "description": "Test Description"}
    )
    response = client.post(
        "/tasks/",
        json={"name": "Test Task", "description": "Another Description"}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_list_tasks():
    """Testa a listagem de tarefas"""
    client.post(
        "/tasks/",
        json={"name": "Task 1", "description": "Description 1"}
    )
    client.post(
        "/tasks/",
        json={"name": "Task 2", "description": "Description 2"}
    )
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_complete_task():
    """Testa a marcação de uma tarefa como concluída"""
    client.post(
        "/tasks/",
        json={"name": "Test Task", "description": "Test Description"}
    )
    response = client.put("/tasks/Test Task")
    assert response.status_code == 200
    assert "completed" in response.json()["message"]


def test_complete_task_not_found():
    """Testa a marcação de uma tarefa inexistente"""
    response = client.put("/tasks/NonExistent")
    assert response.status_code == 404


def test_delete_task():
    """Testa a deleção de uma tarefa"""
    client.post(
        "/tasks/",
        json={"name": "Test Task", "description": "Test Description"}
    )
    response = client.delete("/tasks/Test Task")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]


def test_delete_task_not_found():
    """Testa a deleção de uma tarefa inexistente"""
    response = client.delete("/tasks/NonExistent")
    assert response.status_code == 404
