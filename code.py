"""
This repository provides core code snippets for DETA, covering dynamic
endmember threshold calculation and bloom abundance retrieval but
excluding image preprocessing.
"""

# 1. Imports
import os
import glob
import warnings
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from osgeo import gdal
from sklearn.mixture import GaussianMixture


# 2. Triangle Algorithm
def custom_triangle_logic(
    bins, counts, pt1_idx, pt2_idx, search_start_idx, search_end_idx
):
    """
    Calculate perpendicular distances from histogram points to the
    baseline and return the bin value with the maximum distance.
    """
    x1, y1 = bins[pt1_idx], counts[pt1_idx]
    x2, y2 = bins[pt2_idx], counts[pt2_idx]

    A = y1 - y2
    B = x2 - x1
    C = x1 * y2 - x2 * y1

    start, end = min(search_start_idx, search_end_idx), max(
        search_start_idx, search_end_idx
    )
    search_idx = np.arange(start, end + 1)

    x_s, y_s = bins[search_idx], counts[search_idx]
    norm = np.sqrt(A**2 + B**2)
    if norm == 0:
        return bins[search_start_idx]

    distances = np.abs(A * x_s + B * y_s + C) / norm
    return x_s[np.argmax(distances)]


# 3. Otsu Thresholding
# The following snippets require variables supplied by the main workflow.

# Normalize valid NDVI values to 0–255 for OpenCV Otsu thresholding
min_val, max_val = ndvi_valid.min(), ndvi_valid.max()
ndvi_uint8 = (
    (ndvi_valid - min_val) / (max_val - min_val) * 255
).astype(np.uint8)

# Calculate the Otsu threshold
otsu_thresh_val, _ = cv2.threshold(
    ndvi_uint8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)

# Convert the threshold back to the original NDVI scale
t_water = min_val + (otsu_thresh_val / 255.0) * (max_val - min_val)


# 4. Logistic Parameter Calculation and Abundance Retrieval
# h: pure-water threshold
# a: pure-bloom threshold

if a == h:
    a += 0.001

ln_99 = np.log(99.0)
j = (2.0 * ln_99) / (a - h)  # Steepness parameter
i = (a + h) / 2.0           # Midpoint (inflection point)

# Initialize abundance, retaining NaN for invalid pixels
valid_mask = ~nan_mask
abundance = np.full_like(ndvi_clean, np.nan, dtype=np.float32)

x_valid = ndvi_clean[valid_mask]

# Calculate the original logistic output
y_raw = 1.0 / (1.0 + np.exp(-j * (x_valid - i)))

# Linearly rescale [0.01, 0.99] to [0, 1]
y_scaled = (y_raw - 0.01) / (0.99 - 0.01)

# Clip to [0, 1]: values <= 0.01 map to 0, and values >= 0.99 map to 1
y_final = np.clip(y_scaled, 0.0, 1.0)

abundance[valid_mask] = y_final
