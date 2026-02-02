import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SLIDES_JSON = PROJECT_ROOT / "04_Delivery/h5_preview/public/slides.json"
TIMELINE_JSON = PROJECT_ROOT / "03_Scripts/timeline.json"

def migrate():
    if not SLIDES_JSON.exists():
        print("❌ slides.json not found!")
        return

    print(f"📖 Reading {SLIDES_JSON}...")
    with open(SLIDES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    timings = {}
    count = 0

    for section in data.get("sections", []):
        for slide in section.get("slides", []):
            if "startTime" in slide:
                sid = slide["id"]
                timings[sid] = slide["startTime"]
                count += 1
    
    print(f"💾 Saving {count} timestamps to {TIMELINE_JSON}...")
    with open(TIMELINE_JSON, "w", encoding="utf-8") as f:
        json.dump(timings, f, indent=2, sort_keys=True)
    
    print("✅ Migration Complete!")

if __name__ == "__main__":
    migrate()
