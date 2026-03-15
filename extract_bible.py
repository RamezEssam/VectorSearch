import os
import re

bible_path = "bible.txt"

extracted_verses_dir = "extracted_verses"

regex = re.compile(r"(.*)\s+(\d+):(\d+)\s+(.*)")

# Ensure output folder exists
os.makedirs(extracted_verses_dir, exist_ok=True)

with open(bible_path, "r") as f:
    corpus = f.read()
    for line in corpus.splitlines():
        match_groups = regex.match(line)
        if match_groups:
            book, chapter, verse, text = match_groups.groups()
            
            
            chapter_folder = os.path.join(extracted_verses_dir, f"{book}")
            
            os.makedirs(chapter_folder, exist_ok=True)
            
            verse_file = os.path.join(chapter_folder, f"{chapter}-{verse}.txt")
            
            with open(verse_file, "w", encoding="utf-8") as vf:
                vf.write(text)
            