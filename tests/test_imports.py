"""Test that the package imports correctly."""

import pytest


def test_package_import():
    """Test that the main package can be imported."""
    import pb_aesa
    assert pb_aesa is not None


def test_version_exists():
    """Test that the package has a version attribute."""
    import pb_aesa
    assert hasattr(pb_aesa, "__version__")
    assert isinstance(pb_aesa.__version__, str)


def test_main_functions_available():
    """Test that main user-facing functions are available."""
    import pb_aesa
    
    # Check that the main API functions are available
    assert hasattr(pb_aesa, "create_pbaesa_methods")
    assert hasattr(pb_aesa, "get_all_allocation_factor")
    assert callable(pb_aesa.create_pbaesa_methods)
    assert callable(pb_aesa.get_all_allocation_factor)


def test_methods_module_import():
    """Test that the methods module can be imported."""
    from pb_aesa import methods
    assert methods is not None


def test_allocation_module_import():
    """Test that the allocation module can be imported."""
    from pb_aesa import allocation
    assert allocation is not None
