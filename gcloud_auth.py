from google.cloud import bigquery
import bigframes.pandas as bpd
import pandas as pd
import json

project_id= "team-2-1771992442"
bpd.options.bigquery.project = project_id

def get_entities(p_entity, p_depth, p_limit):
    query = f""" CALL `team-2-1771992442.CLEANSED_BIOENTITY_REL_WITH_PAPER.get_traversal_results`('{p_entity}', {p_depth}, {p_limit});"""
    df = bpd.read_gbq(query)
    local_df = df.to_pandas()
    json_data = local_df.to_json(orient="records", indent=4)
    #sample = local_df.head()
    #json_data = sample.to_json(orient="records", indent=4)
    json_list = json.loads(json_data)

    # Nest specific fields (example: nesting 'column1' and 'column2' under 'nested')
    for record in json_list:
        record['paper'] = {
            'pmid': record.pop('pmid'),
            'year': record.pop('year'),
            'article_title': record.pop('article_title'),
            'score': record.pop('score'),
            'score_1': record.pop('score_1'),
            'snippet': record.pop('snippet')
        }

        #print(record)
    return json_list
    ## client has to be used because of the read permission error.
    #client = bigquery.Client(project=project_id)
    #query_c23 = """SELECT * FROM team-2-1771992442.C23_BioEntities.c23_bioentities_tb;"""
    #query_job = client.query(query_c23)
    #results = query_job.result() 
    #data = [dict(row) for row in results]

if __name__ == "__main__":
    testdata = get_entities('BRCA1', 2, 3)
    print(type(testdata))
    print(testdata)