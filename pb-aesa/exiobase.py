"""EXIOBASE data handling and matrix calculations."""

import os
import glob
import numpy as np
import pandas as pd
import pymrio as p

from .constants import EXIOBASE_GEO_SCOPES


def download_exiobase_data(year):
    """
    Downloads EXIOBASE3 data for a specific year.
    
    Args:
        year (int): Year for which to download EXIOBASE data (1995-2022).
        
    Returns:
        dict: Download log from pymrio.
    """
    exio_storage_folder = os.path.abspath("./exiobase")
    exio_downloadlog = p.download_exiobase3(
        storage_folder=exio_storage_folder, 
        system="ixi", 
        years=[year]
    )
    return exio_downloadlog


def load_matrices(year):
    """
    Loads Leontief inverse (L) and final demand (Y) matrices from EXIOBASE.
    
    Downloads EXIOBASE data if not already present, parses it, and calculates 
    the Leontief inverse matrix.
    
    Args:
        year (int): Year for which to load matrices (1995-2022).
        
    Returns:
        tuple: (L, Y) where L is the Leontief inverse matrix and Y is the 
               final demand matrix.
    """
    exio_storage_folder = os.path.abspath("./exiobase")
    pattern = os.path.join(exio_storage_folder, f'IOT_{year}_*.zip')
    matching_files = glob.glob(pattern)

    if matching_files:
        exio_file_path = matching_files[0]
    else:
        print(f"EXIOBASE data for {year} not found. Downloading...")
        download_exiobase_data(year)
        matching_files = glob.glob(pattern)
        if matching_files:
            exio_file_path = matching_files[0]
        else:
            raise ValueError(
                "EXIOBASE versions only exist from 1995 to 2022! Choose another year."
            )
    
    # Parse EXIOBASE data
    exio3 = p.parse_exiobase3(exio_file_path)

    # Calculate Leontief inverse
    exio3.calc_all()

    # Extract transaction matrix (Z) and final demand (Y)
    Z = exio3.Z
    Y = exio3.Y

    # Calculate total output (x)
    x = Z.sum(axis=1) + Y.sum(axis=1)

    # Calculate technical coefficient matrix (A)
    x_diag_inv = np.diag(1 / x.values)
    A = Z.values @ x_diag_inv

    # Calculate Leontief inverse (L = (I - A)^-1)
    I = np.eye(A.shape[0])
    L = np.linalg.inv(I - A)

    # Delete not further needed variables to liberate storage
    del A

    return L, Y


def calculate_FR_matrix(year):
    """
    Calculates the FR matrix (sector share of final consumption expenditure).
    
    The FR matrix represents each sector's share of Final Consumption Expenditure 
    (FCE) per geographical scope.
    
    Args:
        year (int): Year for which to calculate the FR matrix.
        
    Returns:
        np.ndarray: FR matrix with shape (num_sectors, num_geo).
    """
    L, Y = load_matrices(year)
    
    geo = EXIOBASE_GEO_SCOPES
    num_geo = len(geo)
    num_sectors = len(L)

    # Step 1: Calculate total final consumption expenditure per geographical scope
    FCE_tot_dict = {} 
    for geo_scope in geo:
        Y_geo_scope = Y[geo_scope]
        FCE_geo_scope = Y_geo_scope.iloc[:, :3].sum().sum()
        FCE_tot_dict[geo_scope] = FCE_geo_scope

    print("Final Consumption Expenditure per geographical scope calculated!")

    # Step 2: Calculate FCE for each sector within each geographical scope (j)
    FCE_j_dict = {}

    for geo_scope in geo:
        for i in range(len(Y)):
            Y_row = Y.iloc[[i]][[geo_scope, "region", "sector"]]
            Y_row.columns = ['_'.join(col) for col in Y_row.columns]

            joint_string_1 = f"{geo_scope}_Final consumption expenditure by households"
            joint_string_2 = (
                f"{geo_scope}_Final consumption expenditure by non-profit "
                "organisations serving households (NPISH)"
            )
            joint_string_3 = f"{geo_scope}_Final consumption expenditure by government"

            Y_filter_FCE = Y_row[[joint_string_1, joint_string_2, joint_string_3]]
            FCE_j = Y_filter_FCE.iloc[0].sum()

            geoscope = Y_row.at[i, 'region_']
            sector = Y_row.at[i, 'sector_']
            reg_sec = (geo_scope, geoscope, sector)

            FCE_j_dict[reg_sec] = FCE_j

    print("Final Consumption Expenditure per sector within geographical scope calculated!")

    # Step 3: Compute FRj,r matrix (sector share of FCE per geographical scope)
    relative_FCE_dict = {}
    for target_geo_scope in geo:
        total_FCE = FCE_tot_dict[target_geo_scope]
        values_with_metadata = [
            (geoscope, sector, value) 
            for (geo_scope, geoscope, sector), value in FCE_j_dict.items() 
            if geo_scope == target_geo_scope
        ]
        rel_FCE_with_metadata = [
            (geoscope, sector, value / total_FCE) 
            for geoscope, sector, value in values_with_metadata
        ]
        relative_FCE_dict[target_geo_scope] = rel_FCE_with_metadata

    # Create MultiIndex dataframe for FR matrix
    unique_geoscopes_sectors = set()
    for data in relative_FCE_dict.values():
        for geoscope, sector, _ in data:
            unique_geoscopes_sectors.add((geoscope, sector))

    unique_geoscopes_sectors = sorted(list(unique_geoscopes_sectors))

    df = pd.DataFrame(
        index=pd.MultiIndex.from_tuples(
            unique_geoscopes_sectors, 
            names=["geoscope", "Sector"]
        )
    )

    for geo_scope, data in relative_FCE_dict.items():
        geo_scope_data = {
            (geoscope, sector): rel_FCE 
            for geoscope, sector, rel_FCE in data
        }
        df[geo_scope] = pd.Series(geo_scope_data)

    # Convert to matrix and check shape    
    FR_matrix = (
        df.transpose()
        .rename(columns=lambda col: '_'.join(col))
        .sort_index()
        .transpose()
        .sort_index()
        .to_numpy()
    )

    assert FR_matrix.shape == (num_sectors, num_geo), "FR_matrix shape mismatch!"

    # Delete not further needed variables to liberate storage
    del FCE_j_dict, Y

    return FR_matrix


def calculate_direct_FCE_allocation_factors(year):
    """
    Calculates direct FCE allocation factors.
    
    This is a placeholder function for calculating allocation factors based on 
    direct Final Consumption Expenditure.
    
    Args:
        year (int): Year for which to calculate allocation factors.
        
    Returns:
        None: Implementation pending.
    """
    # TODO: Implement this function based on specific requirements
    pass
