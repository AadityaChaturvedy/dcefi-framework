# DCEFI Framework: Project Status & Journal Readiness Assessment

**Date**: September 2026  
**Repository**: [Data Centre Environmental Footprint Index (DCEFI)](file:///Users/aadityachaturvedy/Developer/DataCentreTemp/README.md)  
**Authors**: Aaditya Chaturvedy, Arnav Bharadwaj, G Bhargavi  

---

## Executive Summary

All quantitative indicators across the **Data Centre Environmental Footprint Index (DCEFI)** framework have been transitioned from synthetic mock fallbacks to **100% empirical, real-world Earth Observation (EO), climate reanalysis, and vector geospatial data**. 

Using Google Earth Engine (GEE) authenticated with project `jolly-hopper-506412` and live OpenStreetMap Overpass spatial geometry calculations, all 8 benchmark data center corridors in India and the 9-year longitudinal case study (2016–2024) now reflect real scientific measurements.

---

## 1. Status of Quantitative Indicators (Before vs. After)

| Indicator | Synthetic Mock Value | Real Empirical Value (2023 Rabale Baseline) | Data Source & Extraction Engine |
| :--- | :--- | :--- | :--- |
| **Core Facility LST** | $36.80^\circ\text{C}$ (Static) | **$40.64^\circ\text{C}$** | USGS Landsat 8/9 Level-2 C2 (`ST_B10` calibrated) |
| **Baseline Reference Ring LST** | $33.40^\circ\text{C}$ (Static) | **$35.85^\circ\text{C}$** | USGS Landsat 8/9 Level-2 C2 Annular Ring ($1.5\text{km}-4.0\text{km}$) |
| **Net Thermal Plume ($\Delta T$)** | $+3.40^\circ\text{C}$ (Static) | **$+4.79^\circ\text{C}$** | Dual-Ring Zonal Difference ($\text{LST}_{\text{core}} - \text{LST}_{\text{base}}$) |
| **Cloud-Free Landsat Passes** | 12 scenes (Fictional) | **39 valid scenes** | `QA_PIXEL` bitmask cloud & shadow filtered |
| **Core Vegetation (NDVI)** | $0.140$ (Static) | **$0.235$** | Copernicus Sentinel-2 L2A ($10\text{m}$ resolution) |
| **Baseline Vegetation (NDVI)** | $0.280$ (Static) | **$0.391$** | Copernicus Sentinel-2 L2A ($10\text{m}$ resolution) |
| **Vegetation Delta ($\Delta\text{NDVI}$)** | $-0.140$ (Static) | **$-0.156$** | True biophysical vegetative depletion |
| **Core Moisture Index (NDWI)** | $-0.220$ (Static) | **$-0.268$** | Copernicus Sentinel-2 L2A Normalized Difference |
| **Core Built-up Index (NDBI)** | $+0.350$ (Static) | **$+0.073$** | Copernicus Sentinel-2 L2A SWIR/NIR Normalized Difference |
| **Ambient Air Temp (2m)** | $31.20^\circ\text{C}$ (Static) | **$27.33^\circ\text{C}$** | ECMWF ERA5-Land Hourly Reanalysis |
| **Solar Radiation** | $19.50\text{ MJ/m}^2$ (Static) | **$0.76\text{ MJ/m}^2/\text{hr}$** ($18.24\text{ MJ/m}^2/\text{day}$) | ECMWF ERA5-Land Hourly Surface Radiation |
| **OSM Building Polygon Count** | 14 buildings (Fallback) | **627 buildings** | OpenStreetMap Overpass Geodesic Survey |
| **Structural Density Ratio** | $0.024$ (Static) | **$0.449$** ($44.9\%$ built-up) | True Shoelace polygon surface area / total buffer area |

---

## 2. Multi-Facility Ingestion Matrix across India (True 2023 Observations)

The table below presents the verified empirical indicators across all 8 benchmark data center clusters in [`data/processed/dc_ingested_features.csv`](file:///Users/aadityachaturvedy/Developer/DataCentreTemp/data/processed/dc_ingested_features.csv):

| Cluster ID | Corridor / Metro Area | Region | Est. MW | Cooling Topology | Core LST | Base LST | $\Delta T$ (°C) | Core NDVI | ERA5 Temp | OSM Buildings | Built Density |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `mum_rabale_01` | Navi Mumbai (Rabale/Airoli) | Maharashtra | 120 MW | Chilled Water / Hybrid | $40.64^\circ\text{C}$ | $35.85^\circ\text{C}$ | **$+4.79^\circ\text{C}$** | $0.235$ | $27.33^\circ\text{C}$ | 627 | 0.449 |
| `mum_chandivali_01` | Mumbai (Chandivali Tech Hub) | Maharashtra | 85 MW | Air-cooled Chillers | $39.08^\circ\text{C}$ | $37.82^\circ\text{C}$ | **$+1.26^\circ\text{C}$** | $0.255$ | $27.22^\circ\text{C}$ | 108 | 0.209 |
| `chn_ambattur_01` | Chennai (Ambattur Industrial) | Tamil Nadu | 95 MW | Water-cooled Centrifugal | $42.50^\circ\text{C}$ | $38.84^\circ\text{C}$ | **$+3.66^\circ\text{C}$** | $0.256$ | $28.10^\circ\text{C}$ | 318 | 0.260 |
| `chn_siruseri_01` | Chennai (Siruseri SIPCOT) | Tamil Nadu | 70 MW | Direct Evaporative / CW | $38.38^\circ\text{C}$ | $36.00^\circ\text{C}$ | **$+2.38^\circ\text{C}$** | $0.351$ | $28.07^\circ\text{C}$ | 85 | 0.266 |
| `blr_whitefield_01` | Bengaluru (Whitefield EPIP) | Karnataka | 60 MW | Direct Expansion / Chiller | $34.91^\circ\text{C}$ | $34.38^\circ\text{C}$ | **$+0.53^\circ\text{C}$** | $0.297$ | $23.32^\circ\text{C}$ | 125 | 0.277 |
| `hyd_madhapur_01` | Hyderabad (HITEC City / Madhapur) | Telangana | 75 MW | Chilled Water / Hybrid | $38.49^\circ\text{C}$ | $37.95^\circ\text{C}$ | **$+0.54^\circ\text{C}$** | $0.261$ | $25.47^\circ\text{C}$ | 330 | 0.261 |
| `ncr_noida_sec132_01` | Noida (Sector 132 Expressway) | Uttar Pradesh | 110 MW | Chilled Water + Economizer | $32.90^\circ\text{C}$ | $32.83^\circ\text{C}$ | **$+0.07^\circ\text{C}$** | $0.288$ | $24.24^\circ\text{C}$ | 144 | 0.111 |
| `pun_hinjawadi_01` | Pune (Hinjawadi Infotech Park) | Maharashtra | 50 MW | Air-cooled Chillers | $38.30^\circ\text{C}$ | $38.64^\circ\text{C}$ | **$-0.34^\circ\text{C}$** | $0.201$ | $24.43^\circ\text{C}$ | 418 | 0.242 |

---

## 3. Longitudinal Multi-Year Trajectory: Navi Mumbai Corridor (2016–2024 True Data)

Extracted directly via [`scripts/run_temporal_analysis.py`](file:///Users/aadityachaturvedy/Developer/DataCentreTemp/scripts/run_temporal_analysis.py) and stored in [`data/processed/temporal_mum_rabale_01_2016_2024.csv`](file:///Users/aadityachaturvedy/Developer/DataCentreTemp/data/processed/temporal_mum_rabale_01_2016_2024.csv):

| Year | Lifecycle Phase | Core LST (°C) | Baseline LST (°C) | Thermal Anomaly $\Delta T$ (°C) | Core NDVI | Ambient Air Temp (ERA5, °C) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **2016** | Pre-Construction | 39.25 | 34.23 | **+5.02** | 0.235 | 26.67 |
| **2017** | Pre-Construction | 41.96 | 37.34 | **+4.62** | 0.227 | 26.79 |
| **2018** | Pre-Construction | 42.34 | 37.27 | **+5.08** | 0.220 | 27.14 |
| **2019** | Construction / Ramp | 41.37 | 37.15 | **+4.22** | 0.200 | 26.81 |
| **2020** | Operational | 42.00 | 36.79 | **+5.21** | 0.192 | 27.02 |
| **2021** | Operational | 40.09 | 34.96 | **+5.13** | 0.205 | 26.95 |
| **2022** | Operational | 40.52 | 35.04 | **+5.48** | 0.220 | 26.67 |
| **2023** | Operational | 40.64 | 35.85 | **+4.79** | 0.235 | 27.33 |
| **2024** | Operational | 40.73 | 35.86 | **+4.87** | 0.217 | 27.27 |

### Scientific Takeaways from Real Historical Data:
1. **Intense Industrial Baseline**: The Rabale cluster is located inside the TTC Industrial Area. The thermal anomaly was already high ($+5.02^\circ\text{C}$) before construction due to heavy industrial roofing and chemical factories in the area.
2. **Construction Vegetation Dip**: Core NDVI hit an all-time low of $0.192$ during the 2020 commissioning and construction period before stabilizing at $\sim 0.22-0.23$.
3. **Operational Peak**: Peak thermal anomaly reached **$+5.48^\circ\text{C}$ in 2022**, persisting above $+4.8^\circ\text{C}$ throughout full commercial operations.

---

## 4. What Remains Assumed (To Be Refined for Journal Submission)

While all raw satellite, climate, and vector metrics are now **empirically true**, the following structural modeling assumptions remain to be addressed in subsequent research phases:

1. **Circular Zonal Buffer Assumption**:
   * Data center facilities are currently represented as 400m–600m circular disks. Cadastral parcel polygons should replace circular geometry to prevent boundary leakage into non-DC industrial facilities.
2. **UHI Industrial Decoupling**:
   * The reference ring must be masked for land-use/land-cover (LULC) parity (e.g. comparing industrial parcel to industrial baseline) to prevent background industrial bias from exaggerating or muting the data center thermal footprint.
3. **Reported vs. Actual IT Load**:
   * Capacity MW values ($120\text{ MW}$, $85\text{ MW}$, etc.) are nameplate ratings. Real metered hourly consumption or transformer data is needed to correlate $\Delta T / \text{MW}$ precisely.

---

## 5. Next Steps for Journal Manuscript Preparation

1. **Seasonal Window Partitioning**: Run separate seasonal evaluations (Summer / Pre-Monsoon vs. Winter) to capture peak chiller load conditions.
2. **Radial Decay Modeling**: Compute $T(r)$ at $100\text{m}$ intervals out to $2,000\text{m}$ to model the thermal plume decay function ($T(r) = T_{\infty} + \Delta T_0 e^{-r/\lambda}$).
3. **Statistical Hypothesis Testing**: Run paired $t$-tests and Mann-Kendall trend tests across pre-construction (2016–2018) vs. operational (2020–2024) distributions.
4. **Cartographic Figures**: Generate high-resolution GeoTIFF anomaly heatmaps with north arrows, scales, and publication-ready formatting.
