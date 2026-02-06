
import re

db_path = "/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/02_Visuals/Slide_Database.md"
script_path = "/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/03_Scripts/S04_Phase3_Space.md"

with open(db_path, "r") as f:
    db_content = f.read()

db_ids = set(re.findall(r"## (S04_[A-Za-z0-9_]+)", db_content))

with open(script_path, "r") as f:
    script_content = f.read()

script_refs = set(re.findall(r"\[SLIDE: (S04_[A-Za-z0-9_]+)\]", script_content))

missing = script_refs - db_ids
print(f"IDs in DB: {len(db_ids)}")
print(f"Refs in Script: {len(script_refs)}")
print(f"Missing from DB: {missing}")

# Also check for links in script that are NOT in [SLIDE: ID] format but look like IDs
script_raw_ids = set(re.findall(r"(S04_[A-Za-z0-9_]+)", script_content))
possible_ghosts = script_raw_ids - db_ids
print(f"Possible ghosts: {possible_ghosts}")
