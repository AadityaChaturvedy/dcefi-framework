#!/usr/bin/env python3
"""CLI Data Ingestion & Indicator Extraction Runner for Indian Data Centres."""

import argparse
import json
import logging
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.ingestion import init_gee, extract_cluster_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("run_ingestion")


def main():
    parser = argparse.ArgumentParser(description="Multi-Source Data Ingestion for Indian Data Centres")
    parser.add_argument("--config", default=str(ROOT / "config" / "dc_clusters.json"), help="Path to cluster JSON configuration")
    parser.add_argument("--cluster-id", default="all", help="Specific cluster ID to process, or 'all'")
    parser.add_argument("--start-date", default="2023-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", default="2023-12-31", help="End date YYYY-MM-DD")
    parser.add_argument("--output-dir", default=str(ROOT / "data" / "processed"), help="Directory to save extracted records")
    parser.add_argument("--ee-project", default=None, help="Google Cloud Project ID for Earth Engine auth")

    args = parser.parse_args()
    init_gee(project_id=args.ee_project)

    with open(args.config, "r", encoding="utf-8") as f:
        clusters = json.load(f).get("clusters", [])

    if args.cluster_id != "all":
        clusters = [c for c in clusters if c["id"] == args.cluster_id]

    logger.info(f"Ingesting features for {len(clusters)} facility cluster(s)...")
    results = [extract_cluster_features(c, args.start_date, args.end_date) for c in clusters]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "dc_ingested_features.json", "w", encoding="utf-8") as f:
        json.dump({"results": results}, f, indent=2)

    pd.DataFrame(results).to_csv(out_dir / "dc_ingested_features.csv", index=False)
    logger.info(f"Ingestion complete. Exported {len(results)} records to {out_dir}")


if __name__ == "__main__":
    main()
