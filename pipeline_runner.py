import time
import schedule
from data_pipeline.kafka.producers import run_market_producer

def job():
    print("\n--- 🔄 Triggering 5-Minute ETL Cycle ---")
    run_market_producer()

if __name__ == "__main__":
    print("🚀 Starting Data Pipeline Scheduler (5-minute intervals)...")
    
    # Run once immediately on startup
    job()
    
    # Schedule every 5 minutes
    schedule.every(5).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)