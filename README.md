# Aetheria Vertical AI Platform

> Production-quality, open-source Vertical AI Knowledge Graph platform with 8 domain-specific verticals, multi-agent orchestration, and cross-vertical reasoning.

## Features

- **8 Vertical Domains**: Healthcare, Legal, Finance, Education, Customer Service, Manufacturing, Agriculture, Research
- **Domain-Specific NLP**: Custom entity extraction, relation extraction, knowledge reasoning per vertical
- **Multi-Agent Orchestration**: Cross-vertical queries with intelligent routing
- **Plugin Architecture**: Easily add new vertical domains
- **Benchmark Suite**: Evaluation framework for each vertical
- **Docker Deployment**: Full docker-compose with all services
- **CI/CD**: GitHub Actions for testing and deployment
- **200+ Tests**: Comprehensive test coverage

## Architecture

```
aetheria-vert/
├── src/aetheria/
│   ├── core/              # Core framework
│   │   ├── __init__.py
│   │   ├── engine.py      # Query engine
│   │   ├── orchestrator.py # Multi-agent orchestrator
│   │   ├── plugin_base.py  # Plugin architecture
│   │   └── reasoner.py     # Knowledge reasoner
│   ├── verticals/          # Domain-specific verticals
│   │   ├── healthcare/
│   │   ├── legal/
│   │   ├── finance/
│   │   ├── education/
│   │   ├── customer_service/
│   │   ├── manufacturing/
│   │   ├── agriculture/
│   │   └── research/
│   └── benchmark/          # Evaluation suite
├── tests/                  # 200+ tests
├── docs/                   # Documentation
├── .github/workflows/      # CI/CD
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Quick Start

```bash
pip install -e .
python -m pytest tests/ -q
docker compose up -d
```

## License

MIT
