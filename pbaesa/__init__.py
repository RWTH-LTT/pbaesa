"""
pbaesa: Planetary-boundary-based absolute environmental sustainability assessment

This package provides tools for implementing and using planetary boundary-based
LCIA methods in Brightway LCA framework.
"""

__version__ = "0.1.0"

from .methods import create_pbaesa_methods
from .allocation import get_all_allocation_factor

__all__ = [
    "create_pbaesa_methods",
    "get_all_allocation_factor",
]
