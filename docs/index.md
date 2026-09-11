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

## API

```python
from aetheria.core import MultiAgentOrchestrator
from aetheria.verticals.healthcare import HealthcarePlugin

# Create orchestrator
orch = MultiAgentOrchestrator()

# Register plugins
orch.register_plugin(HealthcarePlugin())

# Process text
result = orch.process("Patient has diabetes and takes metformin")

# Query
result = orch.query("diabetes treatment")
print(result.answer)
```

## License

MIT
