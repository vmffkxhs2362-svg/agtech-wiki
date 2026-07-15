import json
import os
import glob

TEMPLATE_PATH = "_wiki_template.html"
CROPS_DIR = "data/crops/"
OUT_DIR = "./"

def generate_navigation(crops, active_id):
    # Sort crops alphabetically by title
    crops_sorted = sorted(crops, key=lambda x: x['title'])
    nav_html = ""
    for crop in crops_sorted:
        active_class = " active" if crop['id'] == active_id else ""
        nav_html += f'<a href="{crop["id"]}.html" class="nav-link{active_class}">{crop["title"]}</a>\n            '
    return nav_html

def build_crop_page(template, data, nav_html):
    content_html = f"""
        <div class="breadcrumb">
            <a href="index.html" style="color: var(--primary); text-decoration: none;">AgriAtlas</a> 
            <span>/</span> <a href="#" style="color: var(--primary); text-decoration: none;">Crops</a> 
            <span>/</span> <span style="color: var(--text-muted);">{data['title']}</span>
        </div>
        
        <h1 id="overview">{data['title']}</h1>
    """
    
    if "image_url" in data:
        content_html += f"""
        <figure style="margin: 0 0 2rem 0; width: 100%;">
            <img src="{data['image_url']}" alt="{data.get('image_caption', '')}" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; border: 1px solid var(--border);">
            <figcaption style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-top: 0.5rem;">{data.get('image_caption', '')}</figcaption>
        </figure>
        """
        
    content_html += f"""
        <div class="metadata">
            <span>📚 Crop Family: Solanaceae (Mock)</span>
            <span>⏱️ Last Updated: 2026-07-15</span>
            <span>✍️ Contributors: AgriAtlas Automation</span>
        </div>
        
        <p style="font-size: 1.15rem; color: #cbd5e1; margin-bottom: 3rem; line-height: 1.6;">
            {data.get('overview', '')}
        </p>
    """

    # Section 2: Global Climate Strategy
    if 'climate_strategy' in data:
        content_html += f"""
            <h2 style="color: white; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;" id="climate-strategy">Global Climate Strategy</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 3rem;">
        """
        for strat in data['climate_strategy']:
            content_html += f"""
                <div class="content-box" style="margin-bottom: 0;">
                    <h3 style="margin-top: 0; color: var(--primary); font-size: 1.2rem;">🌍 {strat.get('region', '')}</h3>
                    <p style="color: #f8fafc; font-size: 0.95rem; line-height: 1.5;">{strat.get('strategy', '')}</p>
                    <span style="font-size: 0.85rem; color: var(--text-muted); background: rgba(0,0,0,0.3); padding: 0.3rem 0.6rem; border-radius: 6px; display: inline-block; margin-top: 1rem;">⚙️ Tech: {strat.get('tech_level', '')}</span>
                </div>
            """
        content_html += "</div>"

    # Section 3: Crop Steering
    if 'crop_steering' in data:
        cs = data['crop_steering']
        content_html += f"""
            <h2 style="color: white; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;" id="crop-steering">Crop Steering Parameters</h2>
            <p style="color: #cbd5e1; margin-bottom: 2rem;">{cs.get('intro', '')}</p>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 3rem; background: rgba(30, 41, 59, 0.5); border-radius: 12px; overflow: hidden; border: 1px solid var(--border);">
                <thead>
                    <tr style="background: rgba(0,0,0,0.3);">
                        <th style="padding: 1rem; text-align: left; border-bottom: 1px solid var(--border); color: var(--text-muted);">Parameter</th>
                        <th style="padding: 1rem; text-align: left; border-bottom: 1px solid var(--border); color: #86efac;">🌱 Vegetative Target (Leaf Growth)</th>
                        <th style="padding: 1rem; text-align: left; border-bottom: 1px solid var(--border); color: #fca5a5;">🍅 Generative Target (Fruit Growth)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: bold; color: var(--primary);">Temperature DIF</td>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['vegetative_triggers'].get('temperature_dif', '')}</td>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['generative_triggers'].get('temperature_dif', '')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: bold; color: var(--primary);">VPD (kPa)</td>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['vegetative_triggers'].get('vpd_target', '')}</td>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['generative_triggers'].get('vpd_target', '')}</td>
                    </tr>
                    <tr>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: bold; color: var(--primary);">Irrigation Strategy</td>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['vegetative_triggers'].get('irrigation', '')}</td>
                        <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['generative_triggers'].get('irrigation', '')}</td>
                    </tr>
                </tbody>
            </table>
        """

    # Section 4: Fertigation & CTA
    if 'fertigation' in data:
        fg = data['fertigation']
        content_html += f"""
            <h2 style="color: white; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;" id="fertigation">Fertigation Strategy</h2>
            <p style="color: #cbd5e1; margin-bottom: 1.5rem;">{fg.get('intro', '')}</p>
            
            <div style="background: rgba(255,255,255,0.03); border-left: 4px solid var(--primary); padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0;">
                <h4 style="margin-top: 0; color: #86efac;">Phase 1: Vegetative</h4>
                <p style="margin-bottom: 0; color: #f8fafc;">{fg.get('vegetative_phase', '')}</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.03); border-left: 4px solid #fca5a5; padding: 1.5rem; margin-bottom: 3rem; border-radius: 0 8px 8px 0;">
                <h4 style="margin-top: 0; color: #fca5a5;">Phase 2: Generative (Fruiting)</h4>
                <p style="margin-bottom: 0; color: #f8fafc;">{fg.get('generative_phase', '')}</p>
            </div>
        """

    content_html += f"""
        <div id="calculators" style="background: linear-gradient(135deg, rgba(16,185,129,0.1) 0%, rgba(56,189,248,0.1) 100%); border: 1px solid rgba(16,185,129,0.3); padding: 2.5rem; border-radius: 12px; text-align: center; margin-bottom: 2rem;">
            <h2 style="margin-top: 0; color: white; font-size: 1.8rem;">Ready to steer your crop?</h2>
            <p style="color: #cbd5e1; font-size: 1.1rem; margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                AgriAtlas provides the theory, but every greenhouse is unique. Use our precise engineering calculators to hit these target VPD and Temperature DIF values based on your specific facility's U-Value and heating capacity.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="https://smartfarm.inwoovation.com/vpd.html" target="_blank" style="display: inline-block; background: var(--primary); color: #0f172a; font-weight: bold; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-size: 1.1rem; transition: transform 0.2s;">Run VPD Calculator</a>
                <a href="https://smartfarm.inwoovation.com/heat_loss.html" target="_blank" style="display: inline-block; background: transparent; border: 2px solid var(--accent-green); color: var(--accent-green); font-weight: bold; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-size: 1.1rem; transition: transform 0.2s;">Calculate Heat Loss</a>
            </div>
        </div>
    """
        
    output = template.replace("{{TITLE}}", f"{data['title']} | AgriAtlas")
    output = output.replace("{{DESC}}", data.get('description', ''))
    output = output.replace("{{OG_IMAGE}}", data.get('image_url', ''))
    output = output.replace("{{CONTENT}}", content_html)
    output = output.replace("{{CROP_NAVIGATION}}", nav_html)
    
    with open(os.path.join(OUT_DIR, f"{data['id']}.html"), "w", encoding="utf-8") as f:
        f.write(output)

def build_index_page(template, crops, nav_html):
    # Generates the homepage (index.html)
    content_html = f"""
        <div class="breadcrumb">
            <span style="color: var(--text-muted);">AgriAtlas Home</span>
        </div>
        
        <h1 id="overview">Welcome to AgriAtlas</h1>
        <p style="font-size: 1.15rem; color: #cbd5e1; margin-bottom: 3rem; line-height: 1.6;">
            The world's most advanced, data-driven engineering repository for Controlled Environment Agriculture (CEA).
            Select a crop from the navigation menu to explore deep-dive engineering strategies, or browse the grid below.
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1.5rem;">
    """
    
    crops_sorted = sorted(crops, key=lambda x: x['title'])
    for crop in crops_sorted:
        content_html += f"""
            <a href="{crop['id']}.html" style="text-decoration: none; color: inherit; background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; transition: transform 0.2s, border-color 0.2s;">
                <div style="height: 150px; background: #000; overflow: hidden;">
                    <img src="{crop.get('image_url', '')}" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.8;">
                </div>
                <div style="padding: 1.5rem;">
                    <h3 style="margin: 0 0 0.5rem 0; color: var(--primary);">{crop['title']}</h3>
                    <p style="margin: 0; color: var(--text-muted); font-size: 0.9rem;">{crop.get('description', '')[:100]}...</p>
                </div>
            </a>
        """
        
    content_html += "</div>"
    
    output = template.replace("{{TITLE}}", "Home | AgriAtlas")
    output = output.replace("{{DESC}}", "Global Database for CEA Engineering")
    output = output.replace("{{OG_IMAGE}}", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Greenhouse_tomato.jpg/800px-Greenhouse_tomato.jpg")
    output = output.replace("{{CONTENT}}", content_html)
    output = output.replace("{{CROP_NAVIGATION}}", nav_html)
    
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(output)

def generate_search_index(crops):
    search_data = []
    for crop in crops:
        search_data.append({
            "title": crop['title'],
            "url": f"{crop['id']}.html",
            "desc": crop.get('description', '')
        })
    with open(os.path.join(OUT_DIR, "search_index.json"), "w", encoding="utf-8") as f:
        json.dump(search_data, f, ensure_ascii=False)

def main():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
        
    # Read all crop JSONs
    crop_files = glob.glob(os.path.join(CROPS_DIR, "*.json"))
    crops_data = []
    
    for cf in crop_files:
        with open(cf, "r", encoding="utf-8") as f:
            crops_data.append(json.load(f))
            
    # Build each crop page
    for data in crops_data:
        nav_html = generate_navigation(crops_data, active_id=data['id'])
        build_crop_page(template, data, nav_html)
        print(f"Built: {data['id']}.html")
        
    # Build index page
    nav_html_index = generate_navigation(crops_data, active_id=None)
    build_index_page(template, crops_data, nav_html_index)
    print("Built: index.html (Homepage)")
    
    # Generate search index
    generate_search_index(crops_data)
    print("Generated: search_index.json")
    
if __name__ == "__main__":
    main()
