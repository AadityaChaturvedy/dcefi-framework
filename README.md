# Data Centre Environmental Footprint Index (DCEFI)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-API-brightgreen.svg)](https://earthengine.google.com/)
[![Sentinel & Landsat](https://img.shields.io/badge/Satellite%20Data-Sentinel%202%20%7C%20Landsat%208%2F9-orange.svg)](https://scihub.copernicus.eu/)

An automated Earth Observation (EO) and geospatial analytics pipeline designed to quantify, benchmark, and monitor the microclimatic thermal plume ($\Delta T$), land-cover transformation, and biophysical footprint of hyperscale and enterprise colocation data centers across India.

---

## 📌 Background & Motivation

India is witnessing an exponential build-out of hyperscale cloud infrastructure, concentrated across major metro corridors (Navi Mumbai, Chennai, Bengaluru, Hyderabad, Noida, Pune). Data centers reject massive amounts of continuous low-grade sensible and latent heat into the boundary layer through chiller exhausts, cooling towers, and dry coolers, while converting vegetated land into impervious surface infrastructure.

This framework isolates the localized anthropogenic footprint of data centers from broader Urban Heat Island (UHI) effects and macro-regional weather patterns using high-resolution multi-source remote sensing and meteorological reanalysis.

---

## 🔬 Scientific Methodology

```
                   ┌───────────────────────────────────────────┐
                   │    Background Reference Ring (Annular)    │
                   │    Inner: 1.2–1.8 km | Outer: 3.5–4.5 km  │
                   │                                           │
                   │         ┌───────────────────────┐         │
                   │         │   Core Facility Area  │         │
                   │         │     Radius: 400-600m  │         │
                   │         │   [ Data Hall & HV ]  │         │
                   │         └───────────────────────┘         │
                   │                                           │
                   └───────────────────────────────────────────┘
```

The system implements a **dual-ring zonal statistics** methodology:
1. **Core Facility Zone ($400\text{m} - 600\text{m}$ buffer)**: Directly encloses the facility perimeter, sub-stations, transformer yards, and heat rejection equipment.
2. **Baseline Reference Ring ($1,200\text{m}-1,800\text{m}$ inner to $3,500\text{m}-4,500\text{m}$ outer annular buffer)**: Captures surrounding ambient microclimate without immediate plume contamination.
3. **Net Thermal Anomaly ($\Delta T$)**:
   $$\Delta T = \text{LST}_{\text{core}} - \text{LST}_{\text{baseline}}$$
4. **Vegetation & Moisture Shift ($\Delta\text{NDVI}$, $\Delta\text{NDWI}$)**:
   $$\Delta\text{NDVI} = \text{NDVI}_{\text{core}} - \text{NDVI}_{\text{baseline}}$$

---

## 🛰️ Multi-Source Data Pipeline

| Sensor / Source | Dataset Identifier | Resolution / Cadence | Extracted Indicators |
|---|---|---|---|
| **Landsat 8 & 9 (TIRS)** | `LANDSAT/LC08_LC09/C02/T1_L2` | 30m / 8–16 days | Land Surface Temperature (LST, °C), $\Delta T$ |
| **Sentinel-2 (MSI)** | `COPERNICUS/S2_SR_HARMONIZED` | 10m–20m / 5 days | NDVI (Vegetation), NDWI (Moisture), NDBI (Built-up) |
| **ECMWF ERA5-Land** | `ECMWF/ERA5_LAND/HOURLY` | ~11km (0.1°) / Hourly | 2m Air Temperature, Surface Solar Radiation ($MJ/m^2$) |
| **OpenStreetMap** | Overpass API (`building=*`) | Vector polygons | Built-up Footprint Area ($m^2$), Structural Density Ratio |

---

## 🏢 Monitored Facility Clusters (`config/dc_clusters.json`)

The pipeline tracks key hyperscale and enterprise colocation corridors across India:
- **Navi Mumbai** (`mum_rabale_01`): Rabale & Airoli DC Corridor (120 MW, Chilled Water / Hybrid)
- **Mumbai** (`mum_chandivali_01`): Chandivali Tech Hub (85 MW, Air-cooled Chillers)
- **Chennai** (`chn_ambattur_01`): Ambattur Industrial Cluster (95 MW, Water-cooled Centrifugal)
- **Chennai** (`chn_siruseri_01`): Siruseri SIPCOT IT Corridor (70 MW, Direct Evaporative / CW)
- **Bengaluru** (`blr_whitefield_01`): Whitefield EPIP (60 MW, Direct Expansion / Air-cooled)
- **Hyderabad** (`hyd_madhapur_01`): HITEC City & Madhapur (75 MW, Chilled Water / Hybrid)
- **Noida** (`ncr_noida_sec132_01`): Sector 132 Expressway Corridor (110 MW, CW + Economizer)
- **Pune** (`pun_hinjawadi_01`): Hinjawadi Rajiv Gandhi Infotech Park (50 MW, Air-cooled Chillers)

---

## 📁 Repository Structure

```
├── config/
│   └── dc_clusters.json               # Facility coordinates, MW ratings, cooling types & buffer radii
├── data/
│   ├── raw/                           # Raw satellite scene cache (.gitkeep)
│   └── processed/                     # Extracted indicator records (CSV & JSON)
│       ├── dc_ingested_features.csv
│       ├── dc_ingested_features.json
│       └── temporal_mum_rabale_01_2017_2023.csv
├── scripts/
│   ├── run_ingestion.py               # Batch multi-source ingestion CLI runner
│   ├── run_temporal_analysis.py       # Longitudinal pre vs. post-operational analyzer
│   └── generate_report_docx.py        # Zero-dependency OpenXML .docx progress report generator
├── src/
│   ├── __init__.py
│   └── ingestion.py                   # Unified EO & GIS extractor (Landsat, Sentinel-2, ERA5, OSM)
├── tests/
│   └── test_ingestion_offline.py      # Unit test suite with offline mock validation
├── requirements.txt                   # Dependency manifest (earthengine-api, pandas, requests)
├── .gitignore                         # Git exclusion rules
├── LICENSE                            # MIT License
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Optional: A Google Cloud Project registered with [Google Earth Engine](https://earthengine.google.com/) for live satellite ingestion (all modules gracefully fall back to dry-run / offline simulation if GEE credentials are not configured).

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/AadityaChaturvedy/dcefi-framework.git
cd dcefi-framework

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Google Earth Engine Authentication (Optional)
```bash
earthengine authenticate
```

---

## 💻 Usage

### Batch Feature Ingestion
Run multi-source feature extraction across all configured clusters or for a specific facility:
```bash
# Ingest all clusters for year 2023
python3 scripts/run_ingestion.py --start-date 2023-01-01 --end-date 2023-12-31

# Ingest a specific cluster with GEE cloud project ID
python3 scripts/run_ingestion.py --cluster-id mum_rabale_01 --ee-project your-gcp-project-id
```

### Multi-Year Longitudinal Analysis
Analyze thermal plume growth and land-cover transformation across pre-construction (2016) and operational (2023) periods:
```bash
python3 scripts/run_temporal_analysis.py \
  --cluster-id mum_rabale_01 \
  --start-year 2016 \
  --end-year 2024 \
  --pre-year 2016 \
  --post-year 2023
```

### Generate Technical Progress Report (.docx)
Generate a styled `.docx` executive report without any third-party Office/Word dependencies:
```bash
python3 scripts/generate_report_docx.py
```

### Running Test Suite
Execute the offline test suite:
```bash
python3 -m unittest discover tests
```

---

## 👥 Authors

- **Aaditya Chaturvedy**
- **Arnav Bharadwaj**
- **G Bhargavi**

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

