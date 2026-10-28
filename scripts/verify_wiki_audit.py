import glob
import json
import os
import re
import shutil

WIKI_SRC = r"g:\Meine Ablage\Antigravity\Headquater\Career\AgTech_Wiki"
WIKI_PORTAL = r"g:\Meine Ablage\Antigravity\Headquater\Career\Inwoovation_Portal\wiki"

# Sync build_wiki.py and enrich_all_wiki_data.py to WIKI_PORTAL
shutil.copy2(os.path.join(WIKI_SRC, "build_wiki.py"), os.path.join(WIKI_PORTAL, "build_wiki.py"))
os.makedirs(os.path.join(WIKI_PORTAL, "scripts"), exist_ok=True)
shutil.copy2(os.path.join(WIKI_SRC, "scripts", "enrich_all_wiki_data.py"), os.path.join(WIKI_PORTAL, "scripts", "enrich_all_wiki_data.py"))


def strip_visible_words(html_text):
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", html_text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    words = [w for w in text.split() if w.strip()]
    return len(words)


def audit_directory(target_dir):
    html_files = sorted([
        p for p in glob.glob(os.path.join(target_dir, "*.html"))
        if not os.path.basename(p).startswith("_")
    ])
    print(f"\n=== AUDITING {target_dir} ({len(html_files)} pages) ===")

    low_word_pages = []
    meta_errors = []
    img_alt_errors = []
    na_errors = []
    author_leak_errors = []
    h1_errors = []
    schema_errors = []
    adsense_errors = []
    eeat_errors = []

    min_words = 999999
    max_words = 0
    min_file = ""

    for p in html_files:
        fn = os.path.basename(p)
        with open(p, "r", encoding="utf-8") as f:
            raw = f.read()

        wc = strip_visible_words(raw)
        if wc < min_words:
            min_words = wc
            min_file = fn
        if wc > max_words:
            max_words = wc
        if wc < 550:
            low_word_pages.append((fn, wc))

        # Check meta description
        m_desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', raw, re.IGNORECASE)
        if not m_desc or len(m_desc.group(1).strip()) < 50 or len(m_desc.group(1).strip()) > 160:
            meta_errors.append((fn, "meta description", m_desc.group(1) if m_desc else "MISSING"))

        # Check og:title, og:description, og:image
        for og_prop in ("og:title", "og:description", "og:image"):
            m_og = re.search(rf'<meta\s+property="{og_prop}"\s+content="([^"]*)"', raw, re.IGNORECASE)
            if not m_og or not m_og.group(1).strip():
                meta_errors.append((fn, og_prop, "EMPTY/MISSING"))

        # Check canonical
        m_can = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', raw, re.IGNORECASE)
        if not m_can or not m_can.group(1).startswith("https://inwoovation.com/wiki/"):
            meta_errors.append((fn, "canonical", m_can.group(1) if m_can else "MISSING"))

        # Check img alt
        for img_tag in re.findall(r"<img\b[^>]*>", raw, re.IGNORECASE):
            m_alt = re.search(r'\balt="([^"]*)"', img_tag, re.IGNORECASE)
            if not m_alt or not m_alt.group(1).strip():
                img_alt_errors.append((fn, img_tag))

        # Check N/A
        if "N/A" in raw:
            na_errors.append(fn)

        # Check legacy handle
        legacy_handle = "vmffkxhs" + "2362"
        if legacy_handle in raw:
            author_leak_errors.append(fn)

        # Check h1 count
        h1s = re.findall(r"<h1\b[^>]*>.*?</h1>", raw, flags=re.DOTALL | re.IGNORECASE)
        if len(h1s) != 1:
            h1_errors.append((fn, len(h1s)))

        # Check JSON-LD Article schema
        m_ld = re.search(r'<script\s+type="application/ld\+json">\s*(.*?)\s*</script>', raw, flags=re.DOTALL | re.IGNORECASE)
        if not m_ld:
            schema_errors.append((fn, "Missing JSON-LD"))
        else:
            try:
                ld_obj = json.loads(m_ld.group(1))
                if ld_obj.get("@type") != "Article" or ld_obj.get("author", {}).get("name") != "Inwoo Hwang":
                    schema_errors.append((fn, "Invalid JSON-LD fields"))
            except Exception as e:
                schema_errors.append((fn, str(e)))

        # Check AdSense
        if 'content="ca-pub-8597809158257497"' not in raw or 'client=ca-pub-8597809158257497' not in raw:
            adsense_errors.append(fn)

        # Check E-E-A-T Box
        if "Inwoo Hwang — Horticultural &amp; CEA Systems Engineer, Inwoovation Lab" not in raw:
            eeat_errors.append(fn)

    print(f"  Total pages audited: {len(html_files)}")
    print(f"  Visible word count range: {min_words}w ({min_file}) to {max_words}w")
    print(f"  Pages with < 550 visible words: {len(low_word_pages)} {low_word_pages}")
    print(f"  Pages with meta/OG/canonical errors: {len(meta_errors)} {meta_errors}")
    print(f"  <img> tags with empty/missing alt: {len(img_alt_errors)} {img_alt_errors}")
    print(f"  Pages with 'N/A': {len(na_errors)} {na_errors}")
    print(f"  Pages with legacy handle: {len(author_leak_errors)} {author_leak_errors}")
    print(f"  Pages without exactly 1 <h1>: {len(h1_errors)} {h1_errors}")
    print(f"  Pages with JSON-LD schema errors: {len(schema_errors)} {schema_errors}")
    print(f"  Pages with AdSense errors: {len(adsense_errors)} {adsense_errors}")
    print(f"  Pages with E-E-A-T Author Box errors: {len(eeat_errors)} {eeat_errors}")

    # Also check all JSON/JS/PY files for legacy handle
    leaks_any = []
    for root, dirs, files in os.walk(target_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            if f.endswith((".json", ".html", ".js", ".py")):
                fp = os.path.join(root, f)
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    if legacy_handle in fh.read():
                        leaks_any.append(os.path.relpath(fp, target_dir))
    print(f"  Any file with legacy handle: {len(leaks_any)} {leaks_any}")


if __name__ == "__main__":
    audit_directory(WIKI_PORTAL)
    audit_directory(WIKI_SRC)
