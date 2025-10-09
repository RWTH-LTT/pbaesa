"""
Example usage of the pb-aesa package.

This example demonstrates how to:
1. Set up LCIA methods for planetary boundaries
2. Run a MultiLCA assessment
3. Calculate exploitation of Safe Operating Space
4. Visualize results
"""

import bw2data as bd
import bw2calc as bc
import pb_aesa

# ============================================================================
# 1. Initialize Brightway25 project and databases
# ============================================================================

# Set the current Brightway25 project
bd.projects.set_current('PB_AESA')

# Load databases
bio = bd.Database("ecoinvent-3.10.1-biosphere")
ei = bd.Database("ecoinvent-3.10.1-cutoff")

# ============================================================================
# 2. Create planetary boundary LCIA methods
# ============================================================================

# Create all LCIA methods (standard + nitrogen cycle)
pb_aesa.implement_lcia_methods(bio)

# ============================================================================
# 3. Define functional unit and run MultiLCA
# ============================================================================

# Get all planetary boundary methods
m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

# Select a process (example: wheat grain production in Germany)
dummy_process = [
    act for act in ei 
    if 'DE' in act['location'] 
    and 'wheat grain production' in act['name']
][0]

# Define functional unit
functional_unit = {
    "dummy_process": {ei.get(dummy_process["code"]).id: 22.6 * 10e9},
}

# Configure MultiLCA
config = {
    "impact_categories": m
}

# Get data objects
data_objs = bd.get_multilca_data_objs(
    functional_units=functional_unit, 
    method_config=config
)

# Run MultiLCA
mlca = bc.MultiLCA(
    demands=functional_unit, 
    method_config=config, 
    data_objs=data_objs
)
mlca.lci()
mlca.lcia()
mlca_scores = mlca.scores

# ============================================================================
# 4. Calculate and visualize exploitation of Safe Operating Space
# ============================================================================

# Calculate exploitation
exploit = pb_aesa.calculate_exploitation_of_SOS(mlca_scores)

# Print results
print("\n" + "="*70)
print("Exploitation of Safe Operating Space")
print("="*70)
for method_key, value in exploit.items():
    category = method_key[0][1]
    if value is not None:
        print(f"{category:.<50} {value:.4f}")
    else:
        print(f"{category:.<50} N/A")
print("="*70)

# Plot results
pb_aesa.plot_exploitation_of_SOS(exploit)

# ============================================================================
# 5. Access constants and reference values
# ============================================================================

print("\nSafe Operating Space Thresholds:")
for category, threshold in pb_aesa.SAFE_OPERATING_SPACE.items():
    print(f"  {category}: {threshold}")

print("\nAvailable EXIOBASE geographical scopes:")
print(f"  {len(pb_aesa.EXIOBASE_GEO_SCOPES)} regions: {', '.join(pb_aesa.EXIOBASE_GEO_SCOPES[:10])}...")
