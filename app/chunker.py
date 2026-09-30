from pathlib import Path

knowledge_directory = Path("knowledge")

for file in knowledge_directory.glob("*.md"):

    content = file.read_text()

    document_name = file.name
    
    sections = content.split("## ")

    for section in sections:
      if not section.strip():
          continue

      lines = section.strip().splitlines()

      section_name = lines[0]
      section_content = "\n".join(lines[1:]).strip()

      if not section_content:
          continue

      chunk_text = (
          f"{document_name}\n"
          f"{section_name}\n\n"
          f"{section_content}"
      )

      chunk = {
        "document": document_name,
        "section": section_name,
        "content": section_content,
        "text": chunk_text
      }

      print("\n--- CHUNK ---")
      print("Document:", chunk["document"])
      print("Section:", chunk["section"])
      print("Text to embed:")
      print(chunk["text"])
