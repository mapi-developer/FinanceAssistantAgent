from kafka import KafkaConsumer
import json
from database.session import SessionLocal, engine
from database.models import Base, MarketData
from database.redis_cache import cache_latest_price

# Ensure database tables are created
Base.metadata.create_all(bind=engine)

def run_market_consumer():
    """Listens to Kafka, caches to Redis, and saves to PostgreSQL."""
    print("📥 [KAFKA CONSUMER] Listening for market data...")
    
    consumer = KafkaConsumer(
        'market_ingestion',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    db = SessionLocal()
    
    try:
        for message in consumer:
            data = message.value
            ticker = data['ticker']
            
            # 1. Write to Redis (Fast access for Analytical Agents)
            cache_latest_price(ticker, data)
            
            # 2. Write to PostgreSQL (Historical persistence)
            new_record = MarketData(
                ticker=ticker,
                price=data['price'],
                volume=data['volume']
            )
            db.add(new_record)
            db.commit()
            
            print(f"💾 [DB SAVED] {ticker} inserted into PostgreSQL & Redis.")
            
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        db.close()

if __name__ == "__main__":
    run_market_consumer()