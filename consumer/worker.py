import asyncio
import aio_pika
import json
from api.config import settings
from api.models import Task

async def process_task(task: Task):
    """
    Process the task. This is where you would implement your actual task processing logic.
    """
    # Simulate some work
    await asyncio.sleep(5)
    return True

async def handle_task_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            # Parse the task data
            task_data = json.loads(message.body.decode())
            task = Task(**task_data)
            
            # Process the task
            success = await process_task(task)
            
            if success:
                print(f"Successfully processed task {task.id}")
            else:
                print(f"Failed to process task {task.id}")
                
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            # In production, you might want to send this to a dead letter queue

async def main():
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            # Connect to RabbitMQ
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            print(f"Successfully connected to RabbitMQ on attempt {attempt + 1}")
            
            async with connection:
                # Create channel
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=1)
                
                # Declare queue
                queue = await channel.declare_queue(
                    settings.TASK_QUEUE,
                    durable=True
                )
                
                print(" [*] Waiting for messages. To exit press CTRL+C")
                
                # Start consuming messages
                await queue.consume(handle_task_message)
                
                try:
                    # Wait until terminate
                    await asyncio.Future()
                except asyncio.CancelledError:
                    pass
                
            # If we get here, the connection was successful and we're done
            return
            
        except Exception as e:
            print(f"Failed to connect on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                print("Max retries reached. Exiting...")
                raise


if __name__ == "__main__":
    asyncio.run(main())
