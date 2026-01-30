import os
import pandas as pd
import numpy as np
from pathlib import Path

data_dir = Path("data")
outputs_dir = Path("outputs")

comp_dir = data_dir / "ingredient_comp" / "Ingredient_Composition"
mapping_file = data_dir / "single_item_mapping_with_modifier_tag.csv"
impact_file = data_dir / "mrio_food_outputs" / "DNK" / "food_commodity_impacts.csv" # this is for 2021
missing_fix = pd.read_csv(data_dir / "missing_items_fix_DNK.csv")

mappings = pd.read_csv(mapping_file)
map_dict = dict(zip(mappings["Food_Category_sub_sub"], mappings["Food Commodity"]))
map_item = lambda x: map_dict.get(x, np.nan)

impacts = pd.read_csv(impact_file, index_col=0)
impact_dict = dict(zip(impacts.index, impacts["exp_extinctions_per_kg"]))
impact_uncertainty_dict = dict(zip(impacts.index, impacts["exp_extinctions_err_per_kg"]))

def map_impact_func(x):
    # have to do this because the FAO entry for a few things are missing for Denmark (Barley, Beans, Wheat)
    if x in missing_fix.Item.to_list():
        try:
            missing_item_info = missing_fix[missing_fix.Item == x]
            LIFE_value = np.sum(missing_item_info.LIFE_pkg * missing_item_info.Weight / missing_item_info.Weight.sum())
            return LIFE_value
        except IndexError:
            return np.nan
    else:
        try:
            return impact_dict[x]
        except KeyError:   
            return np.nan
        
def map_impact_err_func(x):
    # have to do this because the FAO entry for a few things are missing for Denmark (Barley, Beans, Wheat)
    if x in missing_fix.Item.to_list():
        try:
            missing_item_info = missing_fix[missing_fix.Item == x]
            LIFE_value = 0.20 * np.sum(missing_item_info.LIFE_pkg * missing_item_info.Weight / missing_item_info.Weight.sum())
            return LIFE_value
        except IndexError:
            return np.nan
    else:
        try:
            return impact_uncertainty_dict[x]
        except KeyError:   
            return np.nan

for file in comp_dir.glob("*.csv"):
    comp_df = pd.read_csv(file, low_memory=False)
    
    # carry the groups forward to fill missing values
    comp_df["identifying_category"] = comp_df["Food_Category_sub_sub"]
    comp_df["identifying_category"] = comp_df["identifying_category"].fillna(comp_df["Food_Category_sub"])
    comp_df["identifying_category"] = comp_df["identifying_category"].fillna(comp_df["Food_Category"])
    
    # map to impact items
    comp_df["mapped_commodity"] = comp_df["identifying_category"].apply(map_item)
    os.makedirs(data_dir / "processed" / "composition", exist_ok=True)
    
    # clean % field
    comp_df["percent_clean"] = pd.to_numeric(comp_df["percent"].astype(str).str.replace(r'[^0-9.]', "", regex=True),
                                errors='coerce')
    
    # comp_df["mapped_impact_kg"] = comp_df["mapped_commodity"].apply(map_impact_func)
    # comp_df["mapped_impact_kg_err"] = comp_df["mapped_commodity"].apply(map_impact_err_func)
    # compute impact per kg of product - this is a bit janky but don't have actual mass values here...
    
    comp_df["impact_per_kg_product"] = (comp_df["percent_clean"]/100) * comp_df["mapped_commodity"].apply(map_impact_func)
    comp_df["impact_per_kg_product_err"] = (comp_df["percent_clean"]/100) * comp_df["mapped_commodity"].apply(map_impact_err_func)
    
    comp_df.to_csv(data_dir / "processed" / "composition" / file.name, index=False)


    




    
