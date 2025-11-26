from pathlib import Path
from loguru import logger


ASCII_ART_PATH = Path(__file__).resolve().parents[2] / "art" / "tars_text.txt"


def load_ascii_art() -> str:
    try:
        return ASCII_ART_PATH.read_text(encoding="utf-8")
    except Exception as exc:
        logger.warning("Could not load ASCII art from {}: {}", ASCII_ART_PATH, exc)
        return ""
