import os
import hashlib
import colorsys
from jinja2 import Environment, FileSystemLoader
from scour.scour import scourString, parse_args
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


def format_project_name(name: str, shape: str = "rect") -> dict:
    """Calculates text wrapping and dynamic font sizing for the project name."""
    words = name.split()
    if len(words) <= 1:
        length = len(name)
        # scale down if longer than 10 chars
        # min font size 12
        font_size = 26 if length <= 10 else max(12, int(260 / length))

        if shape == "pentagon" and length > 8:
            font_size = max(10, int(font_size * 0.85))

        return {
            "is_multiline": False,
            "line1": name,
            "line2": "",
            "font_size": font_size,
        }
    else:
        # split into two lines at middle-most space
        mid = (len(words) + 1) // 2
        font_size = 20

        if shape == "pentagon":
            font_size = 16

        return {
            "is_multiline": True,
            "line1": " ".join(words[:mid]),
            "line2": " ".join(words[mid:]),
            "font_size": font_size,
        }


def render_svg(
    project: str,
    shape: str,
    score: int | str,
    logo_style: str,
    theme: str,
    variant: str,
    custom_color: str | None = None,
) -> BadgeMeta:
    """Renders a single SVG, optimizes it with Scour, and returns its metadata."""
    template = env.get_template("src/templates/badge.svg")

    theme_colors: ThemeColors = APP_CONFIG["theme_data"].get(
        theme,
        APP_CONFIG["theme_data"].get(
            "dark", {"bg_color": "#121418", "text_color": "#ffffff"}
        ),
    )

    defaults: ProjectData = APP_CONFIG.get(
        "default_project_data", {"color": "#00babc", "threshold": 50}
    )

    accent: str
    if custom_color:
        accent = custom_color
    else:
        project_data: ProjectData = APP_CONFIG["batch_matrices"]["projects"].get(
            project, {}
        )
        threshold: int = project_data.get("threshold", defaults.get("threshold", 50))
        resolved_color: str = project_data.get(
            "color", defaults.get("color", "#00babc")
        )
        accent = "#E74C3C" if int(score) < threshold else resolved_color

    clean_name: str = project.replace(" ", "_").lower()
    filename: str = (
        f"{clean_name}--{shape}--{score}--{logo_style}--{theme}--{variant}.svg"
    )
    grad1, grad2, grad3 = generate_project_gradient(project)
    name_data = format_project_name(project, shape)

    raw_svg: str = template.render(
        project_name=project,
        name_data=name_data,
        shape=shape,
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

    scour_options = parse_args(
        [
            "--enable-comment-stripping",
            "--shorten-ids",
            "--enable-id-stripping",
            "--indent=none",
            "--strip-xml-prolog",
            "--strip-xml-space",
            "--no-line-breaks",
            "--enable-viewboxing",
            "--remove-descriptive-elements",
            "--create-groups",
        ]
    )

    optimized_svg: str = scourString(raw_svg, options=scour_options)

    with open(os.path.join(OUTPUT_DIR, filename), "w") as f:
        _ = f.write(optimized_svg)

    return {
        "filename": filename,
        "project_name": project,
        "shape": shape,
        "score": score,
        "theme": theme,
        "logo_style": logo_style,
        "variant": variant,
    }
