# Intellicloud Consumer

A Kafka consumer application that processes book messages and stores them in MongoDB.

## Features

- Kafka message consumption
- Book data processing
- MongoDB integration
- Docker containerization
- Python type hints and validation

## Project Structure

```
src/
├── __init__.py
├── main.py
├── consumer.py
├── models.py
└── mongodb_client.py
```

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Start the services:
```bash
docker compose up -d
```

## Environment Variables

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker address (default: kafka:9092)
- `KAFKA_GROUP_ID`: Consumer group ID (default: my_consumer_group)
- `KAFKA_TOPIC`: Kafka topic to consume from (default: my_topic)
- `MONGODB_URI`: MongoDB connection URI (default: mongodb://admin:admin@mongodb:27017)

## Usage

The consumer will automatically start processing messages from the specified Kafka topic and store them in MongoDB.

## Development

Run tests:
```bash
poetry run pytest
```

Format code:
```bash
poetry run black src/
``` 