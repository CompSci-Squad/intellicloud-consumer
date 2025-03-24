import logging
from consumer import KafkaMessageConsumer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the Kafka consumer application.
    """
    try:
        # Initialize the consumer
        consumer = KafkaMessageConsumer()
        
        # Start consuming messages
        logger.info("Starting Kafka consumer...")
        consumer.run()
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        raise

if __name__ == "__main__":
    main()
