"""Visualization functions for planetary boundary assessments."""

import matplotlib.pyplot as plt


def plot_exploitation_of_SOS(exploitation_of_SOS):
    """
    Plots a bar chart of the exploitation of the Safe Operating Space.
    
    Creates a bar chart showing the SOS exploitation for each planetary boundary 
    category.

    Args:
        exploitation_of_SOS (dict): Dictionary of SOS exploitation values with 
                                   LCIA method keys as keys.
                                   
    Returns:
        None: Displays the plot.
    """
    # Extract labels (categories) and values (normalized impacts)
    labels = [key[0][1] for key in exploitation_of_SOS.keys()]
    values = list(exploitation_of_SOS.values())

    # Create bar plot
    plt.figure(figsize=(12, 6))
    plt.bar(labels, values)
    plt.xlabel('Earth-system process')
    plt.ylabel('Exploitation of Safe Operating Space')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    return None
