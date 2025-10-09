"""Analysis functions for planetary boundary assessments."""

from .constants import SAFE_OPERATING_SPACE


def calculate_exploitation_of_SOS(mlca_scores):
    """
    Calculates the exploitation of the Safe Operating Space (SOS).
    
    Calculates the exploitation for each planetary boundary category based on 
    LCIA scores.

    Args:
        mlca_scores (dict): Dictionary with LCIA method keys as keys and impact 
                           scores as values.

    Returns:
        dict: Dictionary with method keys and their corresponding SOS exploitation 
              values. Values are normalized impact scores (impact/threshold).
    """
    exploitation_of_SOS = {}
    
    for key, value in mlca_scores.items():
        # Extract planetary boundary category from method key
        category = key[0][1]
        divisor = SAFE_OPERATING_SPACE.get(category)
        
        if divisor:
            # Compute exploitation if the category has a defined threshold
            exploitation_of_SOS[key] = value / divisor
        else:
            # Assign None if no threshold is defined
            exploitation_of_SOS[key] = None

    return exploitation_of_SOS
