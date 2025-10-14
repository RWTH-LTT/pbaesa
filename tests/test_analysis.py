"""Tests for analysis module."""

import pytest


def test_analysis_import():
    """Test that analysis module can be imported."""
    from pb_aesa import analysis
    assert analysis is not None


def test_calculate_exploitation_of_SOS_basic():
    """Test basic functionality of calculate_exploitation_of_SOS."""
    from pb_aesa.analysis import calculate_exploitation_of_SOS
    from pb_aesa.constants import SAFE_OPERATING_SPACE
    
    # Create mock MLCA scores
    mock_scores = {
        (('Planetary Boundaries', 'Climate Change'),): 0.3,
        (('Planetary Boundaries', 'Ocean Acidification'),): 0.1,
        (('Planetary Boundaries', 'Freshwater Use'),): 2000.0,
    }
    
    # Calculate exploitation
    result = calculate_exploitation_of_SOS(mock_scores)
    
    # Check result structure
    assert isinstance(result, dict)
    assert len(result) == 3
    
    # Check calculation correctness
    for key, value in result.items():
        category = key[0][1]
        expected = mock_scores[key] / SAFE_OPERATING_SPACE[category]
        assert abs(value - expected) < 1e-6


def test_calculate_exploitation_of_SOS_with_missing_threshold():
    """Test handling of categories without defined thresholds."""
    from pb_aesa.analysis import calculate_exploitation_of_SOS
    
    # Create mock scores with a category that doesn't have a threshold
    mock_scores = {
        (('Planetary Boundaries', 'Climate Change'),): 0.3,
        (('Planetary Boundaries', 'Unknown Category'),): 100.0,
    }
    
    result = calculate_exploitation_of_SOS(mock_scores)
    
    # Check that unknown category returns None
    assert result[(('Planetary Boundaries', 'Climate Change'),)] is not None
    assert result[(('Planetary Boundaries', 'Unknown Category'),)] is None


def test_calculate_exploitation_of_SOS_empty():
    """Test with empty input."""
    from pb_aesa.analysis import calculate_exploitation_of_SOS
    
    result = calculate_exploitation_of_SOS({})
    
    assert isinstance(result, dict)
    assert len(result) == 0


def test_calculate_exploitation_of_SOS_all_categories():
    """Test with all planetary boundary categories."""
    from pb_aesa.analysis import calculate_exploitation_of_SOS
    from pb_aesa.constants import SAFE_OPERATING_SPACE
    
    # Create mock scores for all categories
    mock_scores = {}
    for category in SAFE_OPERATING_SPACE.keys():
        mock_scores[(('Planetary Boundaries', category),)] = 1.0
    
    result = calculate_exploitation_of_SOS(mock_scores)
    
    # All should have values
    for key, value in result.items():
        assert value is not None
        assert value > 0
