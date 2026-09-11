# Aetheria Vertical AI Knowledge Graph — Web Dashboard

The flagship open-source frontend for the Aetheria Vertical AI Knowledge Graph platform.

## Features

- **Real-time Knowledge Graph Visualization** — Interactive D3.js-powered graph explorer
- **Query Interface** — Search across all 8 vertical domains
- **Domain Selector** — Switch between Healthcare, Legal, Finance, Education, Customer Service, Manufacturing, Agriculture, and Research
- **REST API Client** — Built-in API tester with endpoint discovery
- **Documentation Site** — MkDocs-style integrated docs
- **Plugin UI** — Extensible architecture for adding new verticals
- **Dark/Light Mode** — Modern UI with theme support

## Quick Start

```bash
pip install -r requirements.txt
python -m uvicorn aetheria_dashboard.app:create_app --reload
```

Open http://localhost:8000 in your browser.

## Running Tests

```bash
pytest tests/ -v
```

## Architecture

```
aetheria_dashboard/
├── app.py              # FastAPI application factory
├── routers/
│   ├── graph.py        # KG explorer API
│   ├── query.py        # Query interface API
│   ├── verticals.py    # Vertical domains API
│   ├── api_client.py   # REST API client
│   └── docs.py         # Documentation API
├── static/
│   ├── css/style.css   # Dark theme styles
│   └── js/
│       ├── graph.js    # D3.js visualization
│       ├── query.js    # Query interface
│       ├── verticals.js
│       ├── api_client.js
│       └── docs.js
└── templates/          # Jinja2 HTML templates
```

## License

MIT
