from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/db"
    
    # Message Queue settings
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    TASK_QUEUE: str = "task_queue"
    
    class Config:
        env_file = ".env"

settings = Settings()
