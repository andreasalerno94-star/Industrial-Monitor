![Dashboard](dashboard.png)
# Industrial Monitor Dashboard

Real-time monitoring dashboard for industrial wire bonding machines, built with Python Flask and Chart.js.

## Overview

Industrial Monitor simulates and visualizes sensor data from 8 machines in real time, with an alarm system and historical alarm logging. Designed to replicate the kind of monitoring tools used in semiconductor manufacturing environments.

## Features

- **Real-time dashboard** — 8 machine cards updated every 2 seconds
- **Multi-sensor monitoring** — Temperature (°C), Vacuum (mBar), Overpressure (Bar), Vibration (g)
- **Alarm system** — per-machine alarm logic with warning and maintenance stop states
- **Focus mode** — click any machine to view its full sensor history chart
- **Interactive chart** — pause on hover, crosshair, tooltip with real values
- **Alarm history** — SQLite database with filterable table and bar chart
- **Retention policy** — automatic cleanup of records older than 7 days

## Tech Stack

- **Backend:** Python, Flask, SQLite, Gunicorn
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Architecture:** REST API + polling frontend
- **Deployment:** Docker, Docker Compose

## How to Run

### With Docker (recommended)

```bash
docker volume create alarms-data
docker compose up -d --build
```

Then open `http://localhost:8080` in your browser.

Alarm history is persisted in a named Docker volume mounted at `/data`, so it
survives container restarts and rebuilds. Configuration (`DB_PATH`, `PORT`) is
injected via environment variables, so the same image runs unchanged in any
environment.

Useful commands:

```bash
docker compose ps        # status + healthcheck state
docker compose logs -f   # follow logs
docker compose down      # stop and remove (volume is kept)
```

### Locally (development)

```bash
pip3 install -r requirements.txt
python3 app.py
```

Then open `http://127.0.0.1:5000` in your browser.
On macOS port 5000 is used by AirPlay Receiver — use `PORT=5001 python3 app.py`
if it is occupied.

## Container Design Notes

- **Slim base image** (`python:3.12-slim`) to reduce image size and attack surface
- **Non-root runtime user** following least-privilege principles
- **Layer-cache-friendly build**: dependencies are copied and installed before
  application code, so code changes do not invalidate the `pip install` layer
- **Pinned dependency versions** for reproducible builds
- **Healthcheck** so the orchestrator can distinguish "process running" from
  "service actually responding"
- **Production WSGI server** (Gunicorn) instead of the Flask development server

## Background

This project was built as a learning exercise to apply Python and web development skills in a domain I know well — industrial machine maintenance in semiconductor manufacturing.
