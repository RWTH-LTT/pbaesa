"""Test that the package imports correctly."""

import pytest


def test_package_import():
    """Test that the main package can be imported."""
    import pbaesa
    assert pbaesa is not None


def test_version_exists():
    """Test that the package has a version attribute."""
    import pbaesa
    assert hasattr(pbaesa, "__version__")
    assert isinstance(pbaesa.__version__, str)


def test_main_functions_available():
    """Test that main user-facing functions are available."""
    import pbaesa
    
    # Check that the main API functions are available
    assert hasattr(pbaesa, "create_pbaesa_methods")
    assert hasattr(pbaesa, "get_all_allocation_factor")
    assert callable(pbaesa.create_pbaesa_methods)
    assert callable(pbaesa.get_all_allocation_factor)


def test_methods_module_import():
    """Test that the methods module can be imported."""
    from pbaesa import lcia
    assert lcia is not None


def test_allocation_module_import():
    """Test that the allocation module can be imported."""
    from pbaesa import allocation
    assert allocation is not None
