import os
import pandas as pd
import numpy as np
from pathlib import Path

data_dir = Path("data")
outputs_dir = Path("outputs")

dat_path = data_dir / "GS1" / "OptiusGS1MatchingImpacts" / "2025-12-10_optiusGS1_matched_impacts_PRELIMINARY.tsv"
processed_dir = data_dir / "processed"

data_df = pd.read_csv(dat_path, sep="\t")
comp_df = pd.read_csv(processed_dir / "all_compositions.csv", low_memory=False)

impact_summary = comp_df.groupby("id").agg(
    deltaE_per_kg_product=("impact_per_kg_product", "sum"),
    deltaE_per_kg_product_err=("impact_per_kg_product_err", lambda x: np.sqrt(np.sum(x ** 2)))
).reset_index()

data_df = data_df.merge(
    impact_summary,
    left_on="GTIN",
    right_on="id",
    how="left"
)

data_df["deltaE_per_kg_product"] = data_df["deltaE_per_kg_product"].fillna(0)
data_df["deltaE_per_kg_product_err"] = data_df["deltaE_per_kg_product_err"].fillna(0)

data_df.drop(columns=["id"], inplace=True, errors='ignore')

os.makedirs(outputs_dir, exist_ok=True)

data_df.to_csv(outputs_dir / "GS1_products_with_impacts.csv", index=False)
