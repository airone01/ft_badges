#!/usr/bin/env python3
import argparse
import sys
from src.config import APP_CONFIG, load_config
from src.types import BatchMatrices, BadgeMeta
from src.renderer import render_svg
from src.markdown import generate_markdown


def run_batch() -> list[BadgeMeta]:
    """Generates the locked matrix of images and returns their metadata."""
    matrices: BatchMatrices = APP_CONFIG["batch_matrices"]
    generated_badges: list[BadgeMeta] = []

    for project in matrices["projects"]:
        for shape in matrices["shapes"]:
            for score in matrices["scores"]:
                for logo in matrices["logo_styles"]:
                    for theme in matrices["themes"]:
                        for variant in matrices["variants"]:
                            badge_meta = render_svg(
                                project, shape, score, logo, theme, variant
                            )
                            generated_badges.append(badge_meta)

    return generated_badges


def validate_single_args(args: argparse.Namespace) -> None:
    """Ensures all standard flags are present when not running in batch mode."""
    required = ["project", "shape", "score", "logo", "theme", "variant"]
    missing = [req for req in required if not getattr(args, req)]
    if missing:
        print(
            f"Error: The following arguments are required when not using --batch: {', '.join(missing)}"
        )
        sys.exit(1)


def setup_cli() -> None:
    parser = argparse.ArgumentParser(description="ft_badges generator CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)
    gen_parser = subparsers.add_parser("gen", help="Generate badges or markdown")

    gen_subparsers = gen_parser.add_subparsers(dest="subcommand", required=True)

    for cmd_name in ["badge", "docs"]:
        cmd_parser = gen_subparsers.add_parser(cmd_name)
        _ = cmd_parser.add_argument(
            "--batch", action="store_true", help="Run batch generation from config"
        )
        _ = cmd_parser.add_argument(
            "--config", default="config.json", help="Path to custom config file"
        )

        _ = cmd_parser.add_argument("--project", help="Project name (e.g., 'libft')")
        _ = cmd_parser.add_argument(
            "--shape", choices=["square", "round", "pentagon"], help="Badge shape"
        )
        _ = cmd_parser.add_argument("--score", help="Score value (e.g., '125')")
        _ = cmd_parser.add_argument(
            "--logo", choices=["text", "logo"], help="Logo style"
        )
        _ = cmd_parser.add_argument(
            "--theme", choices=["dark", "light"], help="Color theme"
        )
        _ = cmd_parser.add_argument(
            "--variant", choices=["classic", "noisy"], help="Background variant"
        )
        _ = cmd_parser.add_argument(
            "--color", help="Force a specific HEX accent color (e.g., '#ff00ff')"
        )

    args = parser.parse_args()

    if args.config != "config.json":
        APP_CONFIG.update(load_config(args.config))

    if args.subcommand == "badge":
        if args.batch:
            run_batch()
        else:
            validate_single_args(args)
            render_svg(
                args.project,
                args.score,
                args.logo,
                args.theme,
                args.variant,
                args.color,
            )

    elif args.subcommand == "docs":
        if args.batch:
            badges = run_batch()
            generate_markdown(badges)
        else:
            validate_single_args(args)
            clean_name = args.project.replace(" ", "_").lower()
            filename = f"{clean_name}--{args.shape}--{args.score}--{args.logo}--{args.theme}--{args.variant}.svg"
            img_url = f"{APP_CONFIG['img_origin_url']}/{filename}"
            print(f"![{args.project} Badge]({img_url})")


if __name__ == "__main__":
    setup_cli()
