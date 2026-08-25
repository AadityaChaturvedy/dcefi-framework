"""Unit tests for data ingestion modules in offline/mock mode."""

import unittest
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.ingestion import (
    extract_landsat_lst,
    extract_sentinel_indices,
    extract_era5_climate,
    extract_osm_footprints,
    extract_cluster_features,
    _meters_to_deg,
)


class TestIngestionPipeline(unittest.TestCase):

    def setUp(self):
        with open(ROOT / "config" / "dc_clusters.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def test_config_structure(self):
        clusters = self.config.get("clusters", [])
        self.assertGreaterEqual(len(clusters), 5)
        for c in clusters:
            self.assertTrue(8.0 <= c["latitude"] <= 36.0)
            self.assertTrue(68.0 <= c["longitude"] <= 97.0)

    def test_meters_to_deg(self):
        dlat, dlon = _meters_to_deg(111320.0, 0.0)
        self.assertAlmostEqual(dlat, 1.0, places=3)
        self.assertAlmostEqual(dlon, 1.0, places=3)

    def test_landsat_lst_offline(self):
        res = extract_landsat_lst(19.1412, 73.0089, "2023-01-01", "2023-12-31")
        self.assertIsNotNone(res["delta_t_lst_c"])

    def test_sentinel_indices_offline(self):
        res = extract_sentinel_indices(13.0982, 80.1625, "2023-01-01", "2023-12-31")
        self.assertIn("delta_ndvi", res)

    def test_era5_climate_offline(self):
        res = extract_era5_climate(28.5085, 77.3821, "2023-01-01", "2023-12-31")
        self.assertIn("ambient_temp_2m_c", res)

    def test_osm_footprints(self):
        res = extract_osm_footprints(12.9784, 77.7289, 400.0)
        self.assertTrue(0.0 <= res["builtup_density_ratio"] <= 1.0)

    def test_extract_cluster_features_end_to_end(self):
        record = extract_cluster_features(self.config["clusters"][0], "2023-01-01", "2023-12-31")
        self.assertIn("delta_t_lst_c", record)
        self.assertIn("ndvi_core", record)
        self.assertIn("ambient_temp_era5_c", record)


if __name__ == "__main__":
    unittest.main()
