import os
import json
import re

def analyze_repo(root_dir='.'):
    analysis = {
        'frameworks': [],
        'languages': set(),
        'services': [],
        'databases': [],
        'deployment': [],
        'env_vars': set(),
        'structure': {},
        'external_integrations': []
    }

    knowledge_graph = {
        'nodes': [],
        'edges': []
    }

    # Map file extensions to languages
    ext_to_lang = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.html': 'HTML',
        '.css': 'CSS',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP'
    }

    # Framework indicators (simplistic)
    framework_indicators = {
        'django': 'Django',
        'flask': 'Flask',
        'react': 'React',
        'vue': 'Vue',
        'angular': 'Angular',
        'express': 'Express',
        'spring': 'Spring Boot',
        'next.js': 'Next.js'
    }

    # DB indicators
    db_indicators = {
        'postgres': 'PostgreSQL',
        'mysql': 'MySQL',
        'mongodb': 'MongoDB',
        'redis': 'Redis',
        'sqlite': 'SQLite'
    }

    # Deployment indicators
    deploy_indicators = {
        'dockerfile': 'Docker',
        'docker-compose': 'Docker Compose',
        'kubernetes': 'Kubernetes',
        'helm': 'Helm',
        'terraform': 'Terraform',
        'vercel': 'Vercel',
        'netlify': 'Netlify',
        'heroku': 'Heroku',
        'aws': 'AWS',
        'gcp': 'Google Cloud'
    }

    ignore_dirs = {'.git', 'node_modules', 'venv', '__pycache__', '.github', 'dist', 'build'}

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        rel_root = os.path.relpath(root, root_dir)
        if rel_root == '.':
            rel_root = 'root'

        analysis['structure'][rel_root] = []

        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.join(rel_root, file)

            analysis['structure'][rel_root].append(file)

            # Languages
            _, ext = os.path.splitext(file)
            if ext in ext_to_lang:
                analysis['languages'].add(ext_to_lang[ext])

            # Frameworks, DBs from config files
            if file.lower() in ('package.json', 'requirements.txt', 'pom.xml', 'go.mod'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for key, name in framework_indicators.items():
                            if key in content:
                                if name not in analysis['frameworks']:
                                    analysis['frameworks'].append(name)
                        for key, name in db_indicators.items():
                            if key in content:
                                if name not in analysis['databases']:
                                    analysis['databases'].append(name)
                except Exception:
                    pass

            # Deployment
            lower_file = file.lower()
            if 'dockerfile' in lower_file:
                if 'Docker' not in analysis['deployment']: analysis['deployment'].append('Docker')
            if 'docker-compose' in lower_file:
                if 'Docker Compose' not in analysis['deployment']: analysis['deployment'].append('Docker Compose')

            # Env vars
            if ext in ('.py', '.js', '.ts'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Very simplistic regex for env vars
                        env_matches = re.findall(r'os\.environ\.get\([\'"]([A-Z0-9_]+)[\'"]\)', content)
                        env_matches += re.findall(r'process\.env\.([A-Z0-9_]+)', content)
                        for match in env_matches:
                            analysis['env_vars'].add(match)
                except Exception:
                    pass

            # Basic Node for Graph
            node_id = rel_path.replace('\\', '/')
            knowledge_graph['nodes'].append({'id': node_id, 'label': file, 'type': 'file'})
            if rel_root != 'root':
                 knowledge_graph['edges'].append({'source': rel_root.replace('\\', '/'), 'target': node_id, 'type': 'contains'})

    # Convert sets to lists for JSON
    analysis['languages'] = list(analysis['languages'])
    analysis['env_vars'] = list(analysis['env_vars'])

    with open('repo_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)

    with open('repo_knowledge_graph.json', 'w') as f:
        json.dump(knowledge_graph, f, indent=2)

    print("Repository analysis complete. Outputs written to repo_analysis.json and repo_knowledge_graph.json")

if __name__ == '__main__':
    analyze_repo()
