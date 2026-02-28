import json
import os
from typing import cast
from src.types import ConfigData

SITE_URL: str = "https://airone01.github.io/ft_badges"
IMG_ORIGIN_URL: str = (
    "https://raw.githubusercontent.com/airone01/ft_badges/refs/heads/main/badges"
)
OUTPUT_DIR: str = "badges"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_config(filepath: str = "config.json") -> ConfigData:
    """Loads and types the configuration JSON."""
    with open(filepath, "r") as f:
        return cast(ConfigData, json.load(f))


# singleton
APP_CONFIG: ConfigData = load_config()
