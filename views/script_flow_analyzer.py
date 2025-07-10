from io import BytesIO
import streamlit as st
import re
import networkx as nx
from graphviz import Digraph

st.set_page_config(page_title="Qlik Sense ETL Visualizer", layout="wide")

st.title("Qlik Sense ETL Visualizer")

# ────────────────────────────────────────────────────────────────────────────────

# 1. Upload script

# ────────────────────────────────────────────────────────────────────────────────


uploaded_file = st.file_uploader(
    "Upload your Qlik Sense load script ( .qvs or .txt )",
    type=["qvs", "txt"],
)

if not uploaded_file:
    st.info("👆 Upload a script file to get started.")
    st.stop()

script_text = uploaded_file.read().decode("utf-8", errors="ignore")
# ────────────────────────────────────────────────────────────────────────────────

# 2. Helper functions

# ────────────────────────────────────────────────────────────────────────────────


def strip_comments(text: str) -> str:
    """Remove // single‑line and /* ... */ multi‑line comments."""
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return text


def parse_script(text: str) -> nx.DiGraph:
    """
    Parse a Qlik Sense script and build a dependency graph.
    Heuristic‑based: detects LOAD/RESIDENT/JOIN/CONCATENATE and optional
    table labels (e.g. `MyTable:`). Adjust regexes for rare constructs.
    """

    cleaned = strip_comments(text)
    statements = [s.strip() for s in re.split(r";\s*(?:\r?\n|$)", cleaned) if s.strip()]
    g: nx.DiGraph = nx.DiGraph()

    for stmt in statements:
        label_match = re.match(r"^([\w\$]+)\s*:\s*", stmt)
        target_table: str | None = None
        stmt_body = stmt

        if label_match:
            target_table = label_match.group(1)
            stmt_body = stmt[label_match.end():].lstrip()
            g.add_node(target_table)

        if res := re.search(r"RESIDENT\s+([\w\$]+)", stmt_body, flags=re.I):
            source = res.group(1)
            g.add_node(source)
            tgt = target_table or f"Step_{len(g)}"
            g.add_node(tgt)
            g.add_edge(source, tgt, label="RESIDENT")
            target_table = tgt

        if join := re.search(r"(?:LEFT|RIGHT|INNER|OUTER)?\s*JOIN\s*\(([^)]+)\)", stmt_body, flags=re.I):
            source = join.group(1).strip()
            g.add_node(source)
            tgt = target_table or f"Step_{len(g)}"
            g.add_node(tgt)
            g.add_edge(source, tgt, label="JOIN")
            target_table = tgt

        if concat := re.search(r"CONCATENATE\s*\(([^)]+)\)", stmt_body, flags=re.I):
            dest = concat.group(1).strip()
            src = target_table or f"Step_{len(g)}"
            g.add_node(dest)
            g.add_node(src)
            g.add_edge(src, dest, label="CONCATENATE")

        if target_table and g.in_degree(target_table) == 0 and g.out_degree(target_table) == 0:
            g.add_node(target_table)

    return g

def build_graphviz(graph: nx.DiGraph) -> Digraph:
    """Convert a NetworkX graph to a Graphviz Digraph with vertical layout."""

    dot = Digraph(format='svg')
    dot.attr(rankdir='TB', concentrate='true')

    for node in graph.nodes:
        dot.node(node, shape='box', style='rounded,filled', fillcolor='#EFEFEF', fontsize='10')

    for u, v, data in graph.edges(data=True):
        label = data.get('label', '')
        dot.edge(u, v, label=label, fontsize='9', arrowsize='0.7')

    return dot

# ────────────────────────────────────────────────────────────────────────────────


# 3. Build the graph


# ────────────────────────────────────────────────────────────────────────────────

try:
    graph = parse_script(script_text)

except Exception as e:
    st.error(f"❌ Failed to parse script: {e}")
    st.stop()

if not graph:
    st.warning("No LOAD/JOIN/RESIDENT/CONCATENATE statements found.")
    st.stop()

# ────────────────────────────────────────────────────────────────────────────────

# 4. Display: collapsible flowchart, tables, and downloads
# ────────────────────────────────────────────────────────────────────────────────
dot_graph = build_graphviz(graph)

with st.expander("🔄 ETL Flowchart (click to expand/collapse)", expanded=True):
    st.graphviz_chart(dot_graph.source, use_container_width=True)

    # Download as PNG
    # png_data = BytesIO(dot_graph.pipe(format='png'))
    # st.download_button("🖼️ Download as PNG", data=png_data, file_name="etl_flowchart.png", mime="image/png")

with st.expander("📋 Detected Tables & Steps"):
    st.write(sorted(graph.nodes))

with st.expander("💾 Download DOT Source"):
    st.download_button(
        "Download .dot",
        data=dot_graph.source.encode("utf-8"),
        file_name="etl_flow.dot",
        mime="text/vnd.graphviz",
    )

st.success("✅ Flowchart generated using Graphviz Python package.")