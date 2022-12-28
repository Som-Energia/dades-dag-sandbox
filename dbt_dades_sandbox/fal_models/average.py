"""Generates Python model with forecast data

For fal to pick up these dependencies:
- ref('my_first_dbt_model')
- source('dades_sandbox', 'energy_budget')
"""


import pandas as pd

df: pd.DataFrame = ref("my_first_dbt_model")
meandf = df.mean(axis=0)

print(meandf)

print("it works")

# write to data warehouse
write_to_model(meandf)
