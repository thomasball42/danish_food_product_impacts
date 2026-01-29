import os
import pandas as pd
import numpy as np
from pathlib import Path

data_dir = Path("data")
outputs_dir = Path("outputs")

dat_path = data_dir / "GS1" / "OptiusGS1MatchingImpacts" / "2025-12-10_optiusGS1_matched_impacts_PRELIMINARY.tsv"
comp_dir = data_dir / "ingredient_comp" / "Ingredient_Composition"
mapping_file = data_dir / "single_item_mapping_with_modifier_tag.csv"

impact_file = data_dir / "mrio_food_outputs" / "DNK" / "impacts_aggregated.csv" # this is for 2021


mappings = pd.read_csv(mapping_file)
map_dict = dict(zip(mappings["Food_Category_sub_sub"], mappings["Food Commodity"]))
map_item = lambda x: map_dict.get(x, np.nan)

impacts = pd.read_csv(impact_file)

for file in comp_dir.glob("*.csv"):

    comp_df = pd.read_csv(file)
    # carry the groups forward to fill missing values
    comp_df["identifying_category"] = comp_df["Food_Category_sub_sub"]
    comp_df["identifying_category"] = comp_df["identifying_category"].fillna(comp_df["Food_Category_sub"])
    comp_df["identifying_category"] = comp_df["identifying_category"].fillna(comp_df["Food_Category"])
    comp_df["mapped_commodity"] = comp_df["identifying_category"].apply(map_item)
    os.makedirs(data_dir / "processed" / "composition", exist_ok=True)

    
    
    comp_df.to_csv(data_dir / "processed" / "composition" / file.name, index=False)




    
