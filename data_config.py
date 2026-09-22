import numpy as np
import pandas as pd

TABLE_DF = pd.DataFrame({
    "product": ["Widget A", "Widget B", "Widget C", "Widget D", "Widget E"],
    "region": ["North", "South", "East", "West", "North"],
    "units_sold": [120, 85, 200, 60, 150],
    "revenue": [2400.00, 1700.00, 5000.00, 1200.00, 3000.00],
})


rng = np.random.default_rng(seed=42) # seeded random numbers

date_range = pd.date_range(start="2025-01-01", end="2025-03-31", freq="D")

COLLAPSIBLE_TABLE_DF = pd.DataFrame({
    "date": date_range,
    "product": rng.choice(["Widget A", "Widget B", "Widget C"], size=len(date_range)),
    "region": rng.choice(["North", "South", "East", "West"], size=len(date_range)),
    "units_sold": rng.integers(10, 100, size=len(date_range)),
    "revenue": rng.uniform(100, 2000, size=len(date_range)).round(2),
})