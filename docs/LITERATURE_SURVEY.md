# Literature Survey — Violence & Anomaly Detection in Surveillance Video

## 1. Introduction

Automatic violence detection in surveillance has been approached through three major paradigms: 3D convolutional networks, optical-flow/two-stream models, and skeleton/pose-based methods. This survey reviews representative techniques and identifies where SENTINEL-AI contributes.

## 2. 3D Convolutional Approaches

**C3D (Tran et al., 2015)** learns spatio-temporal features using 3D convolutions over video clips. While accurate, it is computationally expensive and requires GPU resources, making multi-camera edge deployment difficult.

**I3D (Carreira & Zisserman, 2017)** inflates 2D filters into 3D and pre-trains on large video datasets. It achieves high benchmark scores but inference latency often exceeds 150 ms/frame on CPU.

**Limitation:** Pixel-heavy architectures do not scale to real-time CPU streams.

## 3. Optical Flow & Two-Stream Models

**Simonyan & Zisserman (2014)** proposed two-stream networks using RGB frames and optical-flow stacks. Subsequent works applied dense trajectories and flow maps to violence detection.

**Limitation:** Optical flow is sensitive to camera jitter and background motion. Benign high-motion actions (running, dancing, sports) frequently produce false positives.

## 4. Pose & Skeleton-Based Methods

Recent work converts video into skeletal keypoint sequences and applies graph or temporal models:

- **ST-GCN** operates on body-joint graphs and achieves good accuracy with lightweight input.
- **LSTM over keypoints** learns temporal dynamics from coordinate sequences.

These methods reduce input dimensionality significantly but still require training on large datasets and can be black-box.

## 5. Public Datasets

| Dataset | Content | Size | Use in Project |
|---|---|---|---|
| Hockey Fights | Ice-hockey fight clips | ~1 GB | Viva 1–2 quick benchmarking |
| RWF-2000 | Real-world fight/non-fight | ~10 GB | Primary benchmark (Viva 4) |
| UCF-Crime | Anomaly detection videos | Large | Literature context |

## 6. Synthesis

Current literature either sacrifices real-time performance for accuracy (3D-CNNs) or suffers from high false-positive rates (optical flow). There is a gap for an explainable, low-latency, CPU-compatible system with production-grade integration.

## References (Representative)

1. Tran et al. Learning Spatiotemporal Features with 3D Convolutional Networks. ICCV 2015.
2. Carreira & Zisserman. Quo Vadis, Action Recognition? CVPR 2017.
3. Simonyan & Zisserman. Two-Stream Convolutional Networks for Action Recognition. NeurIPS 2014.
4. Yan, Xiong & Lin. Spatial Temporal Graph Convolutional Networks for Skeleton-Based Action Recognition. AAAI 2018.
5. Sultani, Chen & Shah. Real-World Anomaly Detection in Surveillance Videos. CVPR 2018.
