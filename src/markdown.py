import os
from collections import defaultdict
from src.types import BadgeMeta
from src.config import APP_CONFIG


def generate_markdown(badges_metadata: list[BadgeMeta]) -> None:
    """Generates grouped and collapsible Markdown files for MkDocs."""
    os.makedirs("markdown_src/projects", exist_ok=True)

    projects_dict: defaultdict[str, list[BadgeMeta]] = defaultdict(list)
    for badge in badges_metadata:
        projects_dict[badge["project_name"]].append(badge)

    for project_name, badges in projects_dict.items():
        clean_name: str = project_name.replace(" ", "_").lower()
        filepath: str = f"markdown_src/projects/{clean_name}.md"

        # group badges by score
        scores_dict: defaultdict[int, list[BadgeMeta]] = defaultdict(list)
        for badge in badges:
            score_val = (
                int(badge["score"]) if str(badge["score"]).isdigit() else badge["score"]
            )
            scores_dict[score_val].append(badge)

        with open(filepath, "w") as f:
            _ = f.write("---\n")
            _ = f.write(f"title: {project_name}\n")
            _ = f.write("---\n\n")
            _ = f.write(f"# {project_name} Badges\n\n")
            _ = f.write(
                "Expand your score below to find the perfect badge style, then copy the snippet.\n\n"
            )

            # desc
            sorted_scores = sorted(
                scores_dict.keys(),
                key=lambda x: int(x) if str(x).isdigit() else 0,
                reverse=True,
            )

            for score in sorted_scores:
                _ = f.write(
                    f'<p style="font-size: 1.6em; font-weight: 500; margin-top: 1.6em; margin-bottom: 0.6em;">Score: {score}</p>\n\n'
                )
                _ = f.write("<details>\n")
                _ = f.write(
                    f"<summary><b>View Badges for Score {score}</b></summary>\n\n"
                )

                score_badges = scores_dict[score]
                score_badges.sort(
                    key=lambda b: (b["theme"], b["variant"], b["logo_style"])
                )

                for badge in score_badges:
                    img_url: str = f"{APP_CONFIG['img_origin_url']}/{badge['filename']}"
                    md_snippet: str = f"![{project_name} Badge]({img_url})"

                    _ = f.write(
                        f"<h4>{badge['theme'].title()} Theme | {badge['variant'].title()} Variant | {badge['logo_style'].title()} Style</h4><br>"
                    )
                    _ = f.write(
                        f'<img src="{img_url}" width="200" alt="{project_name} badge">\n\n'
                    )
                    _ = f.write(f"```markdown\n{md_snippet}\n```\n\n")

                _ = f.write("</details>\n\n")
