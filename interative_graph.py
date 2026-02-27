import streamlit as st
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle

st.set_page_config(layout="wide")

# ======================================================
# MOCK KNOWLEDGE GRAPH (paper = evidence)
# ======================================================

MOCK_GRAPH = [
    # Original 4
    {
        "source": "BRCA1",
        "source_type": "gene",
        "target": "DNA Repair Pathway",
        "target_type": "pathway",
        "relation": "INVOLVED_IN",
        "paper": {
            "pmid": "11078742",
            "year": 2021,
            "score": 0.92,
            "snippet": "BRCA1 plays a critical role in homologous recombination DNA repair."
        }
    },
    {
        "source": "BRCA1",
        "source_type": "gene",
        "target": "Breast Cancer",
        "target_type": "disease",
        "relation": "ASSOCIATED_WITH",
        "paper": {
            "pmid": "20301589",
            "year": 2022,
            "score": 0.95,
            "snippet": "BRCA1 mutations significantly increase breast cancer risk."
        }
    },
    {
        "source": "DNA Repair Pathway",
        "source_type": "pathway",
        "target": "PARP Inhibitors",
        "target_type": "drug",
        "relation": "TARGETED_BY",
        "paper": {
            "pmid": "31234567",
            "year": 2023,
            "score": 0.96,
            "snippet": "PARP inhibitors exploit DNA repair deficiencies."
        }
    },
    {
        "source": "Breast Cancer",
        "source_type": "disease",
        "target": "PARP Inhibitors",
        "target_type": "drug",
        "relation": "TREATED_WITH",
        "paper": {
            "pmid": "28901234",
            "year": 2024,
            "score": 0.97,
            "snippet": "PARP inhibitors are approved for BRCA-mutated breast cancer."
        }
    },
    # ----------------- New nodes -----------------
    {
        "source": "TP53",
        "source_type": "gene",
        "target": "Cell Cycle",
        "target_type": "pathway",
        "relation": "REGULATES",
        "paper": {
            "pmid": "40000001",
            "year": 2020,
            "score": 0.9,
            "snippet": "TP53 controls checkpoints in the cell cycle."
        }
    },
    {
        "source": "TP53",
        "source_type": "gene",
        "target": "Lung Cancer",
        "target_type": "disease",
        "relation": "ASSOCIATED_WITH",
        "paper": {
            "pmid": "40000002",
            "year": 2021,
            "score": 0.88,
            "snippet": "Mutations in TP53 are frequent in lung cancer."
        }
    },
    {
        "source": "Cell Cycle",
        "source_type": "pathway",
        "target": "Chemotherapy",
        "target_type": "drug",
        "relation": "TARGETED_BY",
        "paper": {
            "pmid": "40000003",
            "year": 2022,
            "score": 0.87,
            "snippet": "Chemotherapy drugs target rapidly dividing cells in the cell cycle."
        }
    },
    # ---------------- Loop back to existing nodes -----------------
    {
        "source": "Chemotherapy",
        "source_type": "drug",
        "target": "PARP Inhibitors",
        "target_type": "drug",
        "relation": "SYNERGISTIC_WITH",
        "paper": {
            "pmid": "40000005",
            "year": 2023,
            "score": 0.91,
            "snippet": "Chemotherapy and PARP inhibitors show synergistic effects in certain cancers."
        }
    },
    {
        "source": "DNA Repair Pathway",
        "source_type": "pathway",
        "target": "Chemotherapy",
        "target_type": "drug",
        "relation": "TARGETED_BY",
        "paper": {
            "pmid": "40000004",
            "year": 2023,
            "score": 0.89,
            "snippet": "Chemotherapy also targets DNA repair-deficient pathways."
        }
    },
]

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

    filtered = [e for e in MOCK_GRAPH if e["paper"]["year"] >= year_filter]
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
