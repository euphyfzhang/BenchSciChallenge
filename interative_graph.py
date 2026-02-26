import streamlit as st
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle

st.set_page_config(layout="wide")

# Sample Data
elements = {
    "nodes": [
        {"data": {"id": 1, "label": "gene", "name": "BRCA1"}},
        {"data": {"id": 2, "label": "gene", "name": "BRCA2"}},
        {"data": {"id": 3, "label": "disease", "content": "sometumor1"}},
        {"data": {"id": 4, "label": "disease", "content": "sometumor2"}},
        {"data": {"id": 5, "label": "drug", "content": "somedrug1"}},
    ],
    "edges": [
        {"data": {"id": 6, "label": "RELATED", "source": 1, "target": 2}},
        {"data": {"id": 7, "label": "CAUSES", "source": 2, "target": 3}},
        {"data": {"id": 7, "label": "CAUSES", "source": 1, "target": 3}},
        {"data": {"id": 8, "label": "CAUSES", "source": 3, "target": 4}},
        {"data": {"id": 9, "label": "CONTROLS", "source": 5, "target": 3}},
        {"data": {"id": 10, "label": "CONTROLS", "source": 5, "target": 4}},
    ],
}

# Style node & edge groups
node_styles = [
    NodeStyle("gene", "#FF7F3E", "name", "gene"),
    NodeStyle("disease", "#2A629A", "content", "disease"),
    NodeStyle("drug", "#2A929A", "content", "drug"),
]

edge_styles = [
    EdgeStyle("RELATED", caption='label', directed=True),
    EdgeStyle("CAUSES", caption='label', directed=True),
    EdgeStyle("CONTROLS", caption='label', directed=True),
]

# Render the component
st.markdown("### BenchSci Challenge 5")
st.markdown("by Team 2")
st_link_analysis(elements, "cose", node_styles, edge_styles)