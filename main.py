#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import hashlib
import colorsys
from jinja2 import Environment, FileSystemLoader

with open("config.json", "r") as f:
    config = json.load(f)

OUTPUT_DIR = "badges"
os.makedirs(OUTPUT_DIR, exist_ok=True)
env = Environment(loader=FileSystemLoader("."))


def generate_project_gradient(project_name):
    """Generates 3 vibrant, deterministic hex colors based on the project name."""
    hash_obj = hashlib.md5(project_name.encode("utf-8"))
    hash_int = int(hash_obj.hexdigest(), 16)
    base_hue = hash_int % 360
    # determine how far the hue shifts across the gradient
    # 30 to 90 makes it smooth
    hue_step = 30 + (hash_int % 60)
    direction = 1 if (hash_int % 2 == 0) else -1
    colors = []

    h1 = base_hue / 360.0
    r, g, b = colorsys.hls_to_rgb(h1, 0.30, 0.90)
    colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")

    h2 = ((base_hue + (hue_step * direction)) % 360) / 360.0
    r, g, b = colorsys.hls_to_rgb(h2, 0.50, 0.95)
    colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")

    h3 = ((base_hue + (hue_step * 2 * direction)) % 360) / 360.0
    r, g, b = colorsys.hls_to_rgb(h3, 0.70, 1.00)
    colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")

    return colors


def render_svg(project, score, logo_style, theme, variant, custom_color=None):
    """Renders a single SVG and returns its metadata dictionary."""
    template = env.get_template("badge_template.svg")

    theme_colors = config["theme_data"].get(theme, config["theme_data"]["dark"])
    if custom_color:
        accent = custom_color
    else:
        project_data = config["batch_matrices"]["projects"].get(
            project, {"color": "#00babc", "threshold": 50}
        )
        accent = (
            "#E74C3C"
            if int(score) < project_data.get("threshold", 50)
            else project_data["color"]
        )

    clean_name = project.replace(" ", "_").lower()
    filename = f"{clean_name}--{score}--{logo_style}--{theme}--{variant}.svg"
    grad1, grad2, grad3 = generate_project_gradient(project)

    rendered = template.render(
        project_name=project,
        score=score,
        logo_style=logo_style,
        bg_color=theme_colors["bg_color"],
        text_color=theme_colors["text_color"],
        accent_color=accent,
        variant=variant,
        grad1=grad1,
        grad2=grad2,
        grad3=grad3,
    )

    with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
        f.write(rendered)

    return {
        "filename": filename,
        "project_name": project,
        "score": score,
        "theme": theme,
        "logo_style": logo_style,
    }


def run_batch():
    """Generates the locked matrix of images and builds the catalog."""
    matrices = config["batch_matrices"]
    generated_badges = []

    for project in matrices["projects"]:
        for score in matrices["scores"]:
            for logo in matrices["logo_styles"]:
                for theme in matrices["themes"]:
                    for variant in matrices["variants"]:
                        badge_meta = render_svg(project, score, logo, theme, variant)
                        generated_badges.append(badge_meta)

    try:
        subprocess.run(
            ["pnpm", "exec", "svgo", "-f", OUTPUT_DIR],
            check=True,
            stdout=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"SVGO skipped or failed: {e}")


def setup_cli():
    parser = argparse.ArgumentParser(description="42 Badge Generator CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("batch", help="Generate all standard badges from config.json")

    single_parser = subparsers.add_parser(
        "single", help="Generate a custom badge with arbitrary values"
    )
    single_parser.add_argument(
        "--project", required=True, help="Any project name (e.g., 'My Custom C++')"
    )
    single_parser.add_argument(
        "--score", required=True, help="Any score (e.g., 'OVER 9000')"
    )
    single_parser.add_argument("--logo", choices=["text", "logo"], default="text")
    single_parser.add_argument("--theme", choices=["dark", "light"], default="dark")
    single_parser.add_argument(
        "--color", help="Force a specific HEX accent color (e.g., '#ff00ff')"
    )
    single_parser.add_argument(
        "--variant", choices=["classic", "noisy"], default="double"
    )

    args = parser.parse_args()

    if args.command == "batch":
        run_batch()
    elif args.command == "single":
        filename = render_svg(
            args.project, args.score, args.logo, args.theme, args.color
        )


if __name__ == "__main__":
    setup_cli()
