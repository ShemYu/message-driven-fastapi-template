from fastapi import APIRouter, HTTPException
from api.models import TaskCreate, Task
from api.config import settings
import aio_pika
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    try:
        # Create a new task with a unique ID
        task_id = str(uuid.uuid4())
        new_task = Task(
            id=task_id,
            title=task.title,
            description=task.description,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Connect to RabbitMQ and send task to queue
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        async with connection:
            channel = await connection.channel()
            await channel.declare_queue(settings.TASK_QUEUE, durable=True)
            
            message = aio_pika.Message(
                body=new_task.model_dump_json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            await channel.default_exchange.publish(
                message,
                routing_key=settings.TASK_QUEUE
            )
        
        return new_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
