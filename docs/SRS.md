# Software Requirements Specification — SENTINEL-AI

## 1. Introduction

SENTINEL-AI is an end-to-end violence detection pipeline for CCTV analytics. It receives video streams, estimates human pose, computes motion and proximity features, and raises alerts when aggressive behavior is detected.

## 2. Functional Requirements

| ID | Requirement | Phase |
|---|---|---|
| FR-01 | Ingest video from file, webcam, and RTSP streams | 1 / 3 |
| FR-02 | Detect and track human pose keypoints (YOLOv8-Pose) | 1 |
| FR-03 | Compute joint velocities and accelerations per person | 1 |
| FR-04 | Compute inter-person proximity using distance metrics | 1 |
| FR-05 | Classify frame threat level (Normal / Warning / Fight) | 2 |
| FR-06 | Render skeletal overlay and color-coded bounding boxes | 1 |
| FR-07 | Record 5-second incident clips | 3 |
| FR-08 | Dispatch Telegram/SMS alerts asynchronously | 3 |
| FR-09 | Persist incident logs in indexed database | 3 |
| FR-10 | Stream metadata via WebSockets to dashboard | 3 |

## 3. Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Inference latency on CPU | < 70 ms/frame |
| NFR-02 | End-to-end alert latency | < 1.5 seconds |
| NFR-03 | Accuracy on violence clips | > 85% precision/recall |
| NFR-04 | False positive rate on benign high-motion clips | < 15% |
| NFR-05 | Platform | Windows 10/11, Python 3.11 |
| NFR-06 | Deployability | Docker containerization |

## 4. System Constraints

- CPU-only target for edge feasibility; GPU acceleration optional.
- Open-source datasets only (Hockey Fights, RWF-2000, UCF-Crime).
- Explainable detection logic; no black-box dependence for Viva 1–2.

## 5. Use Cases

**UC-01 Live CCTV monitoring:** Security operator views multi-camera dashboard and receives instant alerts.

**UC-02 Post-incident audit:** Operator searches incident database by timestamp, camera, severity.

**UC-03 Offline video analysis:** Investigator uploads a clip and receives annotated output video.

## 6. Data Flow Diagrams

### DFD Level 0

```
[External Entity: CCTV Camera / File]
        → [Process: SENTINEL-AI Engine]
        → [Data Store: Incident DB]
        → [External Entity: Security Dashboard / Operator]
```

### DFD Level 1

```
Video Source → Ingest Module → Pose Estimator → Analytics Engine → Threat Classifier
                                                    ↓
                                            [Incident DB]
                                                    ↓
Alert Dispatcher ← WebSocket/HTTP ← Dashboard Renderer
```

## 7. Acceptance Criteria for Viva 1

- [ ] Repository scaffolded with modules and docs.
- [ ] CLI demo runs on a test video and prints keypoints + motion flags.
- [ ] Annotated output video saved with skeletal overlay.
- [ ] pytest unit tests pass for motion and proximity math.
