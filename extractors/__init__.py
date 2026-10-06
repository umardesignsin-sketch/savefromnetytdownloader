"""Platform detection and extraction services for public media URLs."""

from .detect import DetectError, detect_url
from .service import AnalysisError, analyze

__all__ = ["DetectError", "detect_url", "AnalysisError", "analyze"]
