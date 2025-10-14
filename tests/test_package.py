"""Tests for package-level imports."""

import pytest


def test_package_import():
    """Test that pb_aesa package can be imported."""
    import pb_aesa
    assert pb_aesa is not None


def test_version_exists():
    """Test that version is defined."""
    import pb_aesa
    assert hasattr(pb_aesa, '__version__')
    assert isinstance(pb_aesa.__version__, str)


def test_main_functions_accessible():
    """Test that main functions are accessible from package level."""
    import pb_aesa
    
    # Analysis functions
    assert hasattr(pb_aesa, 'calculate_exploitation_of_SOS')
    
    # Visualization functions
    assert hasattr(pb_aesa, 'plot_exploitation_of_SOS')
    
    # Method functions
    assert hasattr(pb_aesa, 'create_normal_methods')
    assert hasattr(pb_aesa, 'create_n_cycle_method')
    assert hasattr(pb_aesa, 'implement_lcia_methods')
    
    # Nitrogen functions
    assert hasattr(pb_aesa, 'create_n_supply_flow')
    assert hasattr(pb_aesa, 'add_n_supply_flow')
    
    # Constants
    assert hasattr(pb_aesa, 'SAFE_OPERATING_SPACE')
    assert hasattr(pb_aesa, 'PLANETARY_BOUNDARY_UNITS')
    assert hasattr(pb_aesa, 'STANDARD_CATEGORIES')
    assert hasattr(pb_aesa, 'EXIOBASE_GEO_SCOPES')


def test_all_exports():
    """Test that __all__ is properly defined."""
    import pb_aesa
    
    assert hasattr(pb_aesa, '__all__')
    assert isinstance(pb_aesa.__all__, tuple)
    assert len(pb_aesa.__all__) > 0
    
    # Check that all exported names are accessible
    for name in pb_aesa.__all__:
        assert hasattr(pb_aesa, name)
