# FinanceAssistantAgent (aaas_platform)

An AI-driven, multi-agent financial assistant and automated trading intelligence platform (aaas_platform). Designed to process real-time market data, aggregate financial news, run risk evaluations, and provide both RESTful/WebSocket APIs and voice-enabled interactions.

## ARCHITECTURE OVERVIEW

```text
+-----------------------------------------------------------------+
|                       Client / Trading Bots                     |
|                 (REST API / WebSockets / Voice)                 |
+--------------------------------|--------------------------------+
                                 |
        +------------------------v------------------------+
        |                 API Layer (FastAPI)             |
        |        routes.py | websocket.py | server.py     |
        +------------------------v------------------------+
                                 |
        +------------------------v------------------------+
        |           Multi-Agent Core Network              |
        |  Main Support & Request Type Orchestrators      |
        |  Lead, Market & News Analysts + Risk Manager    |
        |  (Google ADK A2A Protocol & Local Llama 3)      |
        +------------------------v------------------------+
                                 |
        +------------------------+------------------------+
        |                                                 |
        v                                                 v
+-------------------------------+         +-------------------------------+
|    Data Pipeline (Ingestion)  |         |      Database & Caching       |
|  Market & News APIs           |         |  PostgreSQL (SQLAlchemy)      |
|  Kafka Producers & Consumers  |         |  Redis Cache                  |
+-------------------------------+         +-------------------------------+
```


## PROJECT DIRECTORY STRUCTURE

```text
aaas_platform/
├── api/                        # RESTful & WebSocket APIs
│   ├── routes.py               # FastAPI endpoints for external trading platform integration
│   ├── websocket.py            # Streaming endpoints for partial responses
│   └── server.py               # Server configuration and initialization
├── agents/                     # Multi-Agent Core Network
│   ├── orchestrators/
│   │   ├── main_support.py     # Main Support Agent
│   │   └── request_type.py     # Request Type Agent
│   ├── analysts/               # Delegated network of specialized analysts
│   │   ├── lead_analyst.py     # Lead Analyst
│   │   ├── market.py           # Market Analyst
│   │   └── news.py             # News Analyst
│   ├── risk/
│   │   └── risk_manager.py     # Risk Manager
│   ├── google_adk_config.py    # Google ADK setup for Agent-to-Agent (A2A) protocol
│   └── local_llama.py          # Llama 3 inference connector (e.g., via Ollama)
├── data_pipeline/              # Automated pipeline for aggregating external state data
│   ├── ingestion/              
│   │   ├── market_api.py       # Python Requests fetching free market data
│   │   └── news_api.py         # Python Requests fetching financial news
│   ├── kafka/                  
│   │   ├── producers.py        # Pushes data to Kafka message broker
│   │   └── consumers.py        # 30-minute interval polling and processing
├── database/                   
│   ├── models.py               # SQLAlchemy ORM for structured market data
│   ├── redis_cache.py          # Caches frequent user queries
│   └── session.py              # PostgreSQL database session management
├── voice/                      
│   └── speech_to_text.py       # Integration with ElevenLabs API
├── docker-compose.yml          # Local containerization for Postgres, Redis, Kafka, and Ollama
├── requirements.txt            # Python dependencies
└── main.py                     # Application entry point
```

## KEY COMPONENTS

--------------------------------------
1. Multi-Agent Core Network (agents/)
* Orchestrators (orchestrators/):
  - main_support.py: Routes incoming user/bot intents.
  - request_type.py: Classifies and delegates incoming analysis requests.
* Specialized Analysts (analysts/):
  - lead_analyst.py: Synthesizes market signals, news sentiment, and risk metrics into final action recommendations.
  - market.py: Analyzes price action, technical indicators, and market data feeds.
  - news.py: Parses incoming financial news streams for sentiment and macro shocks.
* Risk Management (risk/risk_manager.py):
  - Evaluates exposure limits, stop-loss thresholds, and volatility metrics before approving actions.
* LLM & Protocol Backbones:
  - google_adk_config.py: Implements Agent-to-Agent (A2A) communication protocols via Google ADK.
  - local_llama.py: Connects to local Llama 3 instances (via Ollama) for zero-latency, private inference.

--------------------------------------------
2. Automated Data Pipeline (data_pipeline/)
* Ingestion:
  - market_api.py & news_api.py fetch raw data from external APIs.
* Apache Kafka:
  - producers.py streams live tick and news events into the broker.
  - consumers.py executes 30-minute interval window polling, aggregation, and downsampling tasks.

---------------------------------
3. Storage & Caching (database/)
* models.py: SQLAlchemy schemas representing financial assets, historical bars, and agent decision logs.
* redis_cache.py: In-memory caching layer for frequent user queries and live session state.
* session.py: Manages PostgreSQL database connection pools and transactions.

------------------------------
4. Interfaces (api/ & voice/)
* FastAPI (api/routes.py, api/server.py): Core HTTP endpoints for trading bot integrations and query execution.
* WebSockets (api/websocket.py): Real-time streaming interface for token-by-token or partial analytical responses.
* Voice (voice/speech_to_text.py): Integrates ElevenLabs API for speech-to-text / voice command handling.

## PREREQUISITES & TECH STACK

* Python 3.10+
* Docker & Docker Compose (for PostgreSQL, Redis, Kafka, and Ollama)
* Ollama (running Llama 3 locally)
* Kafka & Zookeeper (via Docker Compose)

## QUICK START GUIDE

1. Clone & Configure Environment:
   git clone <repository-url>
   cd aaas_platform
   cp .env.example .env  # Configure your API keys (ElevenLabs, Market APIs, etc.)

2. Spin Up Infrastructure (Postgres, Redis, Kafka, Ollama):
   docker-compose up -d

3. Install Dependencies:
   pip install -r requirements.txt

4. Run the Application:
   python main.py

The FastAPI server will start on http://localhost:8000 (or configured port).
Access OpenAPI/Swagger docs at http://localhost:8000/docs.

## API ENDPOINTS & WEBSOCKETS

* REST API: See api/routes.py for trading bot hooks and agent query handlers.
* WebSocket Stream: Connect to /ws/stream (api/websocket.py) to receive live, streaming agent evaluation outputs.

## CONTRIBUTING

1. Create a feature branch: git checkout -b feature/amazing-feature
2. Commit your changes: git commit -m 'Add amazing feature'
3. Push to the branch: git push origin feature/amazing-feature
4. Open a Pull Request
