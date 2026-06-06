import os
import subprocess
import json

def get_git_diff():
    try:
        # Get diff of the last commit or uncommitted changes
        result = subprocess.run(['git', 'diff', 'HEAD~1', 'HEAD'], capture_output=True, text=True)
        if not result.stdout:
            result = subprocess.run(['git', 'diff'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error getting git diff: {e}")
        return ""

import requests

def generate_ai_summary(diff):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
         print("No OpenAI API key found. Using fallback summary.")
         return "No AI summary available (OPENAI_API_KEY not set)."

    if not diff:
        return "No recent changes detected."

    prompt = (
        "You are an AI repository maintainer. Analyze the following git diff and "
        "provide a summary of the architectural modifications, new features, or key code changes.\n\n"
        f"Diff:\n{diff[:10000]}" # Limit to avoid token limits
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful software engineer assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        summary = response.json()['choices'][0]['message']['content']
        return f"### Recent Architectural Changes\n\n{summary}"
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "Failed to generate AI summary due to an API error."

def main():
    diff = get_git_diff()
    summary = generate_ai_summary(diff)

    with open('ai_summary.md', 'w') as f:
        f.write(summary)

    print("AI summary generated and written to ai_summary.md")

if __name__ == '__main__':
    main()
