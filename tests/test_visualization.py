"""Tests for visualization module."""

import pytest


def test_visualization_import():
    """Test that visualization module can be imported."""
    from pb_aesa import visualization
    assert visualization is not None


def test_plot_exploitation_of_SOS_exists():
    """Test that plot_exploitation_of_SOS function exists."""
    from pb_aesa.visualization import plot_exploitation_of_SOS
    assert callable(plot_exploitation_of_SOS)


def test_plot_exploitation_of_SOS_returns_none():
    """Test that plot_exploitation_of_SOS returns None."""
    from pb_aesa.visualization import plot_exploitation_of_SOS
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for testing
    
    # Create mock exploitation data
    mock_data = {
        (('Planetary Boundaries', 'Climate Change'),): 0.5,
        (('Planetary Boundaries', 'Ocean Acidification'),): 0.3,
    }
    
    result = plot_exploitation_of_SOS(mock_data)
    assert result is None


def test_plot_exploitation_of_SOS_with_empty_data():
    """Test plotting with empty data."""
    from pb_aesa.visualization import plot_exploitation_of_SOS
    import matplotlib
    matplotlib.use('Agg')
    
    # Should not raise an error with empty data
    result = plot_exploitation_of_SOS({})
    assert result is None
