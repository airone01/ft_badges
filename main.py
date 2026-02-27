#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
from jinja2 import Environment, FileSystemLoader

with open('config.json', 'r') as f:
    config = json.load(f)

OUTPUT_DIR = "badges"
os.makedirs(OUTPUT_DIR, exist_ok=True)
env = Environment(loader=FileSystemLoader('.'))

def render_svg(project, score, logo_style, theme, custom_color=None):
    """Renders a single SVG and returns its metadata dictionary."""
    template = env.get_template('badge_template.svg')
    
    theme_colors = config["theme_data"].get(theme, config["theme_data"]["dark"])
    if custom_color:
        accent = custom_color
    else:
        project_data = config["batch_matrices"]["projects"].get(project, {"color": "#00babc", "threshold": 50})
        accent = "#E74C3C" if int(score) < project_data.get("threshold", 50) else project_data["color"]

    clean_name = project.replace(' ', '_').lower()
    filename = f"{clean_name}--{score}--{logo_style}--{theme}.svg"
    
    rendered = template.render(
        project_name=project, score=score, logo_style=logo_style,
        bg_color=theme_colors["bg_color"], text_color=theme_colors["text_color"], accent_color=accent
    )

    with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
        f.write(rendered)

    return {
        "filename": filename,
        "project_name": project,
        "score": score,
        "theme": theme,
        "logo_style": logo_style
    }

def run_batch():
    """Generates the locked matrix of images and builds the catalog."""
    matrices = config["batch_matrices"]
    generated_badges = []

    for project in matrices["projects"]:
        for score in matrices["scores"]:
            for logo in matrices["logo_styles"]:
                for theme in matrices["themes"]:
                    # Collect metadata as we generate
                    badge_meta = render_svg(project, score, logo, theme)
                    generated_badges.append(badge_meta)

    try:
        subprocess.run(["pnpm", "exec", "svgo", "-f", OUTPUT_DIR], check=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        print(f"SVGO skipped or failed: {e}")

def setup_cli():
    parser = argparse.ArgumentParser(description="42 Badge Generator CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("batch", help="Generate all standard badges from config.json")

    single_parser = subparsers.add_parser("single", help="Generate a custom badge with arbitrary values")
    single_parser.add_argument("--project", required=True, help="Any project name (e.g., 'My Custom C++')")
    single_parser.add_argument("--score", required=True, help="Any score (e.g., 'OVER 9000')")
    single_parser.add_argument("--logo", choices=["text", "logo"], default="text")
    single_parser.add_argument("--theme", choices=["dark", "light"], default="dark")
    single_parser.add_argument("--color", help="Force a specific HEX accent color (e.g., '#ff00ff')")

    args = parser.parse_args()

    if args.command == "batch":
        run_batch()
    elif args.command == "single":
        filename = render_svg(args.project, args.score, args.logo, args.theme, args.color)

if __name__ == "__main__":
    setup_cli()
