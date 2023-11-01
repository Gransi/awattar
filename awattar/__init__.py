# -*- coding: utf-8 -*-
"""Initialize the aWATTar package."""

from .client import AwattarClient, AsyncAwattarClient
from .marketitem import MarketItem
from .cli import cli as _cli    # for CLI entry only

__all__ = [
    'AwattarClient',
    'AsyncAwattarClient'
]

__version__ = '0.2.2'
