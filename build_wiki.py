import json
import os

TEMPLATE_PATH = "_wiki_template.html"
DATA_PATH = "data/wiki_data.json"
OUT_FILE = "index.html"

def build_wiki():
    if not os.path.exists(DATA_PATH):
        print("No wiki data found.")
        return
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()
        
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    content_html = f"""
        <div class="breadcrumb">
            <a href="#" style="color: var(--primary); text-decoration: none;">AgriAtlas</a> 
            <span>/</span> <a href="#" style="color: var(--primary); text-decoration: none;">Crops</a> 
            <span>/</span> <span style="color: var(--text-muted);">{data['title']}</span>
        </div>
        
        <h1 id="overview">{data['title']}</h1>
    """
    
    if "image_url" in data:
        content_html += f"""
        <figure style="margin: 0 0 2rem 0; width: 100%;">
            <img src="{data['image_url']}" alt="{data['image_caption']}" style="width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; border: 1px solid var(--border);">
            <figcaption style="text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-top: 0.5rem;">{data['image_caption']}</figcaption>
        </figure>
        """
        
    content_html += f"""
        <div class="metadata">
            <span>📚 Crop Family: Solanaceae</span>
            <span>⏱️ Last Updated: 2026-07-15</span>
            <span>✍️ Contributors: AgriAtlas Automation</span>
        </div>
        
        <p style="font-size: 1.15rem; color: #cbd5e1; margin-bottom: 3rem; line-height: 1.6;">
            {data['overview']}
        </p>
    """

    # Section 2: Global Climate Strategy
    content_html += f"""
        <h2 style="color: white; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;" id="climate-strategy">Global Climate Strategy</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 3rem;">
    """
    for strat in data['climate_strategy']:
        content_html += f"""
            <div class="content-box" style="margin-bottom: 0;">
                <h3 style="margin-top: 0; color: var(--primary); font-size: 1.2rem;">🌍 {strat['region']}</h3>
                <p style="color: #f8fafc; font-size: 0.95rem; line-height: 1.5;">{strat['strategy']}</p>
                <span style="font-size: 0.85rem; color: var(--text-muted); background: rgba(0,0,0,0.3); padding: 0.3rem 0.6rem; border-radius: 6px; display: inline-block; margin-top: 1rem;">⚙️ Tech: {strat['tech_level']}</span>
            </div>
        """
    content_html += "</div>"

    # Section 3: Crop Steering
    cs = data['crop_steering']
    content_html += f"""
        <h2 style="color: white; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;" id="crop-steering">Crop Steering Parameters</h2>
        <p style="color: #cbd5e1; margin-bottom: 2rem;">{cs['intro']}</p>
        
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
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['vegetative_triggers']['temperature_dif']}</td>
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['generative_triggers']['temperature_dif']}</td>
                </tr>
                <tr>
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: bold; color: var(--primary);">VPD (kPa)</td>
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['vegetative_triggers']['vpd_target']}</td>
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['generative_triggers']['vpd_target']}</td>
                </tr>
                <tr>
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: bold; color: var(--primary);">Irrigation Strategy</td>
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['vegetative_triggers']['irrigation']}</td>
                    <td style="padding: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); color: #f8fafc;">{cs['generative_triggers']['irrigation']}</td>
                </tr>
            </tbody>
        </table>
    """

    # Section 4: Fertigation & CTA
    fg = data['fertigation']
    content_html += f"""
        <h2 style="color: white; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1.5rem;" id="fertigation">Fertigation Strategy</h2>
        <p style="color: #cbd5e1; margin-bottom: 1.5rem;">{fg['intro']}</p>
        
        <div style="background: rgba(255,255,255,0.03); border-left: 4px solid var(--primary); padding: 1.5rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0;">
            <h4 style="margin-top: 0; color: #86efac;">Phase 1: Vegetative</h4>
            <p style="margin-bottom: 0; color: #f8fafc;">{fg['vegetative_phase']}</p>
        </div>
        
        <div style="background: rgba(255,255,255,0.03); border-left: 4px solid #fca5a5; padding: 1.5rem; margin-bottom: 3rem; border-radius: 0 8px 8px 0;">
            <h4 style="margin-top: 0; color: #fca5a5;">Phase 2: Generative (Fruiting)</h4>
            <p style="margin-bottom: 0; color: #f8fafc;">{fg['generative_phase']}</p>
        </div>

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
    output = output.replace("{{DESC}}", data['description'])
    output = output.replace("{{CONTENT}}", content_html)
    
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)
        
    print("AgriAtlas Wiki built successfully: Ultimate Tomato index.html generated.")

if __name__ == "__main__":
    build_wiki()
