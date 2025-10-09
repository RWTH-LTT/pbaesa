"""Allocation factor functions for planetary boundary assessments."""

import os
import glob
import pandas as pd


def get_all_allocation_factor(geographical_scope, sector, year):
    """
    Retrieves all allocation factors for a specific geographical scope and sector.
    
    Args:
        geographical_scope (str): Geographical scope (country code or region).
        sector (str): Sector name (following EU's NACE Rev.1 classification).
        year (int): Year for which to retrieve allocation factors.
        
    Returns:
        DataFrame: Filtered dataframe with allocation factors for the specified 
                  scope and sector, or None if not found.
    """
    directory = "Allocation Factors"
    pattern = os.path.join(directory, f'*_{year}.xlsx')
    matching_file = glob.glob(pattern)
  
    if matching_file:
        file_path_allocation_factors = matching_file[0]
        allocation_factor_df = pd.read_excel(file_path_allocation_factors)

        geo_scope_col = "Country (c.f. ISO 3166-1 alpha-2) \n& Rest of World regions"
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
    else:
        print("Calculation of allocation factors necessary!")
        return None


def get_direct_FCE_allocation_factor(geographical_scope, sector, year):
    """
    Retrieves the direct Final Consumption Expenditure allocation factor.
    
    Args:
        geographical_scope (str): Geographical scope (country code or region).
        sector (str): Sector name.
        year (int): Year for which to retrieve the allocation factor.
        
    Returns:
        float: Direct FCE allocation factor, or None if not found.
    """
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is not None:
        af_direct_fce = filtered_df[
            'Allocation factors calculated \nvia direct final consumption expenditure'
        ].values[0]
        return af_direct_fce
    return None


def get_total_FCE_allocation_factor(geographical_scope, sector, year):
    """
    Retrieves the total Final Consumption Expenditure allocation factor.
    
    Args:
        geographical_scope (str): Geographical scope (country code or region).
        sector (str): Sector name.
        year (int): Year for which to retrieve the allocation factor.
        
    Returns:
        float: Total FCE allocation factor, or None if not found.
    """
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is not None:
        af_total_fce = filtered_df[
            'Allocation factors calculated \nvia total final consumption expenditure'
        ].values[0]
        return af_total_fce
    return None


def get_direct_GVA_allocation_factor(geographical_scope, sector, year):
    """
    Retrieves the direct Gross Value Added allocation factor.
    
    Args:
        geographical_scope (str): Geographical scope (country code or region).
        sector (str): Sector name.
        year (int): Year for which to retrieve the allocation factor.
        
    Returns:
        float: Direct GVA allocation factor, or None if not found.
    """
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is not None:
        af_direct_gva = filtered_df[
            'Allocation factors calculated \nvia direct gross value added'
        ].values[0]
        return af_direct_gva
    return None


def get_total_GVA_allocation_factor(geographical_scope, sector, year):
    """
    Retrieves the total Gross Value Added allocation factor.
    
    Args:
        geographical_scope (str): Geographical scope (country code or region).
        sector (str): Sector name.
        year (int): Year for which to retrieve the allocation factor.
        
    Returns:
        float: Total GVA allocation factor, or None if not found.
    """
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year)
    if filtered_df is not None:
        ag_total_gva = filtered_df[
            'Allocation factors calculated \nvia total gross value added'
        ].values[0]
        return ag_total_gva
    return None
