from pathlib import Path
import pandas as pd

composition_dir = Path("data") / "processed" / "composition"

output_df = pd.DataFrame()
for file in composition_dir.glob("*.csv"):
    df = pd.read_csv(file, low_memory=False)
    output_df = pd.concat([output_df, df], ignore_index=True)

output_df.to_csv(Path("data") / "processed" / "all_compositions.csv", index=False)