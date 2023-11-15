"""Initialize the aWATTar package."""

from .cli import cli as _cli  # for CLI entry only  # noqa: F401
from .client import AwattarClient

__all__ = [
    "AwattarClient",
]
