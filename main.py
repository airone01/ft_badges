#!/usr/bin/env python3
import argparse
import subprocess
from src.config import APP_CONFIG, OUTPUT_DIR
from src.types import BatchMatrices, BadgeMeta
from src.renderer import render_svg
from src.markdown import generate_markdown


def run_batch(gen_md: bool) -> None:
    """Generates the locked matrix of images and builds the catalog."""
    matrices: BatchMatrices = APP_CONFIG["batch_matrices"]
    generated_badges: list[BadgeMeta] = []

    for project in matrices["projects"]:
        for score in matrices["scores"]:
            for logo in matrices["logo_styles"]:
                for theme in matrices["themes"]:
                    for variant in matrices["variants"]:
                        badge_meta = render_svg(project, score, logo, theme, variant)
                        generated_badges.append(badge_meta)

    try:
        _ = subprocess.run(
            ["pnpm", "exec", "svgo", "-f", OUTPUT_DIR],
            check=True,
            stdout=subprocess.DEVNULL,
        )
    except Exception as e:
        print(f"SVGO skipped or failed: {e}")

    if gen_md:
        generate_markdown(generated_badges)


def setup_cli() -> None:
    parser = argparse.ArgumentParser(description="ft_badges generator cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    batch_parser = subparsers.add_parser(
        "batch", help="Generate all standard badges from config.json"
    )
    _ = batch_parser.add_argument(
        "--md", action="store_true", help="Generate the initial markdown for MkDocs"
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
