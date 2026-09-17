# AGENTS.md — SENTINEL-AI

This file contains context for AI coding assistants working on the SENTINEL-AI project.

## Project Overview

SENTINEL-AI is a final-year capstone project: a real-time, pose-based violence and anomalous behavior detection system for CCTV analytics. It extracts 2D skeletal keypoints using YOLOv8-Pose and applies explainable heuristics (velocity, proximity, IoU) to detect physical aggression.

## Repository Structure

- `backend/app/ingest/` — video capture (file, webcam, RTSP)
- `backend/app/vision/` — YOLOv8-Pose wrapper and skeletal renderer
- `backend/app/analytics/` — motion, proximity, and threat scoring
- `backend/app/api/` — FastAPI + WebSocket server (Phase 3)
- `backend/app/alerts/` — Telegram/SMS dispatch (Phase 3)
- `backend/app/db/` — SQLite/PostgreSQL incident logging (Phase 3)
- `backend/tests/` — pytest unit tests
- `frontend/` — Next.js dashboard (Phase 3)
- `scripts/` — dataset downloaders and benchmark runners
- `docs/` — SRS, literature survey, research gaps, architecture, viva material
- `data/raw/` — input test videos
- `data/processed/` — annotated output videos

## Tech Stack

- Python 3.11+
- OpenCV, Ultralytics YOLOv8-Pose, NumPy, SciPy
- FastAPI, WebSockets, Redis, Celery (Phase 3)
- SQLite → PostgreSQL (Phase 3)
- Next.js, React, Tailwind CSS (Phase 3)

## Build & Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
python -m pytest backend/tests
python backend/cli_demo.py --source data/raw/fight.mp4 --output data/processed/fight_annotated.mp4
```

## Conventions

- Use type hints where practical.
- Keep modules small and single-responsibility.
- Write pytest tests for pure math/util functions.
- Do not commit model weights or large videos.
- Avoid emojis in source files and docs.
- Keep the UI-agnostic JSON contract stable for frontend integration.

## Current Phase

Viva 1 (Phase 1): working pose extraction + CLI demo + documentation.

## Contact

Team: [names]
Mentor: [name]
