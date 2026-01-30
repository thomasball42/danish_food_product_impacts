from pathlib import Path
import os
import zipfile

def main():
    if not os.path.exists(Path("data", "GS1", "OptiusGS1MatchingImpacts", "2025-12-10_optiusGS1_matched_impacts_PRELIMINARY.tsv")):
        zip_path = Path("data", "OptiusGS1MatchingImpacts.zip")
        os.makedirs(Path(zip_path.parent, "GS1"), exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(Path(zip_path.parent, "GS1"))

    extr_name = Path("Denmark_percent_composition_by_ingredient Food_Beverage_Beverages_2025-12-05.csv")
    if not os.path.exists(Path("data", "ingredient_comp", "Ingredient_Composition", extr_name)):
        zip_path = Path("data", "Ingredient_Composition.zip")
        os.makedirs(Path(zip_path.parent, "ingredient_comp"), exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(Path(zip_path.parent, "ingredient_comp"))

    extr_name = Path("food_commodity_impacts.csv")
    if not os.path.exists(Path("data", "DNK", extr_name)):
        zip_path = Path("data", "DNK.zip")
        os.makedirs(Path(zip_path.parent, "mrio_food_outputs"), exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(Path(zip_path.parent, "mrio_food_outputs"))   

if __name__ == "__main__":
    main()