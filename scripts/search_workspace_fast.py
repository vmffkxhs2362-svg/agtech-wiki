import os

search_dir = r"g:\My Drive\Antigravity\Headquater"
print(f"Searching fast in {search_dir}...")

matched = []
for root, dirs, files in os.walk(search_dir):
    # Exclude directories
    if any(p in root for p in ["2025 Dawoovac", ".git", "node_modules", "Archive"]):
        continue
    for f in files:
        if "딸기" in f and f.endswith(".pdf"):
            full_path = os.path.join(root, f)
            print(f"Found PDF: {full_path}")
            matched.append(full_path)

print(f"Total matched: {len(matched)}")
