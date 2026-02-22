# fix_imports.py
import os

files_to_fix = {
    "app/llm/openai_client.py": [
        "import logging\n",
    ],
    "app/agents/risk_agent.py": [
        "import asyncio\n",
    ],
    "app/agents/sprint_agent.py": [
        "import asyncio\n",
        "import re\n",
    ],
    "app/agents/devops_agent.py": [
        "import asyncio\n",
    ],
    "app/agents/architect_agent.py": [
        "import asyncio\n",
    ],
    "app/agents/code_review_agent.py": [
        "import asyncio\n",
    ]
}

def fix_imports():
    for file_path, imports in files_to_fix.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if imports already exist
            for imp in imports:
                if imp.strip() not in content:
                    # Add import after the last import
                    lines = content.split('\n')
                    last_import_line = -1
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            last_import_line = i
                    
                    if last_import_line >= 0:
                        lines.insert(last_import_line + 1, imp.strip())
                    else:
                        # No imports found, add at beginning
                        lines.insert(0, imp.strip())
                    
                    content = '\n'.join(lines)
                    print(f"✅ Added {imp.strip()} to {file_path}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"❌ File not found: {file_path}")

if __name__ == "__main__":
    fix_imports()
    print("\n🎉 All imports fixed! Run the app again.")