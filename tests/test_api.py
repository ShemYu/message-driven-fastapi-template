from fastapi.testclient import TestClient
from api.main import app
import pytest
from unittest.mock import patch

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
@patch('aio_pika.connect_robust')
async def test_create_task(mock_connect):
    # Mock the RabbitMQ connection and channel
    task_data = {
        "title": "Test Task",
        "description": "This is a test task"
    }
    
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    assert response.json()["title"] == task_data["title"]
    assert response.json()["description"] == task_data["description"]
    assert response.json()["status"] == "pending"

@pytest.mark.asyncio
@patch('aio_pika.connect_robust')
async def test_cancel_task(mock_connect):
    # Mock the RabbitMQ connection and channel
    task_id = "test-task-id"
    
    response = client.post(f"/tasks/{task_id}/cancel")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["status"] == "cancelled"
