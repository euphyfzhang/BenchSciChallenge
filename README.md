# BioLinker
## Interactive Biomedical Knowledge Graph Explorer
Access Deployed Project Here: https://interactive-graph-v1-166284934075.us-central1.run.app/

### Project Overview
PubMed contains millions of biomedical papers, but discovering meaningful relationships between genes, diseases, and research findings can be overwhelming.

**BioLinker** is an interactive knowledge graph tool that allows scientists to explore these relationships visually. Instead of reading abstracts one by one, users can expand nodes representing genes, diseases, and papers, uncovering connections step by step.

---

### Key Features
- **Interactive Graph**  
  Nodes represent genes, diseases, or papers; edges show relationships.
- **Hop-by-Hop Exploration**  
  Expand the graph progressively to explore connections without being overwhelmed.
- **Literature Integration**  
  Each node links directly to supporting PubMed papers.
- **Scalable Backend**  
  Uses GCP Bucket + BigQuery for fast querying of large datasets.
- **User-Friendly Interface**  
  Built with Streamlit for simple web access and visualization.

---

### System Architecture
- **GCP Bucket**: Stores PubMed data (bioentities, relationships, and papers)
- **BigQuery**: Efficiently queries and processes large-scale biomedical data
- **Streamlit App**: Renders the interactive knowledge graph
- **Interactive Graph UI**: Enables visual exploration of scientific connections

---

### Tech Stack
- **Cloud**: Google Cloud Platform (GCP)
- **Data Processing**: BigQuery
- **Frontend**: Streamlit + Interactive Graph Component
- **Data**: PubMed TSV files containing bioentities, relationships, and related papers

---

### Demo Example
1. Search for a gene (e.g., **BRCA1**)
2. Expand the node to view related diseases and genes
3. Click nodes to view supporting research papers

---

### Future Improvements
- Multi-hop expansion controls
- Integration with the STRING database for protein–protein interaction evidence
- Ranking nodes based on interaction strength or citation count
- Exportable graphs and reports for research use

---

### Team
- **Isha B.** – Frontend / Demo
- **Charisse C.** – Product Lead / PM (Non-Technical)
- **Euphemia Z.** – Backend / Data
- **David T.** – Infrastructure / Architecture
