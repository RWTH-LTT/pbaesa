"""
LCIA method creation and management for planetary boundaries.
"""

import pandas as pd
import bw2data as bd
import os


def create_normal_methods(biosphere_db=None):
    """
    Creates life cycle impact assessment methods for the planetary boundary categories: 
    climate change, ocean acidification, change in biosphere integrity, phosphorus cycle, 
    atmospheric aerosol loading, freshwater use, stratospheric ozone depletion and 
    land-system change.
    
    The life cycle impact assessment methods cover all elementary flows included in 
    standard and prospective ecoinvent v3.10.1. Other ecoinvent versions are, however, 
    supported partially.

    Args:
        biosphere_db (database): Biosphere database from ecoinvent.
        
    Returns:
        None: LCIA methods are implemented.
    """

    # Load characterization factors for planetary boundary categories from Excel file
    file_path_characterization_factors = "Characterization Factors_for_eco3101.xlsx"
    
    # Check if file exists in current directory or package data directory
    if not os.path.exists(file_path_characterization_factors):
        # Try to find it in the package directory
        package_dir = os.path.dirname(__file__)
        alt_path = os.path.join(package_dir, "data", file_path_characterization_factors)
        if os.path.exists(alt_path):
            file_path_characterization_factors = alt_path
        else:
            raise FileNotFoundError(
                f"Characterization factors file not found. Please ensure "
                f"'{file_path_characterization_factors}' is in the current directory or "
                f"contact the package maintainers for the data file."
            )
    
    df_pb = pd.read_excel(file_path_characterization_factors, sheet_name='Characterization Factors')
    df_pb = df_pb.iloc[1:].reset_index(drop=True)

    # Collect existing planetary boundary methods
    m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

    # Define list of planetary boundary category names
    categories = [
        "Climate Change",
        "Ocean Acidification",
        "Change in Biosphere Integrity",
        "Phosphorus Cycle",
        "Atmospheric Aerosol Loading",
        "Freshwater Use",
        "Stratospheric Ozone Depletion",
        "Land-system Change"
    ]

    # Define corresponding units for each planetary boundary category
    units = {
        "Climate Change": "Energy imbalance at top-of-atmosphere [W/m²]",
        "Ocean Acidification": "Aragonite saturation state [Ωₐᵣₐ]",
        "Change in Biosphere Integrity": "Biodiversity Intactness Index [%]",
        "Phosphorus Cycle": "P-flow from freshwater systems into the ocean [Tg P/year]",
        "Atmospheric Aerosol Loading": "Aerosol optical depth (AOD) [-]",
        "Freshwater Use": "Consumptive bluewater use [km³/year]",
        "Stratospheric Ozone Depletion": "Stratospheric ozone concentration [DU]",
        "Land-system Change": "Land available for anthropogenic occupation [millon km²]"
    }

    # Iterate over each category to create and register LCIA methods
    for cat in categories:
        
        method_key = ('Planetary Boundaries', cat)  # Define method key as (framework, category)

        if method_key not in m:
            my_method = bd.Method(method_key) # Initialize Brightway25 Method object

            myLCIAdata = [] # Initialize list to store LCIA data

            # Collect characterization factors for the current category
            for index, row in df_pb.iterrows(): 
                myLCIAdata.append([(biosphere_db.name, row['Code']), row[cat]])

            # Register and write the method to Brightway25
            my_method.validate(myLCIAdata)
            my_method.register()
            my_method.write(myLCIAdata)
            bd.methods[method_key]["unit"] = units[cat] # Assign correct unit
            bd.methods.flush() # Save changes to methods database

    # Display all LCIA methods for the Planetary Boundary Framework
    m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

    print("The following planetary boundary categories are now available as LCIA-methods:")
    for method in m:
        print(f"- {method}")

    return None


def create_n_supply_flow(biosphere_db=None):
    """
    Creates new elementary flow for nitrogen supplied to soil of agricultural systems.

    Args:
        biosphere_db (database): Biosphere database from ecoinvent.
        
    Returns:
        new_bf: Biosphere Flow for N-supply to soil.
    """

    # Add new dummy biosphere flow for nitrogen supplied to an agricultural system, if it doesn't already exist
    if (biosphere_db.name, 'N_supply') not in biosphere_db:
        new_bf_data_N = biosphere_db.new_activity(
            code = "N_supply",
            name = "N",
            type = "emission",
            categories = ("soil",),
            unit ="kilogram",        
        )

        new_bf_data_N.save() # Register the new nitrogen flow in the biosphere database
    else:
        print("N-supply elementary flows already exists in biosphere!")

    # Retrieve the newly created (or existing) nitrogen flow
    new_bf = bd.get_activity((biosphere_db.name, "N_supply"))
    return new_bf


def add_n_supply_flow_to_foreground_system(biosphere_db=None, process_ids=[]):
    """
    Adds elementary flow of N-supply to soil to custom processes in the foreground-system.

    Args:
        biosphere_db (database): Biosphere database from ecoinvent.
        process_ids (list): List of codes that identify custom processes in their respective database.
        
    Returns:
        None: N-supply flow added to processes.
    """
    
    new_bf = create_n_supply_flow(biosphere_db)
    
    for db_name in bd.databases:
        db = bd.Database(db_name)
        for id in process_ids:
            rev_N = [act for act in db if id in act['code']][0] # Retrieve activity

            # Check if the nitrogen flow is already included
            exchangeN = [exc for exc in rev_N.exchanges() if 'biosphere' in exc['type'] and exc['input'] == (biosphere_db.name, 'N_supply')]


            if len(exchangeN)<1:
                # Add nitrogen flow exchange if not present
                rev_N.new_exchange(input=new_bf,amount=1,type='biosphere').save()
                rev_N.save()
                exchangeN = [exc for exc in rev_N.exchanges() if 'biosphere' in exc['type'] and exc['input'] == (biosphere_db.name, 'N_supply')]  
                print('N-flow added to {} - {}. Exchanges: {}'.format(rev_N['reference product'],rev_N['name'],len(exchangeN)))
            else:
                print('N-flow already added to {} - {}. Exchanges: {}'.format(rev_N['reference product'],rev_N['name'],len(exchangeN)))

    return None         


def add_n_supply_flow_to_databases(biosphere_db=None):
    """
    Adds elementary flow of N-supply to soil to all processes that supply nitrogen to 
    agricultural systems that are not custom processes.

    Args:
        biosphere_db (database): Biosphere database from ecoinvent.
        
    Returns:
        None: N-supply flow added to processes.
    """
    new_bf = create_n_supply_flow(biosphere_db)

    for db_name in bd.databases:
        db = bd.Database(db_name)
        # Step 1: Identify ecoinvent processes (fertiliser supply systems)
        n_search = [act for act in db if 'nutrient' in act['name']]

        if not n_search:
            continue
        
        all_supply = pd.DataFrame(n_search)

        # Filter for relevant nitrogen fertiliser types
        options = ['inorganic nitrogen fertiliser, as N', 'organic nitrogen fertiliser, as N']
        N = all_supply[all_supply['reference product'].isin(options)]

        # Step 2: Add dummy nitrogen flow to each of the identified processes
        for index, n in N.iterrows():
            act_ID = n['code']  # Use activity code as unique identifier
            rev_N = [act for act in db if act_ID in act['code']][0] # Retrieve activity

            # Check if the nitrogen flow is already included
            exchangeN = [exc for exc in rev_N.exchanges() if 'biosphere' in exc['type'] and exc['input'] == (biosphere_db.name, 'N_supply')]


            if len(exchangeN)<1:
                # Add nitrogen flow exchange if not present
                rev_N.new_exchange(input=new_bf,amount=1,type='biosphere').save()
                rev_N.save()
                exchangeN = [exc for exc in rev_N.exchanges() if 'biosphere' in exc['type'] and exc['input'] == (biosphere_db.name, 'N_supply')]  
                print('N-flow added to {} - {}. Exchanges: {}'.format(rev_N['reference product'],rev_N['name'],len(exchangeN)))
            else:
                print('N-flow already added to {} - {}. Exchanges: {}'.format(rev_N['reference product'],rev_N['name'],len(exchangeN)))

    return None         


def add_n_supply_flow(biosphere_db=None, process_ids=[]):
    """
    Adds elementary flow of N-supply to soil to all processes that supply nitrogen to 
    agricultural systems.

    Args:
        biosphere_db (database): Biosphere database from ecoinvent.
        process_ids (list): List of codes that identify custom processes in their respective database.
        
    Returns:
        None: N-supply flow added to processes.
    """
    add_n_supply_flow_to_foreground_system(biosphere_db, process_ids)
    add_n_supply_flow_to_databases(biosphere_db)

    return None


def create_n_cycle_method(biosphere_db=None, process_ids=[]):
    """
    Creates and registers the LCIA method for the nitrogen cycle

    Args:
        biosphere_db (database): Biosphere database from ecoinvent.
        process_ids (list): List of codes that identify custom processes in their respective database.

    Returns:
        None: LCIA method is implemented.        
    """
    
    # Add N-supply elementary flow to all processes that supply nitrogen to agricultural systems
    add_n_supply_flow(biosphere_db, process_ids)

    # Collect existing planetary boundary methods
    m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

    # Define unit for LCIA method
    units = {"Nitrogen Cycle": "Industrial and intentional biological fixation of N [Tg N/year]"}   
    
    # Define the method key for the nitrogen cycle
    method_key = ('Planetary Boundaries', 'Nitrogen Cycle')
    if method_key not in m:
        my_method = bd.Method(method_key)

        # Link the dummy nitrogen flow to its characterization factor (value converts kg to Tg)
        myLCIAdata = [[(biosphere_db.name, 'N_supply'), 0.000000001]]

        # Register and write the LCIA method
        my_method.validate(myLCIAdata)
        my_method.register()
        bd.methods[method_key]["unit"] = units["Nitrogen Cycle"]  # Assign correct unit
        my_method.write(myLCIAdata)
        bd.methods.flush() # Commit method to database

    # Display all LCIA methods for the Planetary Boundary Framework
    m = [met for met in bd.methods if "Planetary Boundaries" in str(met)]

    print("The following planetary boundary categories are now available as LCIA-methods:")
    for method in m:
        print(f"- {method}")

    return None


def create_pbaesa_methods(biosphere_db=None, process_ids=[]):
    """
    Creates and registers LCIA methods for all global planetary boundary categories 
    except novel entities.

    Args:
        biosphere_db (database): Biosphere database from ecoinvent.
        process_ids (list): List of codes that identify custom processes in their respective database.

    Returns:
        None: LCIA methods are implemented.        
    """
    create_n_cycle_method(biosphere_db, process_ids)
    create_normal_methods(biosphere_db)
    print("All Planetary-Boundary-LCIA methods are successfully implemented in your project!")
    return None
