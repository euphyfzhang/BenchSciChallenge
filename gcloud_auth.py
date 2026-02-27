from google.cloud import bigquery
import bigframes.pandas as bpd
import pandas as pd

bpd.options.bigquery.project = "team-2-1771992442"

query = """ CALL `team-2-1771992442.CLEANSED_BIOENTITY_RELATIONSHIPS.get_traversal_results`('BRCA1', 2, 50);"""

# Execute the query and load data into a BigFrames DataFrame
df = bpd.read_gbq(query)

#df = bpd.read_gbq("team-2-1771992442.C23_BioEntities.c23_bioentities_tb")

local_df = df.to_pandas()

# 2. Now standard Pandas formatting works perfectly
json_data = local_df.to_json(orient="records", indent=4)

print(json_data)