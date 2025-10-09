"""Nitrogen-related functionality for agricultural processes."""

import copy
import bw2data as bd


def create_n_supply_flow(biosphere_db):
    """
    Creates new elementary flow for nitrogen supplied to soil of agricultural systems.

    Args:
        biosphere_db: Biosphere database from ecoinvent.
        
    Returns:
        new_bf: Biosphere Flow for N-supply to soil.
    """
    # Add new dummy biosphere flow for nitrogen supplied to an agricultural system
    flow_key = (biosphere_db.name, 'N_supply')
    
    if flow_key not in biosphere_db:
        new_bf_data_N = biosphere_db.new_activity(
            code="N_supply",
            name="N",
            type="emission",
            categories=("soil",),
            unit="kilogram",
        )
        new_bf_data_N.save()
    else:
        print("N-supply elementary flow already exists in biosphere!")

    # Retrieve the newly created (or existing) nitrogen flow
    new_bf = bd.get_activity(flow_key)
    return new_bf


def add_n_supply_flow_to_foreground_system(biosphere_db, process_ids):
    """
    Adds nitrogen supply flow to specified agricultural processes.
    
    This function modifies the specified processes to include a nitrogen supply 
    flow based on their existing nitrogen-related emissions.

    Args:
        biosphere_db: Biosphere database from ecoinvent.
        process_ids (list): List of process IDs to modify.
        
    Returns:
        None: Processes are modified with nitrogen supply flows.
    """
    # Get the nitrogen supply flow
    n_supply_flow = create_n_supply_flow(biosphere_db)

    # Add N-supply to foreground processes
    for process_id in process_ids:
        fg_process = bd.get_activity(process_id)
        
        # Create a copy of the existing exchanges
        exchanges = copy.deepcopy(list(fg_process.exchanges()))
        
        # Find nitrogen-related emissions
        n_air = 0
        n_water = 0
        
        for exc in exchanges:
            if exc["type"] == "biosphere":
                if "Nitrogen" in str(exc["name"]) or "nitrogen" in str(exc["name"]):
                    # Categorize by compartment
                    categories = exc.get("categories", ())
                    if "air" in categories:
                        n_air += exc["amount"]
                    elif "water" in categories:
                        n_water += exc["amount"]
        
        # Calculate total nitrogen supply
        n_supply = n_air + n_water
        
        # Add new exchange for N-supply
        if n_supply > 0:
            fg_process.new_exchange(
                input=n_supply_flow,
                amount=n_supply,
                type="biosphere"
            ).save()
            
            print(f"Added N-supply flow to {fg_process['name']}: {n_supply} kg")

    return None
