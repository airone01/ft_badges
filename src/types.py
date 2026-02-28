from typing import TypedDict


class ThemeColors(TypedDict):
    bg_color: str
    text_color: str


class ProjectData(TypedDict):
    color: str
    threshold: int


class BatchMatrices(TypedDict):
    projects: dict[str, ProjectData]
    scores: list[int]
    logo_styles: list[str]
    themes: list[str]
    variants: list[str]


class ConfigData(TypedDict):
    site_url: str
    img_origin_url: str
    schema: list[str]
    theme_data: dict[str, ThemeColors]
    batch_matrices: BatchMatrices


class BadgeMeta(TypedDict):
    filename: str
    project_name: str
    score: int | str
    theme: str
    logo_style: str
    variant: str
