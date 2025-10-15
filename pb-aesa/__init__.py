"""pb-aesa - Planetary-boundary-based absolute environmental sustainability assessment."""

# Core analysis functions
from .analysis import calculate_exploitation_of_SOS

# Visualization functions
from .visualization import plot_exploitation_of_SOS

# LCIA method creation
from .methods import (
    create_normal_methods,
    create_n_cycle_method,
    implement_lcia_methods,
)

# Nitrogen handling
from .nitrogen import (
    create_n_supply_flow,
    add_n_supply_flow_to_foreground_system,
    add_n_supply_flow_to_databases,
    add_n_supply_flow,
)

# Allocation factors
from .allocation import (
    get_all_allocation_factor,
    get_direct_FCE_allocation_factor,
    get_total_FCE_allocation_factor,
    get_direct_GVA_allocation_factor,
    get_total_GVA_allocation_factor,
)

# EXIOBASE data handling
from .exiobase import (
    download_exiobase_data,
    load_matrices,
    calculate_FR_matrix,
    calculate_direct_FCE_allocation_factors,
)

# Constants
from .constants import (
    SAFE_OPERATING_SPACE,
    PLANETARY_BOUNDARY_UNITS,
    STANDARD_CATEGORIES,
    EXIOBASE_GEO_SCOPES,
)

__version__ = "0.0.1"

__all__ = (
    "__version__",
    # Analysis
    "calculate_exploitation_of_SOS",
    # Visualization
    "plot_exploitation_of_SOS",
    # Methods
    "create_normal_methods",
    "create_n_cycle_method",
    "implement_lcia_methods",
    # Nitrogen
    "create_n_supply_flow",
    "add_n_supply_flow_to_foreground_system",
    "add_n_supply_flow_to_databases",
    "add_n_supply_flow",
    # Allocation
    "get_all_allocation_factor",
    "get_direct_FCE_allocation_factor",
    "get_total_FCE_allocation_factor",
    "get_direct_GVA_allocation_factor",
    "get_total_GVA_allocation_factor",
    # EXIOBASE
    "download_exiobase_data",
    "load_matrices",
    "calculate_FR_matrix",
    "calculate_direct_FCE_allocation_factors",
    # Constants
    "SAFE_OPERATING_SPACE",
    "PLANETARY_BOUNDARY_UNITS",
    "STANDARD_CATEGORIES",
    "EXIOBASE_GEO_SCOPES",
)
