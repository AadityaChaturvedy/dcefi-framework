#!/usr/bin/env python3
"""Temporal & Pre/Post Operational Environmental Footprint Analyzer for Indian Data Centres."""

import argparse
import json
import logging
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.ingestion import init_gee, extract_landsat_lst, extract_sentinel_indices, extract_era5_climate

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("temporal_analysis")


def run_temporal_analysis(cluster: dict, start_year: int = 2016, end_year: int = 2024, pre_year: int = 2016, post_year: int = 2023) -> dict:
    cid, name, lat, lon = cluster["id"], cluster["name"], cluster["latitude"], cluster["longitude"]
    op_year = cluster.get("operational_year", 2019)
    core_r, base_in, base_out = cluster.get("core_radius_m", 500), cluster.get("baseline_ring_inner_m", 1500), cluster.get("baseline_ring_outer_m", 4000)

    logger.info(f"Temporal Analysis for {name} ({cid}) from {start_year} to {end_year}")
    yearly_records = []

    for year in range(start_year, end_year + 1):
        s_date, e_date = f"{year}-01-01", f"{year}-12-31"
        lst_res = extract_landsat_lst(lat, lon, s_date, e_date, core_r, base_in, base_out)
        s2_res = extract_sentinel_indices(lat, lon, s_date, e_date, core_r, base_in, base_out)
        era5_res = extract_era5_climate(lat, lon, s_date, e_date)
        phase = "Pre-Construction" if year < op_year else ("Construction/Ramp" if year == op_year else "Operational")

        yearly_records.append({
            "cluster_id": cid, "cluster_name": name, "year": year, "phase": phase,
            "core_lst_c": lst_res.get("core_lst_mean_c"), "baseline_lst_c": lst_res.get("baseline_lst_mean_c"),
            "delta_t_lst_c": lst_res.get("delta_t_lst_c"), "ndvi_core": s2_res.get("ndvi_core_mean"),
            "ambient_temp_era5_c": era5_res.get("ambient_temp_2m_c"),
        })

    df = pd.DataFrame(yearly_records)
    pre_row = df[df["year"] == pre_year]
    post_row = df[df["year"] == post_year]
    comparison = {}

    if not pre_row.empty and not post_row.empty:
        pre_rec, post_rec = pre_row.iloc[0], post_row.iloc[0]
        comparison = {
            "pre_year": pre_year, "post_year": post_year,
            "pre_delta_t_lst_c": pre_rec.get("delta_t_lst_c", 0.0),
            "post_delta_t_lst_c": post_rec.get("delta_t_lst_c", 0.0),
            "thermal_plume_growth_c": round((post_rec.get("delta_t_lst_c") or 0.0) - (pre_rec.get("delta_t_lst_c") or 0.0), 2),
            "pre_ndvi_core": pre_rec.get("ndvi_core", 0.0),
            "post_ndvi_core": post_rec.get("ndvi_core", 0.0),
            "vegetation_change_delta": round((post_rec.get("ndvi_core") or 0.0) - (pre_rec.get("ndvi_core") or 0.0), 3),
        }

    return {"yearly_records": yearly_records, "comparison": comparison, "df": df}


def main():
    parser = argparse.ArgumentParser(description="Multi-Year and Pre/Post Operational Environmental Analyzer")
    parser.add_argument("--config", default=str(ROOT / "config" / "dc_clusters.json"))
    parser.add_argument("--cluster-id", default="mum_rabale_01")
    parser.add_argument("--start-year", type=int, default=2016)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument("--pre-year", type=int, default=2016)
    parser.add_argument("--post-year", type=int, default=2023)
    parser.add_argument("--output-dir", default=str(ROOT / "data" / "processed"))
    parser.add_argument("--ee-project", default=None)

    args = parser.parse_args()
    init_gee(project_id=args.ee_project)

    with open(args.config, "r", encoding="utf-8") as f:
        clusters = json.load(f).get("clusters", [])

    cluster = next((c for c in clusters if c["id"] == args.cluster_id), None)
    if not cluster:
        logger.error(f"Cluster '{args.cluster_id}' not found")
        sys.exit(1)

    result = run_temporal_analysis(cluster, args.start_year, args.end_year, args.pre_year, args.post_year)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    result["df"].to_csv(out_dir / f"temporal_{args.cluster_id}_{args.start_year}_{args.end_year}.csv", index=False)

    print("\n" + "=" * 80)
    print(f"📊 MULTI-YEAR TEMPORAL TREND: {cluster['name']} ({args.start_year} - {args.end_year})")
    print("=" * 80)
    print(result["df"].to_string(index=False))


if __name__ == "__main__":
    main()
