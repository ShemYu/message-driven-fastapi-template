# Message-Driven FastAPI Template

A high-performance API template designed for building scalable, message-driven services. Built on FastAPI with full support for asynchronous operations, this template leverages modern message queues to ensure smooth, non-blocking communication between components.

## Project Structure

```
project-root/
├── api/
│   ├── main.py              # Entry point for the FastAPI application
│   ├── routes/
│   │   ├── create_task.py   # API route for creating a new task
│   │   └── cancel_task.py   # API route for canceling an existing task
│   ├── models.py            # Database models (e.g., Task)
│   └── config.py            # Configuration for DB and message queue settings
├── consumer/
│   └── worker.py            # Worker that consumes tasks from the message queue and processes them
├── tests/
│   ├── test_api.py          # Unit tests for API endpoints
│   └── test_consumer.py     # Unit tests for consumer logic
├── docker-compose.yml       # Docker Compose configuration for API, DB, message queue, and consumer services
├── Dockerfile               # Dockerfile for building the FastAPI service
└── README.md                # Project documentation
```

## Components

### API Service
- **main.py**: FastAPI application entry point
- **routes/**: Contains API endpoint definitions
  - `create_task.py`: Handles task creation requests
  - `cancel_task.py`: Handles task cancellation requests
- **models.py**: Database models and schemas
- **config.py**: Application configuration settings

### Consumer Service
- **worker.py**: Message queue consumer that processes tasks

### Tests
- **test_api.py**: API endpoint unit tests
- **test_consumer.py**: Consumer logic unit tests

### Docker
- **docker-compose.yml**: Multi-container Docker setup
- **Dockerfile**: Container definition for the FastAPI service

## Usage

### Starting Services with Docker Compose

1. Start all services (API, DB, message queue) using Docker Compose:
```bash
docker compose up --build
```

### Starting the Consumer

1. Activate your Python virtual environment (if using one)

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Start the consumer manually to process messages from the queue:
```bash
python -m consumer.worker
```

The consumer will now listen for and process messages from the queue. You can run multiple consumer instances if needed for increased processing capacity.


