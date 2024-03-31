import glob
import os
import re
import sys
import cv2
import numpy as np
import pydicom
import pydicom.uid
from pathlib import Path
from pydicom import dcmread
from pydicom.data import get_testdata_file
from PIL import Image

def normalize(image: np.ndarray) -> np.ndarray:
    """
    Normalize MR scan image intensity. Sets minimum value to zero, rescales to the full 0-255 range.
    :param np.ndarray image: a single slice of an MR scan
    :return np.ndarray normalized_image: normalized MR slice
    """
    # Set minimum value to zero
    min_val = np.min(image)
    max_val = np.max(image)
    if min_val < max_val:
        image = (image - min_val) / (max_val - min_val) * 255
    else:
        image = np.zeros_like(image)

    # Apply gamma correction to enhance brightness
    gamma = 0.8  # Adjust the gamma value as needed
    normalized_image = cv2.convertScaleAbs(image, alpha=1.0)
    normalized_image = cv2.pow(normalized_image / 255.0, gamma) * 255.0

    return normalized_image.astype(np.uint8)

def grayscale_to_rgb(grayscale_image):
    return cv2.cvtColor(grayscale_image, cv2.COLOR_GRAY2RGB)

def main():
    """Illustration of what normalize might look like in practice """

    data_dir = "/GitHub/AutoRadAI/Convert/DataDicom"  # some path to a set of DICOMs
    target_dir = "/GitHub/AutoRadAI/Convert/DataPng"  # destination

    for image_fpath in os.listdir(data_dir):
        image_fpath = os.path.join(data_dir, image_fpath)

        # Read the DICOM file, setting Transfer Syntax manually
        ds = dcmread(image_fpath, force=True)
        
        # Check if the dataset has pixel data
        if "PixelData" not in ds:
            print(f"Skipping {image_fpath} as it doesn't contain pixel data.")
            continue

        image_nparray = ds.pixel_array

        normalized_image = normalize(image_nparray)
        rgb_image = grayscale_to_rgb(normalized_image)

        image_dir, fname = os.path.split(image_fpath)
        fname = fname.replace(".dcm", ".png")
        cv2.imwrite(os.path.join(target_dir, fname), rgb_image)

if __name__ == "__main__":
    main()

    pass
