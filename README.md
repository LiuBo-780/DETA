# DETA

Code accompanying the paper “Scene-Adaptive Subpixel Retrieval of Cyanobacterial Bloom Abundance from Sentinel-3 OLCI Imagery via Dynamic Endmember Thresholding”.

## Overview

DETA estimates fractional cyanobacterial bloom cover from Sentinel-3 OLCI imagery. It determines pure-water and pure-bloom thresholds from the NDVI distribution of each scene and uses these thresholds to parameterize a logistic retrieval function without training samples.

## Data access

The file `data.csv` lists the 30 near-synchronous Sentinel-2/Sentinel-3 image pairs used in this study, including acquisition times and Sentinel-2 Earth Engine image identifiers.

Sentinel-3 OLCI products were downloaded from the Copernicus Data Space Ecosystem:
https://dataspace.copernicus.eu/

Sentinel-2 MSI imagery was accessed through Google Earth Engine. The collection identifier and the script used to select and export the imagery are provided in https://code.earthengine.google.com/60c340503329042fb21f60b84bf43e74.

## Reproducing the experiments

1. Download the satellite products listed in `data.csv`.
2. Prepare the imagery and water masks using the preprocessing instructions.
3. Run DETA using the documented input band configuration.
4. Generate the Sentinel-2 reference maps and simulated OLCI-resolution imagery.
5. Run the comparison and evaluation scripts to reproduce the reported results.




