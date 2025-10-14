"""Tests for allocation module."""

import pytest


def test_allocation_import():
    """Test that allocation module can be imported."""
    from pb_aesa import allocation
    assert allocation is not None


def test_allocation_functions_exist():
    """Test that all allocation functions exist."""
    from pb_aesa import allocation
    
    assert hasattr(allocation, 'get_all_allocation_factor')
    assert hasattr(allocation, 'get_direct_FCE_allocation_factor')
    assert hasattr(allocation, 'get_total_FCE_allocation_factor')
    assert hasattr(allocation, 'get_direct_GVA_allocation_factor')
    assert hasattr(allocation, 'get_total_GVA_allocation_factor')
    
    # Check they are callable
    assert callable(allocation.get_all_allocation_factor)
    assert callable(allocation.get_direct_FCE_allocation_factor)
    assert callable(allocation.get_total_FCE_allocation_factor)
    assert callable(allocation.get_direct_GVA_allocation_factor)
    assert callable(allocation.get_total_GVA_allocation_factor)
