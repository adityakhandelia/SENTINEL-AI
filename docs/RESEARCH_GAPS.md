# Research Gaps Addressed by SENTINEL-AI

## Gap 1: Computational Overhead & Latency

**Current State:** 3D-CNN and Vision Transformer models process full RGB pixel volumes, requiring high-end GPUs and producing inference latencies above 150 ms/frame.

**Gap:** Such architectures cannot be deployed on commodity CPU edge hardware or scaled across multiple CCTV cameras.

**Our Contribution:** We extract 17 keypoint coordinates per person using YOLOv8-Pose. This reduces input dimensionality by more than 90%, enabling CPU real-time processing at 10–20 FPS and supporting multi-camera expansion.

## Gap 2: False Positives in Action Ambiguity

**Current State:** Pixel-level classifiers and optical-flow methods confuse benign high-motion activities (dancing, hugging, running) with physical violence.

**Gap:** Existing models lack explicit structural awareness of human body kinematics.

**Our Contribution:** We combine spatial proximity queries (k-d Tree) with relative joint acceleration profiling. By measuring wrist-to-head acceleration ratios and bounding-box overlap, aggressive motion signatures are separated from benign movements.

## Gap 3: End-to-End System Integration

**Current State:** Most academic papers evaluate isolated offline models on pre-trimmed datasets. Network streaming, concurrency, alerting, and dashboard integration are rarely addressed.

**Gap:** There is a shortage of open-source, production-oriented surveillance platforms that integrate all components.

**Our Contribution:** SENTINEL-AI provides a complete pipeline: multi-threaded producer-consumer frame queues, WebSocket metadata streaming, asynchronous alert dispatch, and indexed incident logging.
