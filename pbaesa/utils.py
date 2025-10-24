"""
Utility functions to normalize and plot AESA results.
"""

import matplotlib.pyplot as plt

def calculate_exploitation_of_SOS(mlca_scores):
    """
    Calculates the exploitation of the Safe Operating Space (SOS) for each
    planetary boundary category based on LCIA scores.

    Parameters:
        mlca_scores (dict): Dictionary with LCIA method keys as keys and impact scores as values.

    Returns:
        dict: A dictionary with method keys and their normalized SOS exploitation values.
    """
    # Define the Safe Operating Space thresholds for each category (based on PB framework)
    safe_operating_space = {
        "Climate Change": float("1"),
        "Ocean Acidification": float("0.688"),
        "Change in Biosphere Integrity": float("10"),
        "Phosphorus Cycle": float("10"),
        "Nitrogen Cycle": float("62"),
        "Atmospheric Aerosol Loading": float("0.11"),
        "Freshwater Use": float("4000"),
        "Stratospheric Ozone Depletion": float("14.5"),
        "Land-system Change": float("85.1")
    }

    exploitation_of_SOS = {}
    for key, value in mlca_scores.items():
        category = key[0][1]  # Extract planetary boundary category from method key
        divisor = safe_operating_space.get(category)
        if divisor:  # Only compute if the category has a defined threshold
            exploitation_of_SOS[key] = value / divisor
        else:
            exploitation_of_SOS[key] = None  # Assign None if no threshold is defined

    return exploitation_of_SOS


def plot_exploitation_of_SOS(exploitation_of_SOS):
    """
    Plots a bar chart of the exploitation of the Safe Operating Space for each
    planetary boundary category.

    Parameters:
        exploitation_of_SOS (dict): Dictionary of SOS exploitation values.
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

def plot_AESA(exploitation_of_SOS, total_fce, total_gva):
    """
    Plots a bar chart of the exploitation of the Safe Operating Space for each
    planetary boundary category against the system-specific share of Safe Operating Space based on total GVA and FCE.

    Parameters:
        exploitation_of_SOS (dict): Dictionary of SOS exploitation values.
        total_FCE (float): system-specific share of Safe Operating Space based on total FCE.
        total_GVA (float): system-specific share of Safe Operating Space based on total GVA.
    """
    # Sort bars by height (descending)
    sorted_items = sorted(exploitation_of_SOS.items(), key=lambda x: x[1], reverse=True)
    labels = [key[0][1] for key, _ in sorted_items]
    values = [val for _, val in sorted_items]

    # Define RGB colors (normalized to 0–1)
    bar_color = (0/255, 84/255, 159/255)
    fce_color = (204/255, 7/255, 30/255)
    gva_color = (246/255, 168/255, 0/255)


    # Create bar plot
    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color=bar_color)
    plt.xlabel('Earth-system process')
    plt.ylabel('Exploitation of Safe Operating Space')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.axhline(y=total_fce, color=fce_color, linestyle='--',)
    plt.axhline(y=total_gva, color=gva_color, linestyle='--',)

    # Add italic labels at the top right
    plt.text(
        x=len(labels) - 0.3,  # near the right edge
        y=total_fce * 1.02,       # slightly above the red line
        s='Final Consumption Expenditure',    # your text here (in italics)
        color=fce_color,
        fontsize=12,
        ha='right',
        va='bottom',
        style='italic'
    )
    plt.text(
        x=len(labels) - 0.3,
        y=total_gva * 1.02,
        s='Gross Value Added',
        color=gva_color,
        fontsize=12,
        ha='right',
        va='bottom',
        style='italic'
    )

    plt.show()

    return None