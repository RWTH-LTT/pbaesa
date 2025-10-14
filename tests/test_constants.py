"""Tests for constants module."""

import pytest


def test_constants_import():
    """Test that constants can be imported."""
    from pb_aesa import constants
    assert constants is not None


def test_safe_operating_space():
    """Test that Safe Operating Space thresholds are defined."""
    from pb_aesa.constants import SAFE_OPERATING_SPACE
    
    assert isinstance(SAFE_OPERATING_SPACE, dict)
    assert len(SAFE_OPERATING_SPACE) > 0
    
    # Check expected categories
    expected_categories = [
        "Climate Change",
        "Ocean Acidification",
        "Change in Biosphere Integrity",
        "Phosphorus Cycle",
        "Nitrogen Cycle",
        "Atmospheric Aerosol Loading",
        "Freshwater Use",
        "Stratospheric Ozone Depletion",
        "Land-system Change"
    ]
    
    for category in expected_categories:
        assert category in SAFE_OPERATING_SPACE
        assert isinstance(SAFE_OPERATING_SPACE[category], float)
        assert SAFE_OPERATING_SPACE[category] > 0


def test_planetary_boundary_units():
    """Test that planetary boundary units are defined."""
    from pb_aesa.constants import PLANETARY_BOUNDARY_UNITS
    
    assert isinstance(PLANETARY_BOUNDARY_UNITS, dict)
    assert len(PLANETARY_BOUNDARY_UNITS) > 0
    
    # Each unit should be a string
    for unit in PLANETARY_BOUNDARY_UNITS.values():
        assert isinstance(unit, str)
        assert len(unit) > 0


def test_standard_categories():
    """Test that standard categories list is defined."""
    from pb_aesa.constants import STANDARD_CATEGORIES
    
    assert isinstance(STANDARD_CATEGORIES, list)
    assert len(STANDARD_CATEGORIES) == 8  # Should have 8 standard categories
    
    # Check expected categories (excluding Nitrogen Cycle)
    expected = [
        "Climate Change",
        "Ocean Acidification",
        "Change in Biosphere Integrity",
        "Phosphorus Cycle",
        "Atmospheric Aerosol Loading",
        "Freshwater Use",
        "Stratospheric Ozone Depletion",
        "Land-system Change"
    ]
    
    for category in expected:
        assert category in STANDARD_CATEGORIES


def test_exiobase_geo_scopes():
    """Test that EXIOBASE geographical scopes are defined."""
    from pb_aesa.constants import EXIOBASE_GEO_SCOPES
    
    assert isinstance(EXIOBASE_GEO_SCOPES, list)
    assert len(EXIOBASE_GEO_SCOPES) == 49  # Should have 49 regions
    
    # Check some expected country codes
    expected_codes = ['DE', 'US', 'CN', 'FR', 'GB']
    for code in expected_codes:
        assert code in EXIOBASE_GEO_SCOPES
