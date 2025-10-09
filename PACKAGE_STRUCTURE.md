# Package Structure

This document describes the modular structure of the pb-aesa package, which was created from the functionality in `package.ipynb`.

## Module Overview

The package has been organized into 7 focused modules:

### 1. `constants.py`
**Purpose**: Store reference values and configuration constants

**Contents**:
- `SAFE_OPERATING_SPACE`: Dictionary of planetary boundary thresholds
- `PLANETARY_BOUNDARY_UNITS`: Units for each planetary boundary category
- `STANDARD_CATEGORIES`: List of standard planetary boundary categories
- `EXIOBASE_GEO_SCOPES`: List of geographical scopes in EXIOBASE

### 2. `methods.py`
**Purpose**: LCIA method creation and management

**Functions**:
- `create_normal_methods(biosphere_db)`: Creates standard PB LCIA methods
- `create_n_cycle_method(biosphere_db, process_ids)`: Creates nitrogen cycle LCIA method
- `implement_lcia_methods(biosphere_db, process_ids)`: Creates all LCIA methods (convenience wrapper)

### 3. `nitrogen.py`
**Purpose**: Nitrogen flow handling for agricultural systems

**Functions**:
- `create_n_supply_flow(biosphere_db)`: Creates N-supply elementary flow
- `add_n_supply_flow_to_foreground_system(biosphere_db, process_ids)`: Adds N-supply to custom processes
- `add_n_supply_flow_to_databases(biosphere_db)`: Adds N-supply to fertiliser processes
- `add_n_supply_flow(biosphere_db, process_ids)`: Adds N-supply to all relevant processes (wrapper)

### 4. `analysis.py`
**Purpose**: Core analysis functions

**Functions**:
- `calculate_exploitation_of_SOS(mlca_scores)`: Calculates Safe Operating Space exploitation

### 5. `visualization.py`
**Purpose**: Visualization and plotting functions

**Functions**:
- `plot_exploitation_of_SOS(exploitation_of_SOS)`: Creates bar chart of SOS exploitation

### 6. `allocation.py`
**Purpose**: Allocation factor retrieval

**Functions**:
- `get_all_allocation_factor(geographical_scope, sector, year)`: Gets all allocation factors
- `get_direct_FCE_allocation_factor(geographical_scope, sector, year)`: Gets direct FCE factor
- `get_total_FCE_allocation_factor(geographical_scope, sector, year)`: Gets total FCE factor
- `get_direct_GVA_allocation_factor(geographical_scope, sector, year)`: Gets direct GVA factor
- `get_total_GVA_allocation_factor(geographical_scope, sector, year)`: Gets total GVA factor

### 7. `exiobase.py`
**Purpose**: EXIOBASE data handling and matrix calculations

**Functions**:
- `download_exiobase_data(year)`: Downloads EXIOBASE data
- `load_matrices(year)`: Loads Leontief inverse and final demand matrices
- `calculate_FR_matrix(year)`: Calculates FR matrix (sector share of FCE)
- `calculate_direct_FCE_allocation_factors(year)`: Placeholder for allocation factor calculation

## Design Principles

The modular structure follows these principles:

1. **Separation of Concerns**: Each module handles a specific aspect of the functionality
2. **User-Friendly API**: Key functions are exposed through `__init__.py`
3. **Documentation**: All functions have comprehensive docstrings
4. **Constants Centralization**: Reference values are stored in one place for easy maintenance
5. **Minimal Changes**: The original logic from the notebook is preserved with minimal modifications

## Usage

All main functions are accessible directly from the package:

```python
import pb_aesa

# Access functions
pb_aesa.implement_lcia_methods(bio)
exploit = pb_aesa.calculate_exploitation_of_SOS(mlca.scores)
pb_aesa.plot_exploitation_of_SOS(exploit)

# Access constants
thresholds = pb_aesa.SAFE_OPERATING_SPACE
```

For detailed usage examples, see:
- `examples/basic_usage.py`
- `docs/content/usage.md`

## Migration from Notebook

If you were using the notebook directly, here's how to migrate:

| Notebook Function | Module Location | Import |
|------------------|-----------------|--------|
| `create_normal_methods()` | `methods.py` | `from pb_aesa import create_normal_methods` |
| `create_n_cycle_method()` | `methods.py` | `from pb_aesa import create_n_cycle_method` |
| `create_pbaesa_methods()` | `methods.py` (renamed) | `from pb_aesa import implement_lcia_methods` |
| `create_n_supply_flow()` | `nitrogen.py` | `from pb_aesa import create_n_supply_flow` |
| `add_n_supply_flow()` | `nitrogen.py` | `from pb_aesa import add_n_supply_flow` |
| `calculate_exploitation_of_SOS()` | `analysis.py` | `from pb_aesa import calculate_exploitation_of_SOS` |
| `plot_exploitation_of_SOS()` | `visualization.py` | `from pb_aesa import plot_exploitation_of_SOS` |
| `get_*_allocation_factor()` | `allocation.py` | `from pb_aesa import get_*_allocation_factor` |
| `*_exiobase_*()` | `exiobase.py` | `from pb_aesa import *_exiobase_*` |

## File Structure

```
pb-aesa/
├── __init__.py           # Package initialization and API exposure
├── constants.py          # Reference values and constants
├── methods.py            # LCIA method creation
├── nitrogen.py           # Nitrogen flow handling
├── analysis.py           # SOS exploitation calculation
├── visualization.py      # Plotting functions
├── allocation.py         # Allocation factor retrieval
├── exiobase.py          # EXIOBASE data handling
└── package.ipynb        # Original notebook (for reference)
```
