import os
from collections import defaultdict
from src.types import BadgeMeta
from src.config import IMG_ORIGIN_URL


def generate_markdown(badges_metadata: list[BadgeMeta]) -> None:
    """Generates base Markdown files for MkDocs to generate the docs with."""
    os.makedirs("markdown_src/projects", exist_ok=True)

    projects_dict: defaultdict[str, list[BadgeMeta]] = defaultdict(list)
    for badge in badges_metadata:
        projects_dict[badge["project_name"]].append(badge)

    for project_name, badges in projects_dict.items():
        clean_name: str = project_name.replace(" ", "_").lower()
        filepath: str = f"markdown_src/projects/{clean_name}.md"

        badges.sort(key=lambda b: int(b["score"]), reverse=True)

        with open(filepath, "w") as f:
            _ = f.write("---\n")
            _ = f.write(f"title: {project_name}\n")
            _ = f.write("---\n\n")
            _ = f.write(
                "Copy the markdown snippet below your favorite badge to use it in your README.\n\n"
            )

            for badge in badges:
                img_url: str = f"{IMG_ORIGIN_URL}/{badge['filename']}"
                md_snippet: str = f"![{project_name} Badge]({img_url})"

                _ = f.write(
                    f"### Score: {badge['score']} | {badge['theme'].title()} | {badge['variant'].title()}\n\n"
                )
                _ = f.write(
                    f'<img src="{img_url}" width="200" alt="{project_name} badge">\n\n'
                )
                _ = f.write(f"```markdown\n{md_snippet}\n```\n\n")
                _ = f.write("---\n\n")
