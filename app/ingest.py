from pathlib import Path

knowledge_directory = Path("knowledge")

for file in knowledge_directory.glob("*.md"):
    print("\n---", file.name, "---")

    content = file.read_text()

    print(content)
