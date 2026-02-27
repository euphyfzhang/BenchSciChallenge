import streamlit as st
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle
import gcloud_auth
from google.cloud import bigquery
import bigframes.pandas as bpd
import pandas as pd
import json

st.set_page_config(layout="wide")

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
year_filter = st.sidebar.slider("Minimum publication year", 1868, 2026, 1930)
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
                #"snippet": paper["snippet"],
                "article_title": paper["article_title"],
            }
        }
    )

def build_graph(p_array):
    
    st.session_state.elements = {"nodes": [], "edges": []}

    filtered = [e for e in p_array if e["paper"]["year"] is not None and e["paper"]["year"] >= year_filter]
    filtered = sorted(filtered, key=lambda x: x["paper"][sort_by] if x["paper"][sort_by] is not None else -1, reverse=True)

    for entry in filtered:
        add_node(entry["source"], entry["source_type"])
        add_node(entry["target"], entry["target_type"])
        add_edge(entry)

# ======================================================
# BUILD GRAPH
# ======================================================



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
    EdgeStyle("REGULATES", caption="label", directed=False),
    EdgeStyle("INTERACTS", caption="label", directed=False),
    EdgeStyle("ASSOCIATED_WITH", caption="label", directed=False),
    EdgeStyle("INVOLVES", caption="label", directed=False),
    EdgeStyle("MODULATES", caption="label", directed=False),
    EdgeStyle("TREATS", caption="label", directed=False),
]

edge_styles.append(
    EdgeStyle("HIGHLIGHT", caption="label", directed=False, color="#FFD700")
)

# ======================================================
# UI
# ======================================================
st.title("🔬 Evidence-First Biomedical Knowledge Explorer")

## user input
user_input = st.text_input("Search from the database")

## retrieve user input to conduct searching
json_list = gcloud_auth.get_entities(user_input, 2, 20)

## build graph
build_graph(json_list)

query = st.text_input("Search in the graph")
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
if selected:  # This check prevents the 'NoneType' error
    
    # ---------------- EDGE (PAPER) CLICK ----------------
    if selected.get("type") == "edge":
        data = selected["data"]

        # Update sidebar with edge details
        st.sidebar.markdown(f"### 🔗 Connection Details")
        st.sidebar.markdown(f"""
        **Relation:** {data.get('label', 'N/A')}  
        **From:** {data['source']}  
        **To:** {data['target']}  

        **PMID:** {data['pmid']}  
        **Year:** {data['year']}  
        **Confidence:** {data['score']}
        **Title:** {data.get('article_title', 'N/A')}
        """)

    # ---------------- NODE CLICK ----------------
    elif selected.get("type") == "node":
        node_id = selected["data"]["id"]
        node_label = selected["data"]["label"]

        st.sidebar.markdown("### 🔹 Node Details")
        st.sidebar.write(f"**Name:** {node_id}")
        st.sidebar.write(f"**Type:** {node_label}")

        # Add to path if not already there
        if node_id not in st.session_state.path:
            st.session_state.path.append(node_id)
            # Optional: st.rerun() if you want the path to update immediately

# ======================================================
# PATH
# ======================================================
st.sidebar.markdown("### 🧭 Exploration Path")
if st.session_state.path:
    st.sidebar.write(" → ".join(st.session_state.path))
