#!/usr/bin/env python3
import argparse
from collections import defaultdict
import json
import os
import subprocess
import hashlib
import colorsys
from jinja2 import Environment, FileSystemLoader

SITE_URL = "https://airone01.github.io/ft_badges"
IMG_ORIGIN_URL = (
    "https://raw.githubusercontent.com/airone01/ft_badges/refs/heads/main/badges"
)

with open("config.json", "r") as f:
    config = json.load(f)

OUTPUT_DIR = "badges"
os.makedirs(OUTPUT_DIR, exist_ok=True)
env = Environment(loader=FileSystemLoader("."))


def generate_markdown(badges_metadata):
    """Generates MkDocs-compatible Markdown files with frontmatter."""
    os.makedirs("markdown_src/projects", exist_ok=True)

    projects_dict = defaultdict(list)
    for badge in badges_metadata:
        projects_dict[badge["project_name"]].append(badge)

    for project_name, badges in projects_dict.items():
        clean_name = project_name.replace(" ", "_").lower()
        filepath = f"markdown_src/projects/{clean_name}.md"

        with open(filepath, "w") as f:
            f.write("---\n")
            f.write(f"title: {project_name}\n")
            f.write("---\n\n")

            f.write(
                "Copy the markdown snippet below your favorite badge to use it in your README.\n\n"
            )

            for badge in badges:
                img_url = f"{IMG_ORIGIN_URL}/{badge['filename']}"
                md_snippet = f"![{project_name} Badge]({img_url})"

                f.write(
                    f"### Score: {badge['score']} | {badge['theme'].title()} | {badge['variant'].title()}\n\n"
                )
                f.write(
                    f'<img src="{img_url}" width="200" alt="{project_name} badge">\n\n'
                )
                f.write(f"```markdown\n{md_snippet}\n```\n\n")
                f.write("---\n\n")


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


def render_svg(
    project: str,
    score: int,
    logo_style: str,
    theme: str,
    variant: str,
    custom_color: str | None = None,
):
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
        "variant": variant,
    }


def run_batch(gen_md: bool):
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

    if gen_md:
        generate_markdown(generated_badges)


def setup_cli():
    parser = argparse.ArgumentParser(description="ft_badges generator cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    batch_parser = subparsers.add_parser(
        "batch", help="Generate all standard badges from config.json"
    )
    _ = batch_parser.add_argument(
        "--md", help="Generate the initial markdown for MkDocs"
    )

    single_parser = subparsers.add_parser(
        "single", help="Generate a custom badge with arbitrary values"
    )
    _ = single_parser.add_argument(
        "--project", required=True, help="Any project name (e.g., 'My Custom C++')"
    )
    _ = single_parser.add_argument(
        "--score", required=True, help="Any score (e.g., '112')"
    )
    _ = single_parser.add_argument("--logo", choices=["text", "logo"], default="text")
    _ = single_parser.add_argument("--theme", choices=["dark", "light"], default="dark")
    _ = single_parser.add_argument(
        "--color", help="Force a specific HEX accent color (e.g., '#ff00ff')"
    )
    _ = single_parser.add_argument(
        "--variant", choices=["classic", "noisy"], default="double"
    )

    args = parser.parse_args()

    if args.command == "batch":
        run_batch(args.md)
    elif args.command == "single":
        _ = render_svg(
            args.project,
            args.score,
            args.logo,
            args.theme,
            args.variant,
            args.color,
        )


if __name__ == "__main__":
    setup_cli()
