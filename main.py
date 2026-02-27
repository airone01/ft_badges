#!/usr/bin/env python3
import os
import subprocess
from jinja2 import Environment, FileSystemLoader

PROJECTS = [
    {"name": "libft", "base_color": "#00babc"},
    {"name": "minishell", "base_color": "#00babc", "threshold": 75},
]
SCORES = [0, 50, 100, 125]
THEMES = {
    "dark": {"bg_color": "#121418", "text_color": "#ffffff"},
    "light": {"bg_color": "#f0f6fc", "text_color": "#24292f"}
}
LOGO_STYLES = ["text", "logo"]
FAIL_COLOR = "#E74C3C"
OUTPUT_DIR = "badges"

def setup_env():
    """Ensure output directory exists and setup Jinja environment."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return Environment(loader=FileSystemLoader('.'))

def generate_svgs(env):
    """Generates all SVG permutations and returns a list of metadata for the HTML catalog."""
    svg_template = env.get_template('badge_template.svg')
    generated_badges = []

    print("🎨 Generating SVGs...")
    for project in PROJECTS:
        threshold = project.get("threshold", 50)
        clean_name = project['name'].replace(' ', '_').lower()
        
        for score in SCORES:
            accent = FAIL_COLOR if score < threshold else project["base_color"]
            
            for theme_name, theme_colors in THEMES.items():
                for logo in LOGO_STYLES:
                    filename = f"{clean_name}--{score}--{logo}--{theme_name}.svg"
                    
                    rendered_svg = svg_template.render(
                        project_name=project["name"],
                        score=score,
                        accent_color=accent,
                        bg_color=theme_colors["bg_color"],
                        text_color=theme_colors["text_color"],
                        logo_style=logo
                    )
                    
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    with open(filepath, 'w') as f:
                        f.write(rendered_svg)
                    
                    generated_badges.append({
                        "filename": filename,
                        "project_name": project["name"],
                        "score": score,
                        "theme": theme_name,
                        "logo_style": logo
                    })
    return generated_badges

def optimize_svgs():
    """Runs SVGO via pnpm to minify the generated SVGs."""
    print("⚡ Optimizing SVGs with SVGO...")
    try:
        subprocess.run(["pnpm", "exec", "svgo", "-f", OUTPUT_DIR], check=True)
        print("✅ SVGO Optimization complete.")
    except subprocess.CalledProcessError:
        print("❌ SVGO failed. Is it installed? Run: pnpm add -D svgo")
    except FileNotFoundError:
        print("❌ pnpm not found. Please ensure Node and pnpm are installed.")

def generate_catalog(env, badges):
    """Generates the index.html documentation page."""
    print("📝 Generating HTML Catalog...")
    html_template = env.get_template('catalog_template.html')
    rendered_html = html_template.render(badges=badges)
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
        f.write(rendered_html)
    print("✅ Catalog generated at badges/index.html")

if __name__ == "__main__":
    jinja_env = setup_env()
    badges_metadata = generate_svgs(jinja_env)
    optimize_svgs()
    generate_catalog(jinja_env, badges_metadata)
    print("\n🎉 Build complete! Open badges/index.html in your browser.")
