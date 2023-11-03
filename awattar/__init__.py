# -*- coding: utf-8 -*-
"""Initialize the aWATTar package."""

from .client import AwattarClient
from .marketitem import MarketItem
from .cli import cli as _cli    # for CLI entry only

__all__ = [
    'AwattarClient'
]

__version__ = '0.2.2'
