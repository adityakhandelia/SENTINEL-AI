# Viva 1 Presentation Material — SENTINEL-AI

## Slide 1: Title

**SENTINEL-AI: Pose-Estimation & Spatial Graph Analytics for Real-Time Violence Detection in CCTV Feeds**

Team: [names]
Mentor: [name]

## Slide 2: Problem Statement

- Cities have millions of CCTV cameras but human operators miss ~95% of incidents.
- Average response time to fights/assault is 8–15 minutes.
- Manual monitoring is not scalable and suffers from fatigue-induced errors.

## Slide 3: Proposed Solution

- Replace heavy 3D-CNNs with lightweight 2D pose estimation (17 keypoints per person).
- Use explainable heuristics: joint velocity spikes + inter-person proximity + bounding-box overlap.
- Build an end-to-end pipeline: ingest → pose → analytics → alerts → dashboard.

## Slide 4: Literature Survey & Research Gaps

1. **Computational Overhead Gap:** 3D-CNNs and Vision Transformers need GPUs and run >150 ms/frame on CPU.
2. **False-Positive Gap:** Optical-flow methods confuse running, dancing, or hugging with violence.
3. **Integration Gap:** Most work stops at offline dataset benchmarks; real-time streaming, concurrency, and alerting are rarely addressed.

## Slide 5: System Architecture

Use the block diagram from `docs/ARCHITECTURE.md`.

## Slide 6: Methodology

1. **Pose Extraction:** YOLOv8-Pose detects persons and 17 keypoints.
2. **Motion Analysis:** Frame-to-frame velocity and acceleration of wrists, elbows, and head.
3. **Proximity Analysis:** Distance between person centroids per frame.
4. **Threat Scoring:** In Phase 2, k-d Tree neighbor search + IoU + temporal window will classify Normal / Warning / Fight.

## Slide 7: Viva 1 Deliverables

- Repository scaffolded with modules and docs.
- Working CLI demo on normal and fight test videos.
- Annotated output video with skeletal overlay and bounding boxes.
- pytest unit tests for motion and proximity math.
- SRS, literature survey, research gaps, and architecture documents.

## Slide 8: Demo Script

1. Run CLI demo on a normal clip; show green/normal flags.
2. Run CLI demo on a fight clip; show high velocity values and red flags.
3. Optionally show live webcam overlay briefly to prove real-time feasibility.

## Likely Questions & Winning Answers

**Q: Why not use a 3D-CNN?**
A: 3D-CNNs need GPUs and run slower than 150 ms/frame on CPU. Our pose approach reduces input dimensionality by 90% and runs at 10–20 FPS on commodity hardware.

**Q: How do you distinguish a hug from a fight?**
A: Hugging shows low kinetic variance and sustained close proximity. Fights show rapid, multi-directional limb acceleration and irregular bounding-box overlap.

**Q: What is the role of k-d Trees?**
A: k-d Trees will replace naive O(N²) proximity checks in Phase 2, giving O(N log N) neighbor queries for crowded scenes.

**Q: What datasets will you use?**
A: Hockey Fights for quick validation in Viva 1–2; RWF-2000 for final benchmarking in Viva 4.

**Q: How will alerts avoid freezing the video feed?**
A: Redis + Celery background tasks in Phase 3 will dispatch Telegram/SMS asynchronously so HTTP latency does not block the video loop.

## Notes for the Presenter

- Keep the live demo under 2 minutes.
- Pre-compute annotated videos as a fallback in case webcam fails.
- Emphasize CPU-only feasibility because that directly validates Research Gap 1.
