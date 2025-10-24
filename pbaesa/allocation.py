"""
Allocation factor retrieval and calculation for planetary boundaries.
"""

import pandas as pd
import glob
import os
import numpy as np
import copy
import pymrio as p
from pathlib import Path


def get_direct_FCE_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=None):
    """
    Get allocation factors based on direct FCE for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        af_direct_fce: Allocation factor based on direct FCE
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=exiobase_storage_path)
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


def get_total_FCE_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=None):
    """
    Get allocation factors based on total FCE for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        af_total_fce: Allocation factor based on total FCE
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=exiobase_storage_path)
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


def get_direct_GVA_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=None):
    """
    Get allocation factors based on direct GVA for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        af_direct_gva: Allocation factor based on direct GVA
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=exiobase_storage_path)
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


def get_total_GVA_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=None):
    """
    Get allocation factors based on total GVA for a sector in a specific geographical 
    scope and for a specific year.

    Parameters:
        geographical_scope: str
        sector: str
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        ag_total_gva: Allocation factor based on total GVA
    """    
    filtered_df = get_all_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=exiobase_storage_path)
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

def download_exiobase_data(year, exiobase_storage_path=None):
    """
    Download exiobase industry-to-industry database for given year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        exio_downloadlog: Download-Log

    """ 
    if exiobase_storage_path is None:
        exio_storage_folder = Path.home() / ".pbaesa_data" / "exiobase"
    else:
        exio_storage_folder = Path(exiobase_storage_path)
    exio_storage_folder.mkdir(parents=True, exist_ok=True)
    exio_downloadlog = p.download_exiobase3(
        storage_folder=exio_storage_folder, system="ixi", years=[year]
    )
    return exio_downloadlog 

def load_matrices(year, return_L=True, return_Y=True, exiobase_storage_path=None):
    """
    Load Y matrix and calculate L matrix from exiobase.

    Parameters:
        year: int
        return_L: boolean
        return_Y: boolean
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        results: L and/or Y matrix

    """ 

    if exiobase_storage_path is None:
        exio_storage_folder = Path.home() / ".pbaesa_data" / "exiobase"
    else:
        exio_storage_folder = Path(exiobase_storage_path)
    exio_storage_folder.mkdir(parents=True, exist_ok=True)
    pattern = str(exio_storage_folder / f"IOT_{year}_*.zip")
    matching_files = glob.glob(pattern)

    if matching_files:
        exio_file_path = matching_files[0]
    else:
        download_exiobase_data(year, exiobase_storage_path)
        matching_files = glob.glob(pattern)
        if matching_files:
            exio_file_path = matching_files[0]
        else:
            print("Exiobase versions only exist from 1995 to 2022! Choose another")
    
    exio3 = p.parse_exiobase3(exio_file_path)

    #### Extract A-Matrix and Y-Matrix from Exiobase #### 
    A = exio3.A.copy() 
    Y = exio3.Y.copy()
    Y = Y.reset_index() 

    #### Calculate Leontief-Matrix L (c.f. Equation 2 of Oosterhoff et al.) ####
    L = p.calc_L(A)

    #### Delete not further needed variables to liberate storage ####
    del A

    results = []
    if return_L:
        results.append(L)
    if return_Y:
        results.append(Y)
    return results if len(results) > 1 else results[0]

def prepare_L_matrix(year, exiobase_storage_path=None):
    """
    Prepare L matrix by removing multi-index.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        L_sorted: datatframe

    """ 
    L = load_matrices(year, return_Y=False, exiobase_storage_path=exiobase_storage_path)

    # Prepare Leontief-matrix for further calculations
    L_c = copy.deepcopy(L)
    L_c.columns = ['_'.join(col) for col in L.columns]
    L_c.index = ['_'.join(idx) for idx in L.index]
    L_sorted = L_c.sort_index(axis=0).sort_index(axis=1)
    del L_c  

    return L_sorted

def get_index(year):
    """
    Get index for all matrices.

    Parameters:
        year: int

    Returns:
        save_index: index

    """ 
    L_sorted = prepare_L_matrix(year)
    save_index = L_sorted.index

    return save_index

def load_satellites(year, return_F=True, return_x=True, return_z = True, exiobase_storage_path=None):
    """
    Load data from satellite accounts.

    Parameters:
        year: int
        return_F: boolean
        return_x: boolean
        return_z: boolean
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        results: F, z, x

    """ 

    if exiobase_storage_path is None:
        exio_storage_folder = Path.home() / ".pbaesa_data" / "exiobase"
    else:
        exio_storage_folder = Path(exiobase_storage_path)
    exio_storage_folder.mkdir(parents=True, exist_ok=True)
    pattern = str(exio_storage_folder / f"IOT_{year}_*.zip")
    matching_files = glob.glob(pattern)

    if matching_files:
        exio_file_path = matching_files[0]
    else:
        download_exiobase_data(year, exiobase_storage_path)
        matching_files = glob.glob(pattern)
        if matching_files:
            exio_file_path = matching_files[0]
        else:
            print("Exiobase versions only exist from 1995 to 2022! Choose another")
    
    exio3 = p.parse_exiobase3(exio_file_path)

    F_satellite = exio3.factor_inputs.F.copy() #factor_inputs

    x_satellite = exio3.x.copy()

    z_satellite = exio3.Z.copy()

    results = []
    if return_F:
        results.append(F_satellite)
    if return_x:
        results.append(x_satellite)
    if return_z:
        results.append(z_satellite)
    return results if len(results) > 1 else results[0]

def define_scope(year, return_what='all', exiobase_storage_path=None):
    """
    Define geographical scope and sector information for a given year.

    Parameters
    ----------
    year : int or str
        Year of the dataset to load.
    return_what : str, optional
        Specify what to return. Options:
            - 'all' (default): returns (num_geo, num_sectors, geo)
            - 'num_geo': returns only the number of geographical regions
            - 'num_sectors': returns only the number of sectors
            - 'geo': returns only the list of geographical abbreviations
    exiobase_storage_path: str or Path, optional
        Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase
    """
    L = load_matrices(year, return_Y=False, exiobase_storage_path=exiobase_storage_path)

    # Define abbreviations used in Exiobase for all geographical scopes
    geo = [
        'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR',
        'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI',
        'SK', 'GB', 'US', 'JP', 'CN', 'CA', 'KR', 'BR', 'IN', 'MX', 'RU', 'AU', 'CH',
        'TR', 'TW', 'NO', 'ID', 'ZA', 'WA', 'WL', 'WE', 'WF', 'WM'
    ]

    num_geo = len(geo)
    num_sectors = len(L)

    # Handle return options
    if return_what == 'num_geo':
        return num_geo
    elif return_what == 'num_sectors':
        return num_sectors
    elif return_what == 'geo':
        return geo
    elif return_what == 'all':
        return num_geo, num_sectors, geo
    else:
        raise ValueError(f"Invalid return_what value: {return_what}. Choose from 'all', 'num_geo', 'num_sectors', 'geo'.")
    

def calculate_FR_matrix(year, exiobase_storage_path=None):
    """
    Calculate FR matrix.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        FR_matrix: dataframe

    """ 
    
    Y = load_matrices(year, return_L=False, exiobase_storage_path=exiobase_storage_path)

    num_geo, num_sectors, geo = define_scope(year, return_what="all", exiobase_storage_path=exiobase_storage_path)

    
    #### Calculation of Equation 1 ####
    
    # Step 1: Calculate total final consumption expenditure per geographical scope
    FCE_tot_dict = {} 
    for geo_scope in geo:
        Y_geo_scope = Y[geo_scope]
        FCE_geo_scope = Y_geo_scope.iloc[:, :3].sum().sum()
        FCE_tot_dict[geo_scope] = FCE_geo_scope

    print("Final Consumption Expenditure per geographical scope calculated!")

    # Step 2: Calculate final consumption expenditure for each sector within each geographical scope (j)
    FCE_j_dict = {}

    for geo_scope in geo:
        for i in range(len(Y)):
            Y_row = Y.iloc[[i]][[geo_scope, "region", "sector"]]
            Y_row.columns = ['_'.join(col) for col in Y_row.columns]

            joint_string_1 = f"{geo_scope}_Final consumption expenditure by households"
            joint_string_2 = f"{geo_scope}_Final consumption expenditure by non-profit organisations serving households (NPISH)"
            joint_string_3 = f"{geo_scope}_Final consumption expenditure by government"

            Y_filter_FCE = Y_row[[joint_string_1, joint_string_2, joint_string_3]]
            FCE_j = Y_filter_FCE.iloc[0].sum()

            geoscope = Y_row.at[i, 'region_']
            sector = Y_row.at[i, 'sector_']
            reg_sec = (geo_scope, geoscope, sector)

            FCE_j_dict[reg_sec] = FCE_j

    print("Final Consumption Expenditure per sector within geographical scope calculated!")

    # Step 3: Compute FRj,r matrix (sector in geographical scope share of FCE per geographical scope)
    relative_FCE_dict = {}
    for target_geo_scope in geo:
        total_FCE = FCE_tot_dict[target_geo_scope]
        values_with_metadata = [(geoscope, sector, value) for (geo_scope, geoscope, sector), value in FCE_j_dict.items() if geo_scope == target_geo_scope]
        rel_FCE_with_metadata = [(geoscope, sector, value / total_FCE) for geoscope, sector, value in values_with_metadata]
        relative_FCE_dict[target_geo_scope] = rel_FCE_with_metadata

    # Create MultiIndex dataframe for FR matrix
    unique_geoscopes_sectors = set()
    for data in relative_FCE_dict.values():
        for geoscope, sector, _ in data:
            unique_geoscopes_sectors.add((geoscope, sector))

    unique_geoscopes_sectors = sorted(list(unique_geoscopes_sectors))

    df = pd.DataFrame(index=pd.MultiIndex.from_tuples(unique_geoscopes_sectors, names=["geoscope", "Sector"]))

    for geo_scope, data in relative_FCE_dict.items():
        geo_scope_data = { (geoscope, sector): rel_FCE for geoscope, sector, rel_FCE in data }
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

def get_population_weights():
    """
    Get population weights based on a geographical scopes share of global population.

    Returns:
        sPOPr_dict: dict

    """ 
    sPOPr_dict = {
        "AT": 0.001137112, "BE": 0.001469619, "BG": 0.000813057, "CY": 0.000157388,
        "CZ": 0.001342135, "DE": 0.010538512, "DK": 0.000742371, "EE": 0.000169631,
        "ES": 0.006008648, "FI": 0.000698741, "FR": 0.008548135, "GR": 0.001311299,
        "HR": 0.000484889, "HU": 0.001212719, "IE": 0.000644798, "IT": 0.007412402,
        "LT": 0.00035611,  "LU": 8.21348E-05,  "LV": 0.000236353, "MT": 6.67933E-05,
        "NL": 0.002226092, "PL": 0.004630737, "PT": 0.001309134, "RO": 0.002395369,
        "SE": 0.001318847, "SI": 0.000265605, "SK": 0.000683102, "GB": 0.008525459,
        "US": 0.041912521, "JP": 0.015735834, "CN": 0.177596435, "CA": 0.004897012,
        "KR": 0.00649839,  "BR": 0.027078025, "IN": 0.17822501,  "MX": 0.016035037,
        "RU": 0.01813937,  "AU": 0.003271595, "CH": 0.001103648, "TR": 0.010687152,
        "TW": 0.003004855, "NO": 0.000686293, "ID": 0.034647303, "ZA": 0.00753231,
        "WA": 0.121196918797013, "WL": 0.039809986, "WE": 0.0204874844768778, "WF": 0.144929024082053,
        "WM": 0.0618275302286748
    } #Dictionary that includes shares of global population by geographical scope for the year 2022

    return sPOPr_dict

def calculate_population_weights():
    """
    Calculate population weights based on a geographical scopes share of global population.

    Returns:
        sPOPr: array

    """ 
    sPOPr_dict = get_population_weights()

    sorted_geo = sorted(sPOPr_dict.keys())
    sPOPr = np.squeeze(np.array([sPOPr_dict[geo_scope] for geo_scope in sorted_geo]))

    return sPOPr

def calculate_direct_FCE_allocation_factor(year, exiobase_storage_path=None):
    """
    Calculate allocation factors based on direct FCE for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        direct_FCE_pop_df: A dataframe including the allocation factors based on direct FCE for a specified year.

    """   
    save_index = get_index(year)
    FR_matrix = calculate_FR_matrix(year, exiobase_storage_path=exiobase_storage_path)
    sPOPr = calculate_population_weights()
    direct_FCE_pop = (FR_matrix * sPOPr).sum(axis=1)
    direct_FCE_pop_df = pd.DataFrame(direct_FCE_pop, columns=["direct_FCE"])
    direct_FCE_pop_df.index = save_index
    
    return direct_FCE_pop_df

def calculate_total_FCE_allocation_factor(year, exiobase_storage_path=None):
    """
    Calculate allocation factors based on total FCE for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        total_FCE_df: A dataframe including the allocation factors based on total FCE for a specified year.

    """ 
    save_index = get_index(year)
    
    FR_matrix = calculate_FR_matrix(year, exiobase_storage_path=exiobase_storage_path)
    L = load_matrices(year, return_Y=False, exiobase_storage_path=exiobase_storage_path)
    num_geo, num_sectors, geo = define_scope(year, exiobase_storage_path=exiobase_storage_path)
    sPOPr = calculate_population_weights()

    #### Calculation of Equation 3 ####
    L_T = np.transpose(L)
    e = np.ones((len(L_T), 1))
    S_roof_pre = np.dot(L_T, e)
    I = np.identity(len(L_T))
    S_roof = np.multiply(S_roof_pre, I)

    #### Calculation of Equation 5 ####
    L_diag = np.multiply(L, I)
    L_dif = L - L_diag
    L_dif_T = np.transpose(L_dif)
    f_top = np.dot(L_dif_T, e)
    f_bottom = np.dot(L_diag, e)
    f = f_top / f_bottom

    #### Calculation of Equation 4 ####
    e_T = np.transpose(e)
    f_scalar = np.dot(f, e_T)
    L_f = np.multiply(L, f_scalar)
    S_tilde = L + L_f

    #### Calculation of Equation 6 ####
    S = S_roof + S_tilde

    #### Calculation of Equation 7 ####
    S_roof_div = np.linalg.inv(S_roof) 
    S_marginal = np.matmul(S,S_roof_div)
    S_marginal_T = S_marginal.transpose()
    S_marginal_T.columns = ['_'.join(col) for col in S_marginal_T.columns]
    S_marginal_T.index = S_marginal_T.columns
    S_marginal_T = S_marginal_T.sort_index()
    S_marginal = S_marginal_T.transpose()
    S_marginal = S_marginal.sort_index() 
    save_index = S_marginal.index
    S_marginal = S_marginal.to_numpy()

    aSoSOS_j_i_r = np.zeros((num_sectors, num_sectors, num_geo))

    for r in range(num_geo):
        FR_vector = FR_matrix[:, r].reshape((num_sectors, 1))
        aSoSOS_j_i_r[:, :, r] = S_marginal * FR_vector

    #### Calculation of Equation 8 ####
    aSoSOS_j_r = aSoSOS_j_i_r.sum(axis=1) # aSoSOS_j_r is total share assigned to sector j based on the overall final demand for sector i in geographical scope r ###########

    aSoSOS_j = (aSoSOS_j_r * sPOPr).sum(axis=1)
    total_FCE_df = pd.DataFrame(aSoSOS_j, columns=["Allocation factor calculated via total final consumption expenditure"])
    total_FCE_df.index = save_index

    # Delete not further needed variables to liberate storage
    del L_T, L_diag, L_dif, L_dif_T, L_f, S_tilde, f_scalar, I, S_roof_div, S_roof, S_marginal_T, S, S_marginal, aSoSOS_j_i_r

    return total_FCE_df

def calculate_GVA_per_sector(year, exiobase_storage_path=None):
    """
    Calculate GVA per sector for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        V_df: A dataframe including the GVA per sector for a specific year.

    """ 
    value_added = load_satellites(year, return_x = False, return_z=False, exiobase_storage_path=exiobase_storage_path)

  

    #### Calculation of direct gross value added of each sector in each geographical scope (j) ####

    # Step 1: Extract value-added satellite data from Exiobase
    value_added.columns = ['_'.join(col) for col in value_added.columns]
    value_added = value_added.transpose().sort_index()

    # Step 2: Define relevant GVA components
    gva_components = [
        "Other net taxes on production",
        "Compensation of employees; wages, salaries, & employers' social contributions: Low-skilled",
        "Compensation of employees; wages, salaries, & employers' social contributions: Medium-skilled",
        "Compensation of employees; wages, salaries, & employers' social contributions: High-skilled",
        "Operating surplus: Consumption of fixed capital",
        "Operating surplus: Remaining net operating surplus"
    ]

    # Step 3: Sum the selected value-added components across sectors
    V_df = value_added.filter(gva_components).sum(axis=1)
    

    # Delete not further needed variables to liberate storage
    del value_added

    return V_df

def calculate_direct_GVA_per_sector(year, exiobase_storage_path=None):
    """
    Calculate direct GVA per sector for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        GVA_df_geo: A dataframe including the direct GVA per sector for a specific year.

    """ 
    value_added = load_satellites(year, return_x = False, return_z=False, exiobase_storage_path=exiobase_storage_path)

    # Step 1: Extract value-added satellite data from Exiobase
    value_added.columns = ['_'.join(col) for col in value_added.columns]
    value_added = value_added.transpose().sort_index()

    gva_components = [
        "Other net taxes on production",
        "Compensation of employees; wages, salaries, & employers' social contributions: Low-skilled",
        "Compensation of employees; wages, salaries, & employers' social contributions: Medium-skilled",
        "Compensation of employees; wages, salaries, & employers' social contributions: High-skilled",
        "Operating surplus: Consumption of fixed capital",
        "Operating surplus: Remaining net operating surplus"
    ]

    #### Calculation of gross value added per geographical scope ####
    GVA_geo = value_added.filter(gva_components).sum(axis=1)
    GVA_df_geo = pd.DataFrame(GVA_geo)
    GVA_df_geo['geo_scope'] = GVA_df_geo.index.to_series().str.extract(r'^([A-Z]{2})_')

    return GVA_df_geo

def calculate_GVA_per_geographical_scope(year, exiobase_storage_path=None):
    """
    Calculate GVA per sector in geographical scope for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        full_GVA_per_geo: A dataframe including the GVA per sector in geographical scope for a specific year.

    """ 
    GVA_df_geo = calculate_direct_GVA_per_sector(year, exiobase_storage_path=exiobase_storage_path)

    full_GVA_per_geo = GVA_df_geo.groupby('geo_scope')[0].sum()

    return full_GVA_per_geo

def calculate_total_GVA_per_sector(year, exiobase_storage_path=None):
    """
    Calculate total GVA per sector in geographical scope for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        total_GVA_j: A dataframe including the total GVA per sector in geographical scope for a specific year.

    """ 

    V_df = calculate_GVA_per_sector(year, exiobase_storage_path=exiobase_storage_path)
    V = V_df.to_numpy()
    L_sorted = prepare_L_matrix(year, exiobase_storage_path=exiobase_storage_path)
    save_index = get_index(year)
    #### Calculation of type I GVA multiplier ####

    # Step 1: Extract total output from Exiobase
    x_df = load_satellites(year, return_F = False, return_z=False, exiobase_storage_path=exiobase_storage_path)
    x_df = x_df.transpose()
    x_df.columns = ['_'.join(col) for col in x_df.columns]
    x_df = x_df.transpose().sort_index()
    total_output_array = x_df.to_numpy()

    # Step 2: Combute the denominator of the multiplier
    with np.errstate(divide='ignore', invalid='ignore'):
        bottom_multiplier = np.divide(V, total_output_array)
        bottom_multiplier = np.nan_to_num(bottom_multiplier, nan=0.0, posinf=0.0, neginf=0.0)

    bottom_multiplier_df = pd.DataFrame(bottom_multiplier, index=save_index)

    del bottom_multiplier

    # Step 3: Combute the numerator of the multiplier and then the multiplier itself
    multiplier_j_list = []

    for j in range(len(L_sorted)):
        result = pd.DataFrame()
        result = L_sorted.iloc[:, j] * bottom_multiplier_df.iloc[:, 0]

        top_multiplier_j = result.sum()
        bottom_multiplier_j = bottom_multiplier_df.iloc[j, :]
        bottom_multiplier_j = bottom_multiplier_j.iloc[0]
        multiplier_j = np.divide(top_multiplier_j, bottom_multiplier_j, out=np.zeros_like(top_multiplier_j), where=bottom_multiplier_j != 0) 
        multiplier_j_list.append(multiplier_j)

    multiplier_j_df = pd.DataFrame(multiplier_j_list).transpose()
    multiplier_j_df.columns = L_sorted.columns

    #### Calculation of total GVA per sector in geographical scope ####
    V_vector_df = pd.DataFrame(V_df)
    total_GVA_j = multiplier_j_df.transpose() * V_vector_df

    # Delete not further needed variables to liberate storage
    del L_sorted, bottom_multiplier_df

    return total_GVA_j

def add_regional_resolution_to_total_GVA_of_sector(year, exiobase_storage_path=None):
    """
    Add regional resolution to total GVA per sector in geographical scope for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        total_GVA_per_geo_scope: dataframe

    """ 
    #### Compute total GVA of each sector in each geographical scope with regional resolution ####

    V_df = calculate_GVA_per_sector(year, exiobase_storage_path=exiobase_storage_path)

    total_GVA_j = calculate_total_GVA_per_sector(year, exiobase_storage_path=exiobase_storage_path)

    # Step 1: Extract inter-sectoral inputs from Exiobase 
    Input = load_satellites(year, return_F = False, return_x=False, exiobase_storage_path=exiobase_storage_path)
    Input.columns = ['_'.join(col) for col in Input.columns]
    Input.index = ['_'.join(idx) for idx in Input.index]

    # Step 2: Compute value added inputs
    VA = pd.DataFrame(V_df).transpose()
    VA.rename(index={0: 'primary'}, inplace=True)

    geoscopes = sorted(set(col.split('_')[0] for col in VA.columns))
    VA_per_geoscope = pd.DataFrame(index=[f"{geoscope}_primary" for geoscope in geoscopes], columns=VA.columns)
    for geoscope in geoscopes:
        row_name = f"{geoscope}_primary"
        VA_per_geoscope.loc[row_name] = [
            VA.loc['primary', col] if col.startswith(geoscope + '_') else 0
            for col in VA.columns
        ]
    VA_per_geoscope = VA_per_geoscope[Input.columns]

    # Step 3: Compute total input share per geographical scope
    Input = pd.concat([Input, VA_per_geoscope], axis=0)
    Input = Input.div(Input.sum(axis=0), axis=1)

    Input_per_geoscope = (
        Input.groupby(Input.index.str.split('_').str[0])  
            .sum()
            .sort_index()
            .T                                          
            .sort_index()
    )

    # Step 4: Multiply total GVA of each sector in each geographical scope with input shares per geographical scope to obtain regional resolution 
    total_GVA_per_geo_scope = Input_per_geoscope.multiply(total_GVA_j.iloc[:, 0], axis=0)

    # Delete not further needed variables to liberate storage
    del Input, VA_per_geoscope

    return total_GVA_per_geo_scope

def calculate_total_GVA_allocation_factor(year, exiobase_storage_path=None):
    """
    Calculate allocation factors based on total GVA for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        total_GVA_pop_df: A dataframe including the allocation factors based on total GVA for a specified year.

    """ 

    #### Calculate allocation factors based on total GVA ####
    full_GVA_per_geo = calculate_GVA_per_geographical_scope(year, exiobase_storage_path=exiobase_storage_path)
    total_GVA_per_geo_scope = add_regional_resolution_to_total_GVA_of_sector(year, exiobase_storage_path=exiobase_storage_path)
    save_index = get_index(year)
    sPOPr_dict = get_population_weights()

    # Step 1: Compute share of GVA in each geographical scope that originates from total GVA of each sector in each geographical scope
    share_total_GVA_per_geo_scope = total_GVA_per_geo_scope.divide(full_GVA_per_geo, axis=1)

    # Step 2: Multiply GVA shares with population shares to obtain allocation factors
    sPOPr_series = pd.Series(sPOPr_dict).sort_index()
    total_GVA_pop = share_total_GVA_per_geo_scope.mul(sPOPr_series, axis=1).sum(axis=1)
    total_GVA_pop_df = pd.DataFrame({'share_total_gva': total_GVA_pop}, index=save_index)

    return total_GVA_pop_df
    
def calculate_direct_GVA_allocation_factor(year, exiobase_storage_path=None):
    """
    Calculate allocation factors based on direct GVA for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        direct_GVA_pop_df: A dataframe including the allocation factors based on direct GVA for a specified year.

    """ 
    GVA_df_geo = calculate_direct_GVA_per_sector(year, exiobase_storage_path=exiobase_storage_path)
    full_GVA_per_geo = calculate_GVA_per_geographical_scope(year, exiobase_storage_path=exiobase_storage_path)
    save_index = get_index(year)
    sPOPr_dict = get_population_weights()
    sPOPr_series = pd.Series(sPOPr_dict).sort_index()
    ##### Calculate allocation factors based on total GVA ####

    # Step 1: Divide direct GVA of each sector in each geographical scope by full GVA of respective geographical scope
    GVA_df_geo['geo_scope'] = GVA_df_geo['geo_scope'].astype(str)
    GVA_df_geo['normalized_value'] = GVA_df_geo[0] / GVA_df_geo['geo_scope'].map(full_GVA_per_geo)

    # Step 2: Compute share of GVA in each geographical scope that originates from direct GVA of each sector in each geographical scope
    share_direct_GVA_per_geo_scope = GVA_df_geo.reset_index().pivot(
        index='index', 
        columns='geo_scope',
        values='normalized_value'
    ).fillna(0) 

    # Step 3: Multiply GVA shares with population shares to obtain allocation factors
    direct_GVA_pop = share_direct_GVA_per_geo_scope.mul(sPOPr_series, axis=1).sum(axis=1)
    direct_GVA_pop_df = pd.DataFrame({'share_direct_gva': direct_GVA_pop}, index=save_index)
    

    return direct_GVA_pop_df 

def calculate_all_allocation_factors(year, exiobase_storage_path=None):
    """
    Calculate all allocation factors based on direct,total FCE and direct, total GVA for a specific year.

    Parameters:
        year: int
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

    Returns:
        aSoSOS_j_df: A dataframe including the allocation factors based on direct,total FCE and direct, total GVA for a specific year.

    """ 
    direct_FCE_df = calculate_direct_FCE_allocation_factor(year, exiobase_storage_path=exiobase_storage_path)
    indirect_FCE_df = calculate_total_FCE_allocation_factor(year, exiobase_storage_path=exiobase_storage_path)
    total_GVA_df = calculate_total_GVA_allocation_factor(year, exiobase_storage_path=exiobase_storage_path)
    direct_GVA_df = calculate_direct_GVA_allocation_factor(year, exiobase_storage_path=exiobase_storage_path)

    aSoSOS_j_df = pd.DataFrame()
    aSoSOS_j_df["Allocation factor calculated via total final consumption expenditure"] = indirect_FCE_df["Allocation factor calculated via total final consumption expenditure"]
    aSoSOS_j_df['Allocation factor calculated via direct final consumption expenditure'] = direct_FCE_df['direct_FCE']
    aSoSOS_j_df['Allocation factor calculated via total gross value added'] = total_GVA_df['share_total_gva']
    aSoSOS_j_df['Allocation factor calculated via direct gross value added'] = direct_GVA_df['share_direct_gva']

    


    return aSoSOS_j_df   

def export_all_allocation_factors(year, exiobase_storage_path=None):
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
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase
        
    Returns:
        Excel-File with Allocation Factors
        
    """
    aSoSOS_j_df = calculate_all_allocation_factors(year, exiobase_storage_path=exiobase_storage_path)

    # Write to Excel-File that includes the allocation factors
    aSoSOS_j_df['Country (c.f. ISO 3166-1 alpha-2) & Rest of World regions'] = aSoSOS_j_df.index.str.split('_').str[0]
    aSoSOS_j_df['Sector (c.f. EU’s NACE Rev.1 classification)'] = aSoSOS_j_df.index.str.split('_').str[1]
     
    filename = f"Allocation Factors_{year}.xlsx"
    aSoSOS_j_df.to_excel(filename)

def get_all_allocation_factor(geographical_scope, sector, year, exiobase_storage_path=None):
    """
    Get all allocation factors for a sector in a specific geographical scope and for a specific year.
    
    If the allocation factors file does not exist, this function will attempt to download/calculate it
    automatically by calling export_all_allocation_factors.

    Parameters:
        geographical_scope: str - ISO 3166-1 alpha-2 country code or Rest of World region
        sector: str - Sector name according to EU's NACE Rev.1 classification
        year: int - Year for which to retrieve allocation factors
        exiobase_storage_path: str or Path, optional
            Custom path for storing exiobase data. If None, defaults to ~/.pbaesa_data/exiobase

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
            export_all_allocation_factors(year, exiobase_storage_path=exiobase_storage_path)
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
    sector_col = "Sector (c.f. EU’s NACE Rev.1 classification)"

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