from google.cloud import bigquery
import bigframes.pandas as bpd

bpd.options.bigquery.project = "team-2-1771992442"

query = """ CALL `team-2-1771992442.CLEANSED_BIOENTITY_RELATIONSHIP.get_traversal_results_v1`('ALPSA', 2);"""

# Execute the query and load data into a BigFrames DataFrame
df = bpd.read_gbq(query)

#df = bpd.read_gbq("team-2-1771992442.C23_BioEntities.c23_bioentities_tb")
print(df)