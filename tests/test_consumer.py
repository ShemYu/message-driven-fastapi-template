import pytest
from unittest.mock import patch, MagicMock
from consumer.worker import process_task, handle_task_message
from api.models import Task
from datetime import datetime

@pytest.mark.asyncio
async def test_process_task():
    task = Task(
        id="test-id",
        title="Test Task",
        description="Test Description",
        status="pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    result = await process_task(task)
    assert result is True

@pytest.mark.asyncio
async def test_handle_task_message():
    # Create a mock message
    mock_message = MagicMock()
    mock_message.body.decode.return_value = '''
    {
        "id": "test-id",
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
    '''
    
    # Test the message handler
    await handle_task_message(mock_message)
    
    # Verify the message was processed
    mock_message.process.assert_called_once()
