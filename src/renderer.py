import os
import hashlib
import colorsys
from jinja2 import Environment, FileSystemLoader
from src.types import BadgeMeta, ThemeColors, ProjectData
from src.config import APP_CONFIG, OUTPUT_DIR

env: Environment = Environment(loader=FileSystemLoader("."))


def generate_project_gradient(project_name: str) -> list[str]:
    """Generates 3 vibrant, deterministic hex colors based on the project name."""
    hash_obj = hashlib.md5(project_name.encode("utf-8"))
    hash_int: int = int(hash_obj.hexdigest(), 16)
    base_hue: int = hash_int % 360
    hue_step: int = 30 + (hash_int % 60)
    direction: int = 1 if (hash_int % 2 == 0) else -1
    colors: list[str] = []

    h1: float = base_hue / 360.0
    r1, g1, b1 = colorsys.hls_to_rgb(h1, 0.30, 0.90)
    colors.append(f"#{int(r1*255):02x}{int(g1*255):02x}{int(b1*255):02x}")

    h2: float = ((base_hue + (hue_step * direction)) % 360) / 360.0
    r2, g2, b2 = colorsys.hls_to_rgb(h2, 0.50, 0.95)
    colors.append(f"#{int(r2*255):02x}{int(g2*255):02x}{int(b2*255):02x}")

    h3: float = ((base_hue + (hue_step * 2 * direction)) % 360) / 360.0
    r3, g3, b3 = colorsys.hls_to_rgb(h3, 0.70, 1.00)
    colors.append(f"#{int(r3*255):02x}{int(g3*255):02x}{int(b3*255):02x}")

    return colors


def render_svg(
    project: str,
    score: int | str,
    logo_style: str,
    theme: str,
    variant: str,
    custom_color: str | None = None,
) -> BadgeMeta:
    """Renders a single SVG and returns its metadata dictionary."""
    template = env.get_template("src/badge_template.svg")

    theme_colors: ThemeColors = APP_CONFIG["theme_data"].get(
        theme, APP_CONFIG["theme_data"]["dark"]
    )

    accent: str
    if custom_color:
        accent = custom_color
    else:
        project_data: ProjectData = APP_CONFIG["batch_matrices"]["projects"].get(
            project, {"color": "#00babc", "threshold": 50}
        )
        accent = (
            "#E74C3C"
            if int(score) < project_data.get("threshold", 50)
            else project_data["color"]
        )

    clean_name: str = project.replace(" ", "_").lower()
    filename: str = f"{clean_name}--{score}--{logo_style}--{theme}--{variant}.svg"
    grad1, grad2, grad3 = generate_project_gradient(project)

    rendered: str = template.render(
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
        _ = f.write(rendered)

    return {
        "filename": filename,
        "project_name": project,
        "score": score,
        "theme": theme,
        "logo_style": logo_style,
        "variant": variant,
    }
