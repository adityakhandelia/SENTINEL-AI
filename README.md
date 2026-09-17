# SENTINEL-AI: Pose-Based Real-Time Violence & Anomaly Detection

**Domain:** Computer Vision · Distributed Systems · Public Safety Tech

SENTINEL-AI analyzes live CCTV or pre-recorded video, extracts lightweight 2D skeletal keypoints using YOLOv8-Pose, and flags physical violence via explainable motion heuristics.

## Why This Approach

- **90% dimensionality reduction:** 17 keypoints per person instead of full RGB frames.
- **CPU real-time:** yolov8n-pose runs at 10–20 FPS on commodity laptops.
- **Explainable decisions:** velocity spikes + proximity + bounding-box overlap, not a black-box classifier.

## Quick Start (Windows)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
python -m pytest backend/tests
python backend/cli_demo.py --source data/raw/fight.mp4 --output data/processed/fight_annotated.mp4
```

## Streamlit UI (Viva 1 Demo)

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

Open the URL shown in the terminal, upload a short video, and click Analyze Video.

## Repository Layout

```
aegis-vision/
├── backend/
│   ├── app/
│   │   ├── ingest/      # video capture
│   │   ├── vision/      # pose estimation + rendering
│   │   ├── analytics/   # motion + proximity scoring
│   │   ├── alerts/      # Telegram/SMS (Phase 3)
│   │   ├── api/         # FastAPI + WebSockets (Phase 3)
│   │   └── db/          # incident logging (Phase 3)
│   └── tests/
├── frontend/            # Streamlit UI (Viva 1), Next.js dashboard (Phase 3)
├── scripts/             # dataset downloaders, benchmark runners
├── data/                # test videos (gitignored)
└── docs/                # SRS, literature survey, research gaps
```

## Phase Map

| Phase | Focus | Viva |
|---|---|---|
| 1 | Pose extraction, docs, CLI demo | Viva 1 |
| 2 | k-d tree, IoU, temporal heuristics, benchmarks | Viva 2 |
| 3 | Threading, FastAPI/WebSockets, React UI, SQLite | Viva 3 |
| 4 | Dataset evaluation, Docker, report, paper draft | Viva 4 |

## Team

- [Member 1] — Computer Vision & Analytics
- [Member 2] — Backend Systems & Concurrency
- [Member 3] — Frontend & DevOps

Mentor: [Mentor Name]
