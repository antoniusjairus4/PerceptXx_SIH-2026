"""
Generate Random Walk / Smooth Random Trajectory Evaluation and Graph
for Kalman Filter State Estimator (SIH PS-169 ISRO Virtual Camera Tracker)
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from examples.test_kalman_tuning import (
    run_filter,
    save_verification_plot,
    print_run_summary,
    SPEC_TARGET_PX,
)

def generate_random_walk(
    num_frames: int = 300,
    cx: float = 320.0,
    cy: float = 240.0,
    step_std: float = 4.0,
    smooth_window: int = 15,
    seed: int = 42,
) -> np.ndarray:
    """
    Generates a smooth, random maneuver trajectory (random walk with moving average smoothing).
    Fits inside 640x480 resolution frame bounds.
    """
    rng = np.random.default_rng(seed)
    
    # Random velocity step increments
    steps_x = rng.normal(0, step_std, size=num_frames)
    steps_y = rng.normal(0, step_std, size=num_frames)
    
    # Cumsum for integrated trajectory
    x = cx + np.cumsum(steps_x)
    y = cy + np.cumsum(steps_y)
    
    # Smooth to emulate physically realistic target maneuvering dynamics
    kernel = np.ones(smooth_window) / smooth_window
    x_smooth = np.convolve(x, kernel, mode="same")
    y_smooth = np.convolve(y, kernel, mode="same")
    
    # Clamp inside bounds
    x_smooth = np.clip(x_smooth, 40.0, 600.0)
    y_smooth = np.clip(y_smooth, 40.0, 440.0)
    
    return np.column_stack([x_smooth, y_smooth])

def main():
    print("=" * 70)
    print("  Generating Random Trajectory Kalman Evaluation Graph")
    print("=" * 70)

    NUM_FRAMES = 300
    gt_random = generate_random_walk(num_frames=NUM_FRAMES, seed=42)

    BEST_Q = 120.0
    BEST_R = 8.0

    result = run_filter(
        ground_truth=gt_random,
        trajectory_name="Random Motion",
        process_noise_std=BEST_Q,
        measurement_noise_std=BEST_R,
        noise_std=20.0,
        occlusion_start=100,
        occlusion_frames=30,
    )

    print_run_summary(result)

    plot_filename = "kalman_test_random.png"
    save_verification_plot(result, plot_filename)

    print(f"\n[SUCCESS] Saved random motion trajectory graph to: {plot_filename}")

if __name__ == "__main__":
    main()
