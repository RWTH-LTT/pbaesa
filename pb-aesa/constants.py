"""Constants for planetary boundaries."""

# Safe Operating Space thresholds for planetary boundaries
# Values represent the safe operating space for each category
SAFE_OPERATING_SPACE = {
    "Climate Change": float("0.6"),
    "Ocean Acidification": float("0.2"),
    "Change in Biosphere Integrity": float("10"),
    "Phosphorus Cycle": float("10"),
    "Nitrogen Cycle": float("62"),
    "Atmospheric Aerosol Loading": float("0.11"),
    "Freshwater Use": float("4000"),
    "Stratospheric Ozone Depletion": float("14.5"),
    "Land-system Change": float("85.1")
}

# Units for planetary boundary categories
PLANETARY_BOUNDARY_UNITS = {
    "Climate Change": "Energy imbalance at top-of-atmosphere [W/m²]",
    "Ocean Acidification": "Aragonite saturation state [Ωₐᵣₐ]",
    "Change in Biosphere Integrity": "Biodiversity Intactness Index [%]",
    "Phosphorus Cycle": "P-flow from freshwater systems into the ocean [Tg P/year]",
    "Atmospheric Aerosol Loading": "Aerosol optical depth (AOD) [-]",
    "Freshwater Use": "Consumptive bluewater use [km³/year]",
    "Stratospheric Ozone Depletion": "Stratospheric ozone concentration [DU]",
    "Land-system Change": "Land available for anthropogenic occupation [millon km²]"
}

# Standard planetary boundary categories
STANDARD_CATEGORIES = [
    "Climate Change",
    "Ocean Acidification",
    "Change in Biosphere Integrity",
    "Phosphorus Cycle",
    "Atmospheric Aerosol Loading",
    "Freshwater Use",
    "Stratospheric Ozone Depletion",
    "Land-system Change"
]

# EXIOBASE geographical scopes (countries and Rest-of-World regions)
EXIOBASE_GEO_SCOPES = [
    'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR',
    'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI',
    'SK', 'GB', 'US', 'JP', 'CN', 'CA', 'KR', 'BR', 'IN', 'MX', 'RU', 'AU', 'CH',
    'TR', 'TW', 'NO', 'ID', 'ZA', 'WA', 'WL', 'WE', 'WF', 'WM'
]
