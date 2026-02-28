from typing import TypedDict


class ThemeColors(TypedDict):
    bg_color: str
    text_color: str


# total=False means keys are optional
class ProjectData(TypedDict, total=False):
    color: str
    threshold: int


class BatchMatrices(TypedDict):
    projects: dict[str, ProjectData]
    scores: list[int]
    logo_styles: list[str]
    themes: list[str]
    variants: list[str]


class ConfigData(TypedDict):
    project_count: int
    schema: list[str]
    default_project_data: ProjectData
    theme_data: dict[str, ThemeColors]
    batch_matrices: BatchMatrices


class BadgeMeta(TypedDict):
    filename: str
    project_name: str
    score: int | str
    theme: str
    logo_style: str
    variant: str
