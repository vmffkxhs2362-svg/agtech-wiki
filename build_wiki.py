import json
import os

TEMPLATE_PATH = "_wiki_template.html"
DATA_PATH = "data/wiki_data.json"
OUT_FILE = "index.html" # Build the potato page as the index for now

def build_wiki():
    if not os.path.exists(DATA_PATH):
        print("No wiki data found.")
        return
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
        
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Generate Content HTML
    content_html = f"""
        <div class="breadcrumb">
            <a href="#" style="color: var(--primary); text-decoration: none;">AgriAtlas</a> 
            <span>/</span> <a href="#" style="color: var(--primary); text-decoration: none;">Crops</a> 
            <span>/</span> <span style="color: var(--text-muted);">{data['title']}</span>
        </div>
        
        <h1 id="overview">{data['title']}</h1>
        
        <div class="metadata">
            <span>📚 Crop Family: Solanaceae</span>
            <span>⏱️ Last Updated: 2026-07-15</span>
            <span>✍️ Contributors: AgriAtlas Automation</span>
        </div>
        
        <p style="font-size: 1.15rem; color: #cbd5e1; margin-bottom: 3rem; line-height: 1.6;">
            {data['overview']}
        </p>
        
        <h2 style="color: white; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;" id="comparison">Global Climate Comparison</h2>
    """
    
    # Generate Regional Data Blocks
    for i, region in enumerate(data['regions']):
        country_id = region['country'].lower().replace(" ", "")
        content_html += f"""
        <div class="content-box" id="{country_id}">
            <h2 style="font-family: 'Outfit'; font-size: 1.6rem; display: flex; align-items: center; gap: 0.5rem;">
                🌍 {region['country']} <span style="font-size: 0.9rem; background: rgba(255,255,255,0.1); padding: 0.2rem 0.6rem; border-radius: 12px; color: var(--text-muted); font-family: 'Inter';">{region['climate_zone']}</span>
            </h2>
            
            <h3 style="color: #fca5a5; font-size: 1rem; margin-top: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">Climate Challenge</h3>
            <p style="color: #f8fafc;">{region['challenge']}</p>
            
            <h3 style="color: var(--accent-green); font-size: 1rem; margin-top: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">Cultivation Strategy</h3>
            <p style="color: #f8fafc;">{region['strategy']}</p>
            
            <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 8px; margin-top: 2rem;">
                <h4 style="margin-top: 0; color: var(--primary); font-size: 0.95rem; text-transform: uppercase;">Key Metrics</h4>
                <ul style="color: var(--text-muted); line-height: 1.8; margin-bottom: 0; padding-left: 1.2rem;">
                    <li><strong>Planting Season:</strong> {region['key_metrics']['planting_season']}</li>
                    <li><strong>Irrigation Need:</strong> {region['key_metrics']['irrigation_need']}</li>
                    <li><strong>Primary Disease Risk:</strong> {region['key_metrics']['primary_disease']}</li>
                </ul>
            </div>
        </div>
        """
        
    # Inject into template
    output = template.replace("{{TITLE}}", f"{data['title']} | AgriAtlas")
    output = output.replace("{{DESC}}", data['description'])
    output = output.replace("{{CONTENT}}", content_html)
    
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)
        
    print("AgriAtlas Wiki built successfully: index.html generated.")

if __name__ == "__main__":
    build_wiki()
