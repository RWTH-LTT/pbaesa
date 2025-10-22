"""
Allocation factor retrieval and calculation for planetary boundaries.
"""

import pandas as pd
import glob
import os


def export_all_allocation_factors(year):
    """
    Calculate and export all allocation factors for a given year.
    
    This function calculates allocation factors based on EXIOBASE data and exports them
    to an Excel file. The allocation factors are based on:
    - Direct final consumption expenditure (FCE)
    - Total final consumption expenditure (FCE)
    - Direct gross value added (GVA)
    - Total gross value added (GVA)
    
    Parameters:
        year: int - The year for which to calculate allocation factors
        
    Returns:
        str: Path to the generated Excel file
        
    Raises:
        NotImplementedError: This function requires EXIOBASE data processing which
                           needs to be implemented with the full calculation logic.
    """
    raise NotImplementedError(
        "export_all_allocation_factors requires EXIOBASE data processing. "
        "This functionality needs to be implemented with the complete calculation logic "
        "from the notebook. For now, please generate allocation factor files manually "
        "using the Jupyter notebook."
    )


def get_all_allocation_factor(geographical_scope, sector, year):
    """
    Get all allocation factors for a sector in a specific geographical scope and for a specific year.
    
    If the allocation factors file does not exist, this function will attempt to download/calculate it
    automatically by calling export_all_allocation_factors.

    Parameters:
        geographical_scope: str - ISO 3166-1 alpha-2 country code or Rest of World region
        sector: str - Sector name according to EU's NACE Rev.1 classification
        year: int - Year for which to retrieve allocation factors

    Returns:
        filtered_df: A pandas DataFrame with allocation factors for the specified sector 
                    and geographical scope, or None if not found.
    """    
    
    pattern = f"Allocation Factors_{year}.xlsx"
    matching_file = glob.glob(pattern)
  
    if not matching_file:
        print(f"Allocation factors file for year {year} not found.")
        print("Attempting to generate allocation factors...")
        try:
            export_all_allocation_factors(year)
            # Re-check for the file after generation
            matching_file = glob.glob(pattern)
            if not matching_file:
                print("Failed to generate allocation factors file.")
                return None
        except NotImplementedError as e:
            print(f"Error: {e}")
            print("\nPlease provide the allocation factors file manually.")
            print(f"Expected file name: {pattern}")
            return None
    
    file_path_allocation_factors = matching_file[0]
    allocation_factor_df = pd.read_excel(file_path_allocation_factors)

    geo_scope_col = "Country (c.f. ISO 3166-1 alpha-2) & Rest of World regions"
    sector_col = "Sector (c.f. EU's NACE Rev.1 classification)"

    if geographical_scope not in allocation_factor_df[geo_scope_col].values:
        print("Invalid location. Available options:")
        print(allocation_factor_df[geo_scope_col].unique())
        return None

    if sector not in allocation_factor_df[sector_col].values:
        print("Invalid sector. Available options:")
        print(allocation_factor_df[sector_col].unique())
        return None

    filtered_df = allocation_factor_df[
        (allocation_factor_df[geo_scope_col] == geographical_scope) &
        (allocation_factor_df[sector_col] == sector)
    ]

    return filtered_df


def get_direct_FCE_allocation_factor(geographical_scope, sector, year):
    """
    Get allocation factors based on direct FCE for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int

    Returns:
        af_direct_fce: Allocation factor based on direct FCE
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is None or filtered_df.empty:
        return None
    
    # Try multiple possible column names due to formatting variations
    possible_columns = [
        'Allocation factor calculated via direct final consumption expenditure',
        'Allocation factors calculated \nvia direct final consumption expenditure'
    ]
    
    for col in possible_columns:
        if col in filtered_df.columns:
            return filtered_df[col].values[0]
    
    print(f"Column for direct FCE not found. Available columns: {filtered_df.columns.tolist()}")
    return None


def get_total_FCE_allocation_factor(geographical_scope, sector, year):
    """
    Get allocation factors based on total FCE for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int

    Returns:
        af_total_fce: Allocation factor based on total FCE
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is None or filtered_df.empty:
        return None
    
    # Try multiple possible column names due to formatting variations
    possible_columns = [
        'Allocation factor calculated via total final consumption expenditure',
        'Allocation factors calculated \nvia total final consumption expenditure'
    ]
    
    for col in possible_columns:
        if col in filtered_df.columns:
            return filtered_df[col].values[0]
    
    print(f"Column for total FCE not found. Available columns: {filtered_df.columns.tolist()}")
    return None


def get_direct_GVA_allocation_factor(geographical_scope, sector, year):
    """
    Get allocation factors based on direct GVA for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int

    Returns:
        af_direct_gva: Allocation factor based on direct GVA
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is None or filtered_df.empty:
        return None
    
    # Try multiple possible column names due to formatting variations
    possible_columns = [
        'Allocation factor calculated via direct gross value added',
        'Allocation factors calculated \nvia direct gross value added'
    ]
    
    for col in possible_columns:
        if col in filtered_df.columns:
            return filtered_df[col].values[0]
    
    print(f"Column for direct GVA not found. Available columns: {filtered_df.columns.tolist()}")
    return None


def get_total_GVA_allocation_factor(geographical_scope, sector, year):
    """
    Get allocation factors based on total GVA for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int

    Returns:
        ag_total_gva: Allocation factor based on total GVA
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is None or filtered_df.empty:
        return None
    
    # Try multiple possible column names due to formatting variations
    possible_columns = [
        'Allocation factor calculated via total gross value added',
        'Allocation factors calculated \nvia total gross value added'
    ]
    
    for col in possible_columns:
        if col in filtered_df.columns:
            return filtered_df[col].values[0]
    
    print(f"Column for total GVA not found. Available columns: {filtered_df.columns.tolist()}")
    return None
