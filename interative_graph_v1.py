import streamlit as st
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle
#import gcloud_auth
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

st.set_page_config(layout="wide")

json_list = get_entities('BRCA1', 2, 10)
#print(json_list)
st.write(json_list)


# ======================================================
# MOCK KNOWLEDGE GRAPH (paper = evidence)
# ======================================================

MOCK_GRAPH = json_list

# ======================================================
# SESSION STATE
# ======================================================
if "elements" not in st.session_state:
    st.session_state.elements = {"nodes": [], "edges": []}

if "path" not in st.session_state:
    st.session_state.path = []

# ======================================================
# SIDEBAR FILTERS
# ======================================================
st.sidebar.header("Filters")
year_filter = st.sidebar.slider("Minimum publication year", 1990, 2026, 2015)
sort_by = st.sidebar.selectbox("Sort papers by", ["year", "score"])

# ======================================================
# HELPERS
# ======================================================
def add_node(node_id, node_type):
    if node_id not in [n["data"]["id"] for n in st.session_state.elements["nodes"]]:
        st.session_state.elements["nodes"].append(
            {"data": {"id": node_id, "label": node_type}}
        )

def add_edge(entry):
    paper = entry["paper"]
    edge_id = f"PMID:{paper['pmid']}"

    if edge_id in [e["data"]["id"] for e in st.session_state.elements["edges"]]:
        return

    st.session_state.elements["edges"].append(
        {
            "data": {
                "id": edge_id,
                "source": entry["source"],
                "target": entry["target"],

                # 🔑 RELATION = EDGE TYPE + TEXT
                "label": entry["relation"],

                # Evidence
                "pmid": paper["pmid"],
                "year": paper["year"],
                "score": paper["score"],
                "snippet": paper["snippet"],
            }
        }
    )

def build_graph():
    st.session_state.elements = {"nodes": [], "edges": []}

    filtered = [e for e in MOCK_GRAPH if e.get("paper") and e["paper"].get("year") and e["paper"]["year"] >= year_filter]
    filtered = sorted(filtered, key=lambda x: x["paper"][sort_by], reverse=True)

    for entry in filtered:
        add_node(entry["source"], entry["source_type"])
        add_node(entry["target"], entry["target_type"])
        add_edge(entry)

# ======================================================
# BUILD GRAPH
# ======================================================
build_graph()

# ======================================================
# STYLES
# ======================================================
node_styles = [
    NodeStyle("gene", "#FF7F3E", "name", "gene"),
    NodeStyle("pathway", "#7D3C98", "name", "pathway"),
    NodeStyle("disease", "#2A629A", "name", "disease"),
    NodeStyle("drug", "#2A929A", "name", "drug"),
]

edge_styles = [
    EdgeStyle("ASSOCIATED_WITH", caption="label", directed=False),
    EdgeStyle("INVOLVED_IN", caption="label", directed=False),
    EdgeStyle("TARGETED_BY", caption="label", directed=False),
    EdgeStyle("TREATED_WITH", caption="label", directed=False),
]

edge_styles.append(
    EdgeStyle("HIGHLIGHT", caption="label", directed=False, color="#FFD700")
)

# ======================================================
# UI
# ======================================================
st.title("🔬 Evidence-First Biomedical Knowledge Explorer")
query = st.text_input("Search for gene, disease, drug, or pathway")

# ======================================================
# SEARCH → highlight connected edges
# ======================================================
if query:
    for edge in st.session_state.elements["edges"]:
        if edge["data"]["source"] == query or edge["data"]["target"] == query:
            edge["data"]["_original_label"] = edge["data"]["label"]
            edge["data"]["label"] = "HIGHLIGHT"
        else:
            if "_original_label" in edge["data"]:
                edge["data"]["label"] = edge["data"]["_original_label"]

# ======================================================
# RENDER GRAPH
# ======================================================
selected = st_link_analysis(
    st.session_state.elements,
    "cose",
    node_styles,
    edge_styles,
)

# ======================================================
# INTERACTIONS
# ======================================================
if selected:

    # ---------------- PAPER CLICK ----------------
   
   if selected["type"] == "edge":
    data = selected["data"]

    # Highlight logic
    for edge in st.session_state.elements["edges"]:
        edge["data"]["label"] = (
            "highlight" if edge["data"]["pmid"] == data["pmid"] else "default"
        )

    # ===== CLEAN SIDEBAR =====
    st.sidebar.markdown(f"### 🔗 {selected['data']['label']}")

    st.sidebar.markdown(f"""
    **From:** {data['source']}  
    **To:** {data['target']}  

    **PMID:** {data['pmid']}  
    **Year:** {data['year']}  
    **Confidence:** {data['score']}
    """)

    st.sidebar.markdown("**Supporting Evidence:**")
    st.sidebar.info(data["snippet"])

    # ---------------- NODE CLICK ----------------

elif selected["type"] == "node":
        node_id = selected["data"]["id"]

        for edge in st.session_state.elements["edges"]:
            edge["data"]["edge_type"] = "default"

        st.sidebar.markdown("### 🔹 Node")
        st.sidebar.write(f"**Name:** {node_id}")
        st.sidebar.write(f"**Type:** {selected['data']['label']}")

        if node_id not in st.session_state.path:
            st.session_state.path.append(node_id)

# ======================================================
# PATH
# ======================================================
st.sidebar.markdown("### 🧭 Exploration Path")
if st.session_state.path:
    st.sidebar.write(" → ".join(st.session_state.path))
