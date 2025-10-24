# Usage

## Overview

The `pbaesa` package provides tools for planetary-boundary-based absolute environmental sustainability assessment. It includes modules for:

- Creating LCIA methods for planetary boundaries
- Calculating exploitation of Safe Operating Space (SOS)
- Visualizing planetary boundary impacts
- Working with EXIOBASE data
- Managing allocation factors

## Basic Workflow

### 1. Setting up LCIA Methods

First, initialize your Brightway25 project and create the planetary boundary LCIA methods:

```python
import bw2data as bd
import pbaesa

# Set your Brightway25 project
bd.projects.set_current('your_project_name')

# Load your biosphere database
bio = bd.Database("ecoinvent-3.10.1-biosphere")

# Create all planetary boundary LCIA methods
pbaesa.implement_lcia_methods(bio)
```

This creates methods for:
- Climate Change
- Ocean Acidification
- Change in Biosphere Integrity
- Phosphorus Cycle
- Nitrogen Cycle (requires additional setup)
- Atmospheric Aerosol Loading
- Freshwater Use
- Stratospheric Ozone Depletion
- Land-system Change

### 2. Running an LCA Assessment

Perform a multi-LCA calculation and calculate SOS exploitation:

```python
import bw2calc as bc

# Get all planetary boundary methods
m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

# Define your functional unit
# (example: wheat grain production in Germany)
ei = bd.Database("ecoinvent-3.10.1-cutoff")
process = [act for act in ei 
           if 'DE' in act['location'] 
           and 'wheat grain production' in act['name']][0]

functional_unit = {
    "process": {ei.get(process["code"]).id: 1.0},
}

# Configure and run MultiLCA
config = {"impact_categories": m}
data_objs = bd.get_multilca_data_objs(
    functional_units=functional_unit, 
    method_config=config
)

mlca = bc.MultiLCA(
    demands=functional_unit, 
    method_config=config, 
    data_objs=data_objs
)
mlca.lci()
mlca.lcia()

# Calculate exploitation of Safe Operating Space
exploit = pbaesa.calculate_exploitation_of_SOS(mlca.scores)

# Visualize results
pbaesa.plot_exploitation_of_SOS(exploit)
```

### 3. Working with Nitrogen Cycle

For agricultural systems, add nitrogen supply flows:

```python
# Create nitrogen supply flow
n_flow = pbaesa.create_n_supply_flow(bio)

# Add to agricultural processes
process_ids = [process.id for process in your_agricultural_processes]
pbaesa.add_n_supply_flow_to_foreground_system(bio, process_ids)
```

### 4. Working with Allocation Factors

Retrieve allocation factors for specific sectors and geographical scopes:

```python
# Get all allocation factors
factors = pbaesa.get_all_allocation_factor(
    geographical_scope="DE",  # Germany
    sector="Cultivation of wheat",
    year=2022
)

# Or get specific allocation factors
direct_fce = pbaesa.get_direct_FCE_allocation_factor("DE", "Cultivation of wheat", 2022)
total_fce = pbaesa.get_total_FCE_allocation_factor("DE", "Cultivation of wheat", 2022)
direct_gva = pbaesa.get_direct_GVA_allocation_factor("DE", "Cultivation of wheat", 2022)
total_gva = pbaesa.get_total_GVA_allocation_factor("DE", "Cultivation of wheat", 2022)
```

### 5. Working with EXIOBASE Data

Download and process EXIOBASE data:

```python
# Download EXIOBASE data for a specific year
pbaesa.download_exiobase_data(year=2022)

# Load Leontief inverse and final demand matrices
L, Y = pbaesa.load_matrices(year=2022)

# Calculate FR matrix (sector share of final consumption expenditure)
FR_matrix = pbaesa.calculate_FR_matrix(year=2022)
```

## Constants and Reference Values

Access planetary boundary thresholds and other constants:

```python
# Safe Operating Space thresholds
thresholds = pbaesa.SAFE_OPERATING_SPACE

# Planetary boundary units
units = pbaesa.PLANETARY_BOUNDARY_UNITS

# Standard categories
categories = pbaesa.STANDARD_CATEGORIES

# EXIOBASE geographical scopes
geo_scopes = pbaesa.EXIOBASE_GEO_SCOPES
```

## Module Structure

The package is organized into the following modules:

- **`methods`**: LCIA method creation and management
- **`analysis`**: SOS exploitation calculations
- **`visualization`**: Plotting and visualization functions
- **`nitrogen`**: Nitrogen flow handling for agricultural systems
- **`allocation`**: Allocation factor retrieval
- **`exiobase`**: EXIOBASE data handling
- **`constants`**: Reference values and thresholds

## Advanced Usage

### Custom Method Creation

Create only specific methods:

```python
# Create only standard methods (without nitrogen cycle)
pbaesa.create_normal_methods(bio)

# Create only nitrogen cycle method
pbaesa.create_n_cycle_method(bio, process_ids=agricultural_process_ids)
```

### Customizing Visualizations

The visualization functions use matplotlib, so you can customize plots:

```python
import matplotlib.pyplot as plt

# Calculate exploitation
exploit = pbaesa.calculate_exploitation_of_SOS(mlca.scores)

# Create custom plot
labels = [key[0][1] for key in exploit.keys()]
values = list(exploit.values())

plt.figure(figsize=(14, 7))
plt.bar(labels, values, color='steelblue')
plt.axhline(y=1.0, color='r', linestyle='--', label='SOS Boundary')
plt.xlabel('Earth-system process')
plt.ylabel('Exploitation of Safe Operating Space')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.show()
```