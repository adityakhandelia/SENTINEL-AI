# System Architecture — SENTINEL-AI

## 1. High-Level Block Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Video Source   │────▶│   Ingest Layer   │────▶│  Pose Estimator │
│ (File/Webcam/   │     │ (OpenCV capture) │     │ (YOLOv8-Pose)   │
│  RTSP stream)   │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                              ┌───────────────────────────┘
                              ▼
                    ┌─────────────────────┐
                    │  Analytics Engine   │
                    │  · Joint velocity   │
                    │  · k-d Tree prox.   │
                    │  · IoU overlap      │
                    │  · Threat scoring   │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │  SQLite/     │ │  Async Alert │ │  WebSocket   │
      │  PostgreSQL  │ │  Dispatcher  │ │  JSON Stream │
      │  Incident DB │ │ (Redis/Celery│ │  (FastAPI)   │
      └──────────────┘ │   Phase 3)   │ └──────┬───────┘
                       └──────────────┘        │
                                               ▼
                                      ┌─────────────────┐
                                      │  React/Next.js  │
                                      │    Dashboard    │
                                      └─────────────────┘
```

## 2. Component Responsibilities

| Component | Technology | Responsibility |
|---|---|---|
| Ingest Layer | OpenCV | Capture frames from file, webcam, RTSP |
| Pose Estimator | YOLOv8-Pose | Detect persons and 17 keypoints per person |
| Analytics Engine | NumPy, SciPy KDTree | Compute velocity, proximity, IoU, threat score |
| Alert Dispatcher | Redis + Celery (Phase 3) | Send Telegram/SMS without blocking video |
| Database | SQLite → PostgreSQL | Indexed incident logs |
| API Server | FastAPI + WebSockets | Stream metadata to dashboard |
| Dashboard | Next.js (Phase 3) | Canvas overlays, incident replay, multi-camera grid |

## 3. Concurrency Model (Phase 3)

Producer thread decodes frames into a bounded `queue.Queue`. Consumer threads pull frames, run inference, and update shared state. Alerts are dispatched asynchronously to avoid blocking the video loop.

## 4. Data Contracts

**Pose output per frame:**

```json
{
  frame_id: 120,
  timestamp: 1.5,
  persons: [
    {
      track_id: 0,
      bbox: [x1, y1, x2, y2],
      keypoints: [[x, y, conf], ...],
      confidence: 0.91
    }
  ]
}
```

**Threat metadata per frame:**

```json
{
  frame_id: 120,
  threat_level: warning,
  score: 0.72,
  active_pairs: [[0, 1]],
  max_velocity: 145.3
}
```

## 5. Phase Map

- **Phase 1 (Viva 1):** Ingest → Pose → Basic Analytics → Renderer → CLI Demo
- **Phase 2 (Viva 2):** k-d Tree optimization, temporal window, heuristic classifier
- **Phase 3 (Viva 3):** Threading, FastAPI/WebSocket, SQLite, React dashboard, alerts
- **Phase 4 (Viva 4):** Benchmarking, Docker, final report, paper draft
