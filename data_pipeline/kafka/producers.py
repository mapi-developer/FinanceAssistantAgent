from kafka import KafkaProducer
import json
from data_pipeline.ingestion.market_api import fetch_live_market_data

# Initialize Kafka Producer pointing to localhost broker
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def run_market_producer():
    """Fetches data and pushes it to the Kafka topic."""
    market_payloads = fetch_live_market_data()
    
    for data in market_payloads:
        producer.send('market_ingestion', data)
        print(f"📤 [KAFKA PRODUCER] Published {data['ticker']} @ ${data['price']}")
        
    producer.flush()