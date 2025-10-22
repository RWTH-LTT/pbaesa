"""LCIA methods for planetary boundaries."""

import pandas as pd
import bw2data as bd

from .constants import STANDARD_CATEGORIES, PLANETARY_BOUNDARY_UNITS


def create_normal_methods(biosphere_db):
    """
    Creates life cycle impact assessment methods for the planetary boundary categories.
    
    Creates methods for: climate change, ocean acidification, change in biosphere 
    integrity, phosphorus cycle, atmospheric aerosol loading, freshwater use, 
    stratospheric ozone depletion and land-system change.
    
    The life cycle impact assessment methods cover all elementary flows included in 
    standard and prospective ecoinvent v3.10.1. Other ecoinvent versions are supported 
    partially.

    Args:
        biosphere_db: Biosphere database from ecoinvent.
        
    Returns:
        None: LCIA methods are implemented.
    """
    # Load characterization factors for planetary boundary categories from Excel file
    file_path_characterization_factors = (
        "Characterization Factors + Import Script\\Characterization Factors_for_eco3101.xlsx"
    )
    df_pb = pd.read_excel(
        file_path_characterization_factors, 
        sheet_name='Characterization Factors'
    )
    df_pb = df_pb.iloc[1:].reset_index(drop=True)

    # Collect existing planetary boundary methods
    m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

    # Iterate over each category to create and register LCIA methods
    for cat in STANDARD_CATEGORIES:
        method_key = ('Planetary Boundaries', cat)

        if method_key not in m:
            my_method = bd.Method(method_key)
            myLCIAdata = []

            # Collect characterization factors for the current category
            for index, row in df_pb.iterrows(): 
                myLCIAdata.append([(biosphere_db.name, row['Code']), row[cat]])

            # Register and write the method to Brightway25
            my_method.validate(myLCIAdata)
            my_method.register()
            my_method.write(myLCIAdata)
            bd.methods[method_key]["unit"] = PLANETARY_BOUNDARY_UNITS[cat]
            bd.methods.flush()

    # Display all LCIA methods for the Planetary Boundary Framework
    m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

    print("The following planetary boundary categories are now available as LCIA-methods:")
    for method in m:
        print(f"- {method}")

    return None


def create_n_cycle_method(biosphere_db, process_ids=None):
    """
    Creates LCIA method for the nitrogen cycle planetary boundary category.
    
    This method requires a nitrogen supply flow to be added to agricultural processes.

    Args:
        biosphere_db: Biosphere database from ecoinvent.
        process_ids (list, optional): List of process IDs for agricultural activities.
                                     Defaults to None.
        
    Returns:
        None: LCIA method for nitrogen cycle is implemented.
    """
    if process_ids is None:
        process_ids = []
    
    # Load characterization factors for nitrogen cycle from Excel file
    file_path_characterization_factors = (
        "Characterization Factors + Import Script\\Characterization Factors_for_eco3101.xlsx"
    )
    df_pb_N = pd.read_excel(
        file_path_characterization_factors, 
        sheet_name='CF Nitrogen Cycle'
    )

    # Collect existing planetary boundary methods
    m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

    # Check if nitrogen cycle method already exists
    category = "Nitrogen Cycle"
    method_key = ('Planetary Boundaries', category)

    if method_key not in m:
        my_method = bd.Method(method_key)
        myLCIAdata = []

        # Collect characterization factors for nitrogen cycle category
        for index, row in df_pb_N.iterrows():
            if row['Code'] == "N_supply":
                # Use a simplified characterization factor calculation
                cf = (1 - 0.68) * (1 - 0.68) * 1 / 62 * 1000000
                myLCIAdata.append([(biosphere_db.name, row['Code']), cf])
            else:
                myLCIAdata.append([(biosphere_db.name, row['Code']), row['Nitrogen Cycle']])

        # Register and write the method to Brightway25
        my_method.validate(myLCIAdata)
        my_method.register()
        my_method.write(myLCIAdata)
        bd.methods[method_key]["unit"] = (
            "N-flow from Anthroposphere to Atmosphere and Hydrosphere [Tg N/year]"
        )
        bd.methods.flush()

        print(f"Nitrogen Cycle LCIA method created: {method_key}")
    else:
        print("Nitrogen Cycle method already exists!")

    return None


def create_pbaesa_methods(biosphere_db, process_ids=None):
    """
    Creates and registers LCIA methods for all global planetary boundary categories.
    
    This is the main user-facing function to set up all planetary boundary LCIA 
    methods except novel entities. It creates both standard methods (climate change,
    ocean acidification, etc.) and the nitrogen cycle method.

    Args:
        biosphere_db: Biosphere database from ecoinvent.
        process_ids (list, optional): List of process IDs for agricultural activities 
                                     (used for nitrogen cycle). Defaults to None.
        
    Returns:
        None: LCIA methods are implemented.
    """
    if process_ids is None:
        process_ids = []
    
    create_n_cycle_method(biosphere_db, process_ids=process_ids)
    create_normal_methods(biosphere_db)

    return None


def implement_lcia_methods(biosphere_db, process_ids=None):
    """
    Implements all LCIA methods for planetary boundaries.
    
    This is a convenience function that creates both standard methods and 
    the nitrogen cycle method. Alias for create_pbaesa_methods.

    Args:
        biosphere_db: Biosphere database from ecoinvent.
        process_ids (list, optional): List of process IDs for agricultural activities 
                                     (used for nitrogen cycle). Defaults to None.
        
    Returns:
        None: LCIA methods are implemented.
    """
    return create_pbaesa_methods(biosphere_db, process_ids=process_ids)
