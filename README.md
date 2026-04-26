# Pattern Printer

A small full-stack pattern generator. The backend renders 31 text patterns through a JSON API, and the frontend gives the old CLI a clean modern interface.

## Project Structure

```txt
PatternPrinter/
├── backend/
│   ├── cli.py
│   ├── patterns.py
│   └── server.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── DEPLOYMENT.md
├── render.yaml
└── README.md
```

## Run the Web App

```bash
python3 -m backend.server
```

Open http://127.0.0.1:8000.

## API

- `GET /api/patterns` lists available patterns.
- `GET /api/render?pattern=hill&symbol=*&size=8` renders a pattern.
- Rectangle patterns also accept `width` and `height`.

## CLI

```bash
python3 -m backend.cli
```

## Deploy

See [DEPLOYMENT.md](DEPLOYMENT.md).
