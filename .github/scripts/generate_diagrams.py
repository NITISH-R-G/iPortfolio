import json

def generate_diagrams():
    try:
        with open('repo_knowledge_graph.json', 'r') as f:
            kg = json.load(f)
    except FileNotFoundError:
        print("repo_knowledge_graph.json not found. Run analyze_repo.py first.")
        return

    # Basic mapping of graph to Mermaid
    mermaid_lines = ["```mermaid", "graph TD;"]

    # We'll just show directory structure to keep it manageable
    # Extract unique directories from edges
    dirs = set()
    for edge in kg.get('edges', []):
        if edge.get('type') == 'contains':
            source = edge['source']
            target = edge['target']

            # Simplified diagram: only show dir -> dir relationships or dir -> file limit
            source_parts = source.split('/')
            target_parts = target.split('/')

            if len(target_parts) > len(source_parts):
                 # It's a file or subfolder
                 s_clean = source.replace('.', '').replace('-', '_').replace(' ', '_')
                 t_clean = target.replace('.', '').replace('-', '_').replace(' ', '_').replace('/', '_')
                 mermaid_lines.append(f"    {s_clean}[{source}] --> {t_clean}[{target_parts[-1]}];")

    # Limit nodes to avoid massive diagrams
    if len(mermaid_lines) > 100:
        mermaid_lines = mermaid_lines[:100]
        mermaid_lines.append("    ...[Diagram truncated due to size]")

    mermaid_lines.append("```")

    with open('diagrams.md', 'w') as f:
        f.write("\n".join(mermaid_lines))

    print("Diagrams generated and written to diagrams.md")

if __name__ == '__main__':
    generate_diagrams()
