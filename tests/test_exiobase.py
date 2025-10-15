"""Tests for exiobase module."""

import pytest


def test_exiobase_import():
    """Test that exiobase module can be imported."""
    from pb_aesa import exiobase
    assert exiobase is not None


def test_exiobase_functions_exist():
    """Test that all exiobase functions exist."""
    from pb_aesa import exiobase
    
    assert hasattr(exiobase, 'download_exiobase_data')
    assert hasattr(exiobase, 'load_matrices')
    assert hasattr(exiobase, 'calculate_FR_matrix')
    assert hasattr(exiobase, 'calculate_direct_FCE_allocation_factors')
    
    # Check they are callable
    assert callable(exiobase.download_exiobase_data)
    assert callable(exiobase.load_matrices)
    assert callable(exiobase.calculate_FR_matrix)
    assert callable(exiobase.calculate_direct_FCE_allocation_factors)
