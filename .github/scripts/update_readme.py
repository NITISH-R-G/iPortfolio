import json
import re

def update_readme():
    try:
        with open('README.md', 'r') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print("README.md not found. Cannot update.")
        return

    # Load analysis data
    try:
        with open('repo_analysis.json', 'r') as f:
            analysis = json.load(f)
    except FileNotFoundError:
        analysis = {}

    # Load diagrams
    try:
        with open('diagrams.md', 'r') as f:
            diagrams = f.read()
    except FileNotFoundError:
        diagrams = "*Diagrams not available yet.*"

    # Load AI summary
    try:
        with open('ai_summary.md', 'r') as f:
            ai_summary = f.read()
    except FileNotFoundError:
        ai_summary = "*AI summary not available yet.*"

    # Construct Architecture Section
    arch_section = "### Technology Stack\n\n"
    if analysis.get('languages'):
        arch_section += f"**Languages**: {', '.join(analysis['languages'])}\n\n"
    if analysis.get('frameworks'):
        arch_section += f"**Frameworks**: {', '.join(analysis['frameworks'])}\n\n"
    if analysis.get('databases'):
        arch_section += f"**Databases**: {', '.join(analysis['databases'])}\n\n"
    if analysis.get('deployment'):
        arch_section += f"**Deployment**: {', '.join(analysis['deployment'])}\n\n"

    arch_section += "### Environment Variables\n\n"
    if analysis.get('env_vars'):
        arch_section += "The following environment variables were detected:\n"
        for ev in analysis['env_vars']:
            arch_section += f"- `{ev}`\n"
    else:
         arch_section += "No specific environment variables detected.\n"

    arch_section += "\n### Directory Structure\n\n```\n"
    for dir_path, files in analysis.get('structure', {}).items():
        if len(files) > 0 and len(files) < 15: # Arbitrary limit for brevity
            arch_section += f"{dir_path}/\n"
            for file in files:
                arch_section += f"  ├── {file}\n"
    arch_section += "```\n"

    # Replace markers in README
    def replace_section(marker, new_content, text):
        start_marker = f"<!-- START_{marker} -->"
        end_marker = f"<!-- END_{marker} -->"
        pattern = f"({start_marker}).*?({end_marker})"
        replacement = f"\\1\n{new_content}\n\\2"
        return re.sub(pattern, replacement, text, flags=re.DOTALL)

    readme_content = replace_section("ARCHITECTURE", arch_section, readme_content)
    readme_content = replace_section("DIAGRAMS", diagrams, readme_content)
    readme_content = replace_section("AI_SUMMARY", ai_summary, readme_content)

    with open('README.md', 'w') as f:
        f.write(readme_content)

    print("README.md updated successfully.")

if __name__ == '__main__':
    update_readme()
