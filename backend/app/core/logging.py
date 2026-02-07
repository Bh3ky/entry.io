"""Logging helpers for consistent application logs."""

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure basic structured logging style for the application."""

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
