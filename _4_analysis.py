import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from scipy import stats

outputs_dir = Path("outputs")

impact_df = pd.read_csv(outputs_dir / "GS1_products_with_impacts.csv")

Y = impact_df["deltaE_per_kg_product"].dropna().to_numpy()
X = impact_df[~np.isnan(impact_df["deltaE_per_kg_product"])].mean_Biodiversity.to_numpy()

valid_mask = (
    ~np.isnan(impact_df["deltaE_per_kg_product"]) & 
    ~np.isnan(impact_df["mean_Biodiversity"]) &
    (impact_df["deltaE_per_kg_product"] > 0) &
    (impact_df["mean_Biodiversity"] > 0)
)

Y = np.log10(impact_df.loc[valid_mask, "deltaE_per_kg_product"].to_numpy())
X = np.log10(impact_df.loc[valid_mask, "mean_Biodiversity"].to_numpy())

slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)

print(f"Power law exponent (m): {slope:.3f}")
print(f"R-squared: {r_value**2:.3f}")
linedesc = f"Original relationship: LIFE ≈ {10**intercept:.3e}*OriginalBD^{slope:.3f}"
print(linedesc)

label = f"{linedesc}, Slope={slope:.2f}, $R^2$={r_value**2:.2f}"
plt.scatter(X, Y, alpha=0.3)
plt.plot(X, slope*X + intercept, 'r-', label=label,
         alpha = 0.7)
plt.xlabel('log10(Original Biodiversity Impact)')
plt.ylabel('log10(LIFE)')
plt.legend()
plt.show()