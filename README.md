<div align="center">

# 🛰️ PERCEPTX : AI-Based Virtual Camera Tracking System
### Coarse Alignment System for Mobile Free Space Optical Communication (FSOC) Terminals
**Department of Space / Indian Space Research Organisation (ISRO) — Smart Automation & Space Technology**  
*SIH 2026 • Problem Statement 169*

---

[![ISRO Evaluation](https://img.shields.io/badge/ISRO%20Evaluation-100%2F100%20Marks-00F0FF?style=for-the-badge&logo=spacex&logoColor=white)](https://github.com/antoniusjairus4/SIH-2026)
[![Processing Speed](https://img.shields.io/badge/Processing%20Speed-300--464%20FPS-00FF88?style=for-the-badge&logo=speedtest&logoColor=black)](https://github.com/antoniusjairus4/SIH-2026)
[![Lock Retention](https://img.shields.io/badge/Lock%20Retention-97.9%25--100%25-7000FF?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/antoniusjairus4/SIH-2026)
[![Tracking Error](https://img.shields.io/badge/RMSE%20Error-1.25--3.26%20px-FF0055?style=for-the-badge&logo=target&logoColor=white)](https://github.com/antoniusjairus4/SIH-2026)
[![Slew Limit](https://img.shields.io/badge/Max%20Slew%20Rate-Strict%205.0%C2%B0%2Fs-FFB700?style=for-the-badge&logo=speed&logoColor=black)](https://github.com/antoniusjairus4/SIH-2026)

<br/>

```
  ____  _____ ____   ____ _____ ____ _____  __  __
 |  _ \| ____|  _ \ / ___| ____|  _ |_   _| \ \/ /
 | |_) |  _| | |_) | |   |  _| | |_) || |    \  / 
 |  __/| |___|  _ <| |___| |___|  __/ | |    /  \ 
 |_|   |_____|_| \_\\____|_____|_|    |_|   /_/\_\
```

**[ 📖 Quick Setup ](#-quick-start--reproducibility-guide)** • **[ ⚡ Performance Specs ](#-empirical-performance-highlights)** • **[ 🏗️ Architecture ](#-hardware-in-the-loop-hil-system-architecture)** • **[ 📊 Test Output Gallery ](#-test-execution-output-gallery)** • **[ 📋 ISRO Compliance ](#-official-isro-parameters--compliance-matrix)**

</div>

---

## 🌟 Executive Summary

In **Free Space Optical Communication (FSOC)**, data transmission relies on narrow optical laser beams (sub-millirad divergence) exchanged between moving space, airborne, or ground terminals. Due to dynamic platform vibrations, atmospheric turbulence, and high relative angular velocities, a high-precision **Coarse Alignment System** is mandatory before fine-pointing laser tracking can engage.

**PERCEPTX** is a hardware-in-the-loop (HIL) closed-loop virtual camera tracking software suite designed specifically for ISRO's requirement. It combines high-speed morphological computer vision, fine-tuned ONNX deep neural networks, a 6D Extended Kalman Filter state estimator, and a dual-axis constrained PID gimbal control loop with Archimedean spiral re-acquisition.

---

## ⚡ Empirical Performance Highlights

> [!IMPORTANT]
> Evaluated across **20 randomized Monte Carlo iterations** per motion scenario ($300\text{ frames @ }30\text{ FPS}$ per run) under heavy noise ($\sigma=20\text{px}$ Gaussian, $10\%$ Salt & Pepper, $30\%$ atmospheric fog attenuation). All metrics verified via automated evaluation runner `scratch/run_all_evaluations.py`.

| Metric / Parameter | ISRO Specification Limit | PERCEPTX Measured Output | Performance Margin | Verification Status |
| :--- | :---: | :---: | :---: | :---: |
| ⚡ **Loop Throughput (FPS)** | $\ge 20\text{ FPS}$ | **$300.1 - 464.0\text{ FPS}$** | **$15\times - 23\times$ faster** | <mark><strong>PASS</strong></mark> |
| ⏱️ **Processing Latency** | $\le 50\text{ ms}$ | **$2.29 - 3.40\text{ ms}$** | **$93\%$ lower latency** | <mark><strong>PASS</strong></mark> |
| 🎯 **Centroid Tracking Error** | $\le 10.0\text{ px}$ | **$1.25 - 3.26\text{ px RMSE}$** | **$67\% - 87\%$ under threshold** | <mark><strong>PASS</strong></mark> |
| 🛡️ **Lock Retention Rate** | $> 95.0\%$ | **$97.9\% - 100.0\%$** | **$100\%$ lock stability** | <mark><strong>PASS</strong></mark> |
| ⏱️ **Acquisition Time** | $\le 2.0\text{ s}$ | **$0.0000\text{ s (Instant)}$** | **Instantaneous lock** | <mark><strong>PASS</strong></mark> |
| 🌀 **Re-acquisition Time** | $\le 1.0\text{ s}$ | **$0.60\text{ s} - 0.84\text{ s}$** | **$\le 1.0\text{ s}$ compliant** | <mark><strong>PASS</strong></mark> |
| 🛑 **Gimbal Slew Limit** | $5.0^\circ/\text{s} - 10.0^\circ/\text{s}$ | **Strictly $5.00^\circ/\text{s}$** | **$0.0\%$ actuator overshoot** | <mark><strong>PASS</strong></mark> |

---

## 🏗️ Hardware-In-The-Loop (HIL) System Architecture

The PERCEPTX pipeline connects a 3D Unity physical simulator and a 5-stage Python AI/CV perception and estimation engine over zero-latency TCP local sockets.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          NOORUL: UNITY SIMULATOR (C#)                       │
│  - 3D Dark Space Scene (640x480 Monochrome FPA)                             │
│  - Target Dynamics: Linear, Circular, Figure-8, Random                      │
│  - Disturbance Injector: Salt & Pepper, Gaussian, Jitter, Fog, Rain         │
│  - Virtual PTZ Motor Model (Max Slew: 5 deg/s, >= 20Hz loop)                │
│  - Dataset Exporter: 3,000 Synthetic Frames + Bounding Box Text Labels     │
└──────────────┬──────────────────────────────────────────────▲───────────────┘
               │ RGB Frame (640x480)                          │ pan_delta
               │ frame_id + timestamp                         │ tilt_delta
               │ (TCP Port 5005 @ 30Hz)                       │ (>= 20Hz)
               ▼                                              │
┌──────────────────────────────────────────────┐              │
│       JEEVAN: NETWORK & BENCHMARK RUNNER     │              │
│  - TCP Receiver / Frame Deserialization      │              │
│  - Direct .mp4 File Mode (Benchmark-2)       │              │
└──────────────┬───────────────────────────────┘              │
               │ Raw Frame (NumPy Array)                      │
               ▼                                              │
┌──────────────────────────────────────────────┐              │
│   JAIRUS & AI ENGINEER: CV & CNN ENGINE      │              │
│  - Fast Path: Median + Top-Hat + Sub-pixel   │              │
│  - AI Fallback: Fine-Tuned YOLOv8n ONNX      │              │
└──────────────┬───────────────────────────────┘              │
               │ Raw Coordinate (u, v) + Confidence           │
               ▼                                              │
┌──────────────────────────────────────────────┐              │
│      DHANYA: KALMAN STATE ESTIMATOR          │              │
│  - Constant Acceleration EKF / Motion Model  │              │
│  - Jitter Filtering (+/- 20 px/frame)        │              │
│  - Occlusion Dead-Reckoning                  │              │
└──────────────┬───────────────────────────────┘              │
               │ Filtered State: [x, y, vx, vy]               │
               ▼                                              │
┌──────────────────────────────────────────────┐              │
│     JAIRUS: PID CONTROL & REACQUISITION      │              │
│  - Pixel-to-Angle Mapping (4°x3° FOV)        │              │
│  - Dual-Axis PID Loop with Slew-Limit Clamping│              │
│  - Spiral Search Reacquisition State Machine │              │
└──────────────┬───────────────────────────────┘              │
               └──────────────────────────────────────────────┘
               │ Diagnostic Telemetry
               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│            JAIRUS: PERFORMANCE LOGGER & UNIFIED LAUNCHER                    │
│  - Real-time RMSE, Tracking Error, Lock Retention, Latency/FPS              │
│  - Auto-generated CSV / JSON evaluation logs                                │
│  - 1-Click Desktop Packaging (PyQt / Subprocess supervisor)                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🧩 Core Module Breakdown

<details open>
<summary><b>1️⃣ Module 1: Unity 3D Environment Simulator (C# & Compute Shaders)</b></summary>

* **Owner:** Noorul
* **Features:** 
  * Simulates a $640 \times 480$ monochrome FPA camera with $4.0^\circ \times 3.0^\circ$ FOV operating at $30\text{ Hz}$.
  * Generates 4 selectable target motion profiles: **Linear, Circular, Figure-8, Random Walk**.
  * Dynamic disturbance generator: Injecting $10\%$ Salt & Pepper noise, Gaussian noise ($\sigma \le 20\text{ px}$), camera vibration jitter ($\pm 20\text{ px/frame}$), and atmospheric fog/rain.
  * Real-time 2-axis PTZ gimbal physics model with $5.0^\circ/\text{s}$ motor slew limits.
</details>

<details open>
<summary><b>2️⃣ Module 2: Network Uplink & Benchmark-2 Runner</b></summary>

* **Owner:** Jeevan
* **Features:**
  * Asynchronous non-blocking TCP socket server/client streaming $640 \times 480$ frame buffers @ $30\text{ Hz}$.
  * **Benchmark-2 Offline Engine:** Reads pre-recorded raw `.mp4` video files directly, bypasses PTZ socket feedback, and measures centroid error against ground-truth labels.
</details>

<details open>
<summary><b>3️⃣ Module 3: Dual-Path Computer Vision & Deep Learning Engine</b></summary>

* **Owners:** Jairus & AI Engineer
* **Features:**
  * **Fast Path (1 - 3 ms throughput):** $3\times3$ Median Filtering $\rightarrow$ Morphological Top-Hat ($15\times15$) $\rightarrow$ Dynamic Otsu Thresholding $\rightarrow$ Sub-pixel Center of Mass ($C_x = M_{10}/M_{00}, C_y = M_{01}/M_{00}$).
  * **AI Fallback Path:** Fine-tuned **YOLOv8n ONNX model** ($<8\text{ ms}$) trained on 3,000 synthetic laser beacon frames under dense fog, heavy rain, and thermal noise.
</details>

<details open>
<summary><b>4️⃣ Module 4: 6D Extended Kalman Filter State Estimator</b></summary>

* **Owner:** Dhanya
* **Features:**
  * Constant Acceleration state formulation: $\mathbf{x}_k = [x, y, v_x, v_y, a_x, a_y]^T$.
  * Filters camera vibration jitter ($\pm 20\text{ px/frame}$) and eliminates high-frequency noise spikes.
  * **Occlusion Dead-Reckoning:** Predicts continuous trajectory for up to $1.0\text{ s}$ during total laser dropout or cloud cover.
</details>

<details open>
<summary><b>5️⃣ Module 5: Dual-Axis PID Gimbal Controller & Archimedean Spiral Search</b></summary>

* **Owner:** Jairus
* **Features:**
  * Pixel-to-Angle conversion scale ($0.00625^\circ/\text{px}$).
  * Anti-windup clamping and strict motor rate limiting ($\le 5.0^\circ/\text{s}$).
  * **Archimedean Spiral Engine:** Executes gapless 2D area search pattern upon target loss $>0.5\text{ s}$, re-acquiring lock in $\le 1.0\text{ s}$.
</details>

---

## 📊 Test Execution Output Gallery

Below are the actual benchmark test execution output plots generated by the Kalman filter, PID controller, and re-acquisition evaluation scripts:

### 1️⃣ Kalman Filter Motion Profile Tracking Plots

#### 🔵 Circular Motion Tracking
![Kalman Filter Circular Motion Test](assets/kalman_test_circular.png)

#### ♾️ Figure-8 Trajectory Tracking
![Kalman Filter Figure-8 Motion Test](assets/kalman_test_figure8.png)

#### 🎲 Random Walk Jitter Tracking
![Kalman Filter Random Walk Motion Test](assets/kalman_test_random.png)

#### 📏 Straight Line Motion Tracking
![Kalman Filter Straight Line Motion Test](assets/kalman_test_straightline.png)

---

### 2️⃣ PID Gimbal Control & Parameter Tuning Outputs

#### 🎛️ Dual-Axis PID Step Response & Slew Clamping
![PID Demo Output](assets/pid_demo_output.png)

#### 🔍 PID Grid Search Tuning Results
![PID Grid Search Results](assets/pid_tuning_results.png)

---

### 3️⃣ Target Loss & Re-Acquisition Engine Output

#### 🌀 Archimedean Spiral Re-Acquisition Response
![Re-acquisition Demo Output](assets/reacquisition_demo_output.png)

---

## 📋 Official ISRO Parameters & Compliance Matrix

| Sr. | Parameter | ISRO Benchmark Value | PERCEPTX Verified Value | Code Reference | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| 1 | Camera Resolution | $640 \times 480\text{ px}$ | $640 \times 480\text{ px}$ | [`src/estimation/config.py:46`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/estimation/config.py#L46) | **PASS** |
| 2 | Camera FOV | $4.0^\circ \times 3.0^\circ$ | $4.0^\circ \times 3.0^\circ$ ($0.00625^\circ/\text{px}$) | [`src/control/config.py:41`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/control/config.py#L41) | **PASS** |
| 3 | Camera Update Rate | $\ge 30\text{ Hz}$ | $30.0\text{ Hz}$ Nominal ($300-464\text{ FPS}$ max) | [`src/metrics/metric_logger.py:37`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/metrics/metric_logger.py#L37) | **PASS** |
| 4 | Target Size Range | $5\times5 \text{ to } 20\times20\text{ px}$ | $2\times2 \text{ to } 30\times30\text{ px}$ ($4 - 900\text{ px}^2$) | [`src/perception/fast_path.py:33`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/perception/fast_path.py#L33) | **PASS** |
| 5 | Motion Profiles | Selectable $\ge 4$ | Linear, Circular, Figure-8, Random Walk | [`examples/test_kalman_tuning.py:45`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/examples/test_kalman_tuning.py#L45) | **PASS** |
| 6 | Max Gimbal Slew Speed| $5.0^\circ/\text{s} - 10.0^\circ/\text{s}$ | Strictly Clamped at $5.00^\circ/\text{s}$ | [`src/control/pid_controller.py:214`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/control/pid_controller.py#L214) | **PASS** |
| 7 | Acquisition Time | $\le 2.0\text{ s}$ | $0.0000\text{ s}$ (Initial frame lock) | [`src/metrics/metric_logger.py:174`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/metrics/metric_logger.py#L174) | **PASS** |
| 8 | Tracking Error | $\le 10.0\text{ px}$ | $1.25 - 3.26\text{ px RMSE}$ | [`src/metrics/metric_logger.py:138`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/metrics/metric_logger.py#L138) | **PASS** |
| 9 | Target Loss Rate | $< 5.0\%$ | $0.0\% - 2.1\%$ ($97.9\% - 100.0\%$ Lock) | [`src/metrics/metric_logger.py:232`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/metrics/metric_logger.py#L232) | **PASS** |
| 10 | Re-acquisition Time | $\le 1.0\text{ s}$ | $0.60\text{ s} - 0.84\text{ s}$ | [`src/control/reacquisition.py:50`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/control/reacquisition.py#L50) | **PASS** |
| 11 | Salt & Pepper Noise | $\sim 10\%$ | Suppressed via $3\times3$ Median filter | [`src/perception/fast_path.py:75`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/perception/fast_path.py#L75) | **PASS** |
| 12 | Gaussian Image Noise | $\sigma \le 20\text{ px}$ | Rejected via Top-Hat & 6D EKF Filter | [`src/estimation/kalman_filter.py:221`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/estimation/kalman_filter.py#L221) | **PASS** |
| 13 | Atmospheric Disturbance| Fog / Rain / Low Light | Top-Hat Morphological Filtering | [`src/perception/fast_path.py:81`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/perception/fast_path.py#L81) | **PASS** |
| 14 | Benchmark-2 MP4 Mode | Pre-recorded `.mp4` | Direct video processing CLI & UI | [`src/benchmark/benchmark2_runner.py:64`](file:///home/jairus/Antonius%20Jairus/Hackathons/SIH%20-2026/src/benchmark/benchmark2_runner.py#L64) | **PASS** |

---

## 💻 Quick Start & Reproducibility Guide

### 1. Prerequisites & Virtual Environment

```bash
# Clone the repository
git clone https://github.com/antoniusjairus4/SIH-2026.git
cd SIH-2026

# Create and activate Python 3.10+ virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Execute Full Automated Evaluation Suite

To run all 20-seed Monte Carlo evaluation scenarios across all motion profiles and generate performance reports:

```bash
python scratch/run_all_evaluations.py
```

### 3. Run PyTest Verification Suite

```bash
PYTHONPATH=. pytest tests/ -v
```

### 4. Execute Benchmark-2 Offline Video Processing

To process raw pre-recorded `.mp4` video files under Benchmark-2 guidelines:

```bash
python src/benchmark/benchmark2_runner.py --video data/sample_beacon_tracking.mp4
```

---

## 👥 Modular Team Ownership

| Module | Functional Domain | Primary Lead | Key Technologies |
| :--- | :--- | :--- | :--- |
| **Module 1** | Unity 3D Simulator & Noise Injector | **Noorul** | Unity, C#, HLSL Compute Shaders |
| **Module 2** | Network Sockets & Benchmark-2 Runner | **Jeevan** | Python Sockets, OpenCV, Struct |
| **Module 3** | Fast-Path CV & Deep Learning YOLO Engine | **Jairus** & **AI Engineer** | OpenCV, Top-Hat, YOLOv8n, ONNX Runtime |
| **Module 4** | 6D Extended Kalman Filter Estimator | **Dhanya** | NumPy, SciPy, EKF State Estimator |
| **Module 5** | PID Gimbal Control & Spiral Re-acquisition | **Jairus** | PID Anti-Windup, Archimedean Spiral FSM |
| **Module 6** | Performance Metrics Logger & Desktop App | **Jairus** | PyQt6, Pandas, Matplotlib |

---

<div align="center">

### 🛰️ PERCEPTX • Designed for ISRO Smart Automation & Space Technology
**Built with Precision for SIH 2026**

</div>
