"""Initialize the aWATTar package."""

from .cli import cli as _cli  # for CLI entry only
from .client import AwattarClient

__all__ = [
    "AwattarClient",
]

__version__ = "0.2.2"
