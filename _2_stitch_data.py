from pathlib import Path
import pandas as pd

composition_dir = Path("data") / "processed" / "composition"

def main():
    output_df = pd.DataFrame()
    for file in composition_dir.glob("*.csv"):

        print(f"Appending {file.name}...")
        df = pd.read_csv(file, low_memory=False)
        output_df = pd.concat([output_df, df], ignore_index=True)

    output_df.to_csv(Path("data") / "processed" / "all_compositions.csv", index=False)

if __name__ == "__main__":
    main()