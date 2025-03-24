import json
from confluent_kafka import Consumer, KafkaError
import logging
from typing import Dict, Any
import os
from models import Book
from mongodb_client import MongoDBClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KafkaMessageConsumer:
    def __init__(self):
        """
        Initialize the Kafka consumer using environment variables
        """
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.group_id = os.getenv('KAFKA_GROUP_ID', 'default_group')
        self.topic = os.getenv('KAFKA_TOPIC', 'default_topic')
        
        self.consumer = Consumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        })
        
        # Subscribe to the topic
        self.consumer.subscribe([self.topic])

    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process a single message. Override this method in subclasses.
        
        Args:
            message: Parsed message dictionary
        """
        # Add your message processing logic here
        pass

    def consume_messages(self, timeout: float = 1.0) -> None:
        """
        Consume messages from Kafka
        
        Args:
            timeout: Poll timeout in seconds
        """
        try:
            while True:
                msg = self.consumer.poll(timeout)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.info(f"Reached end of partition {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                    else:
                        logger.error(f"Error while consuming: {msg.error()}")
                    continue

                try:
                    # Parse the message value as JSON
                    message_value = json.loads(msg.value().decode('utf-8'))
                    
                    # Process the message
                    self.process_message(message_value)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

        except KeyboardInterrupt:
            logger.info("Shutting down consumer...")
        finally:
            self.consumer.close()

    def run(self) -> None:
        """
        Start consuming messages
        """
        try:
            self.consume_messages()
        except Exception as e:
            logger.error(f"Consumer failed: {e}")
            raise

class BookConsumer(KafkaMessageConsumer):
    def __init__(self):
        """
        Initialize the Kafka consumer using environment variables
        """
        super().__init__()
        
        # Initialize MongoDB client
        self.mongo_client = MongoDBClient(os.getenv('MONGODB_URI'))

    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process a book message and store it in MongoDB
        
        Args:
            message: Parsed message dictionary containing book data
        """
        try:
            # Parse the message into a Book model
            book = Book(**message)
            
            # Save the book to MongoDB
            success = self.mongo_client.save_book(book)
            
            if success:
                logger.info(f"Successfully saved book: {book.title}")
            else:
                logger.info(f"Book already exists: {book.title}")
                
        except Exception as e:
            logger.error(f"Error processing book message: {e}", exc_info=True)

if __name__ == "__main__":
    consumer = BookConsumer()
    consumer.run()
