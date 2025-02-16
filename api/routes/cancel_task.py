from fastapi import APIRouter, HTTPException
from api.models import Task
from api.config import settings
import aio_pika

router = APIRouter()

@router.post("/tasks/{task_id}/cancel", response_model=Task)
async def cancel_task(task_id: str):
    try:
        # In a real application, you would first check if the task exists
        # and if it's in a cancellable state
        
        # Send cancel message to queue
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            cancel_queue = f"{settings.TASK_QUEUE}.cancel"
            await channel.declare_queue(cancel_queue, durable=True)
            
            message = aio_pika.Message(
                body=task_id.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            await channel.default_exchange.publish(
                message,
                routing_key=cancel_queue
            )
        
        # For demonstration, return a mock cancelled task
        # In a real application, you would fetch and update the actual task
        return Task(
            id=task_id,
            title="Task cancelled",
            status="cancelled",
            created_at="2024-01-01T00:00:00",
            updated_at="2024-01-01T00:00:00"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
