# SENTINEL-AI — Mentor Progress Update & Pitch

## 30-Second Elevator Pitch

SENTINEL-AI is a real-time, pose-based violence detection system for CCTV analytics. Instead of heavy 3D-CNNs that need GPUs, we extract 17 lightweight 2D skeletal keypoints per person using YOLOv8-Pose and apply explainable motion heuristics — velocity, proximity, and bounding-box overlap — to flag physical fights within seconds. It runs on CPU, is fully explainable, and is designed as an end-to-end production pipeline.

## Problem

- Cities have millions of CCTV cameras but human operators miss ~95% of incidents due to fatigue.
- Average response time to fights/assaults is 8–15 minutes.
- Existing deep-learning solutions (3D-CNNs, Vision Transformers) need high-end GPUs and run >150 ms/frame, making multi-camera CPU deployment impossible.

## Our Approach

1. **Pose Extraction:** YOLOv8-Pose → 17 keypoints per person.
2. **Motion Analysis:** Frame-to-frame joint velocity (focus on wrists) → suspicious motion flag.
3. **Proximity Analysis:** Distance between person centroids → close-pair flag.
4. **Threat Decision:**
   - NORMAL: low velocity
   - WARNING: high velocity, no close person
   - FIGHT: high velocity + close person
5. **Output:** Annotated video with skeletal overlays + bounding boxes color-coded green/yellow/red.

## What Is Built (Viva 1)

- Repository scaffold with modular backend (`ingest`, `vision`, `analytics`, `alerts`, `api`, `db` placeholders).
- Working CLI demo: `python backend/cli_demo.py --source <video> --output <annotated>`.
- Simple Streamlit web UI: `streamlit run frontend/app.py`.
- pytest unit tests: 5/5 passing.
- Documentation: SRS, literature survey, research gaps, architecture.
- Slide deck for Viva 1.
- GitHub repo: https://github.com/adityakhandelia/SENTINEL-AI

## Tech Stack

- Python 3.11, OpenCV, Ultralytics YOLOv8-Pose, NumPy, SciPy
- Streamlit (Viva 1 UI) → Next.js + FastAPI/WebSockets (Phase 3)
- SQLite → PostgreSQL, Redis + Celery for alerts (Phase 3)

## Research Gaps We Address

1. **Computational overhead:** Pose reduces dimensionality by 90% vs 3D-CNNs, enabling CPU real-time.
2. **False positives:** We combine spatial proximity with joint acceleration to distinguish fights from running/hugging/dancing.
3. **System integration:** Most papers stop at offline benchmarks; we are building a multi-threaded streaming pipeline with alerts and dashboard.

## Demo Script (3 minutes)

1. Open the GitHub repo and show the README + architecture diagram.
2. Run `python scripts/health_check.py` — show 6/6 PASS and 5/5 pytest.
3. Run `streamlit run frontend/app.py`.
4. In the browser upload `data/raw/people_walking_demo.mp4`.
5. Click Analyze Video and show:
   - Progress bar and live status
   - Metrics (frames, max persons, peak velocity)
   - Threat timeline chart
   - Annotated output video with green skeletons
6. Explain that a fight clip would show WARNING (yellow) or FIGHT (red).
7. Show the Viva 1 slide deck.

## Results

- Health check: 6/6 PASS
- Unit tests: 5/5 PASS
- CLI end-to-end demo: working on CPU
- Annotated output video generated successfully

## Roadmap

| Phase | Timeline | Focus |
|---|---|---|
| Viva 1 | Now | Pose + docs + CLI + Streamlit demo |
| Viva 2 | Month 4-5 | k-d Tree, IoU, temporal window, benchmarks |
| Viva 3 | Month 7-8 | Threading, FastAPI/WebSockets, React UI, SQLite, alerts |
| Viva 4 | Month 10-11 | Dataset evaluation, Docker, report, paper draft |

## Current Limitations & Mitigations

- No person tracking yet → IDs can swap; Phase 2 adds temporal consistency.
- Naive O(N²) proximity → Phase 2 replaces with k-d Tree O(N log N).
- CPU throughput ~3-6 FPS at 768x432 → Phase 3 adds threaded producer-consumer queues.

## Likely Mentor Questions

**Q: Why not use a 3D-CNN?**
A: 3D-CNNs need GPUs and run >150 ms/frame. Our pose approach reduces input size by 90% and runs on CPU.

**Q: How do you distinguish a hug from a fight?**
A: Hugging has low kinetic variance and sustained close proximity. Fights show rapid, multi-directional limb acceleration and irregular bounding-box overlap.

**Q: What dataset will you benchmark on?**
A: Hockey Fights for quick validation; RWF-2000 for final metrics in Viva 4.

**Q: How will alerts avoid freezing the video feed?**
A: Redis + Celery async task queue in Phase 3.

**Q: Are you fine-tuning the model?**
A: Not for Viva 1. YOLOv8-Pose is COCO-pretrained and works well. We may add a lightweight LSTM on keypoint sequences in Phase 2 for research depth, but the core stays explainable and CPU-friendly.

## Ask from Mentor

- Feedback on the heuristic vs learned-classifier balance.
- Suggestions for datasets accessible to us.
- Guidance on whether to add an LSTM/GRU in Phase 2 for research depth.
