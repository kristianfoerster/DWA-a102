# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 10:12:05 2021

@author: Edi
"""

param_rages = {
    'P': [500, 1700, 'Precipitation', 'mm/a'], 
    'ETp' :[450, 700, 'Evapotranspiration'], 
    'Sp_steep_roof': [0.1, 0.6, 'Storage height', 'mm/a'],
    'Sp_flat_roof': [0.6, 3, 'Storage height', 'mm'],
    'h_green_roof': [40, 500, 'Installation height', 'mm'],
    'kf_green_roof': [18, 100, 'Hydraulic conductivity', 'mm/h'],
    'WKmax_WP_green_roof': [0.35, 0.65, 'Difference (WKmax - WP)', ''],
    'Sp_storage_roof': [3, 10, 'Storage height', 'mm'],
    'FA_permeable_surface': [2, 10, 'Joint ratio'],
    'Sp_permeable_surface': [0.1, 2, 'Storage height', 'mm'],
    'WKmax_WP_permeable_surface': [0.1, 0.2, 'Difference (WKmax - WP)'],
    'kf_permeable_surface': [6, 100, 'Hydraulic conductivity', 'mm/h'],
    'Sp_porous_surface': [2.5, 4.2, 'Storage height', 'mm'],
    'h_porous_surface': [50, 100, 'Installation height', 'mm'],
    'kf_porous_surface': [10, 180, 'Hydraulic conductivity', 'mm/h'],
    'FA_paver_stonegrid': [20, 30, 'Joint ratio'],
    'Sp_paver_stonegrid': [0.1, 2, 'Storage height', 'mm'],
    'WKmax_WP_paver_stonegrid': [0.1, 0.2, 'Difference (WKmax - WP)'],
    'h_gravel_cover': [50, 100, 'Installation height', 'mm'],
    'Sp_gravel_cover': [2.5, 4.2, 'Storage height', 'mm'],
    'kf_gravel_cover': [0.72, 10, 'Hydraulic conductivity', 'mm/h'],
    'kf_surf_infiltration': [325, 1100, 'Hydraulic conductivity', 'mm/h'],
    'kf_infilt_swale': [14, 3600, 'Hydraulic conductivity', 'mm/h'],
    'kf_swale_trench': [3.6, 36, 'Hydraulic conductivity', 'mm/h'],
    'qDr_swale_trench_system': [1, 10, 'throttled discharge yield'],
    'kf_swale_trench_system': [0.36, 3.6, 'Hydraulic conductivity', 'mm/h'],
    'VSp_rainwater_usage': [10, 200, 'Hydraulic conductivity', 'mm'],
    'VBr_rainwater_usage': [0, 5, 'Available water volume', 'mm/d'],
    'FAbw_rainwater_usage': [0, 5, 'Proportion of irrigated area', ''],
    'qBw_rainwater_usage': [0, 200, 'Specific annual requirement for irrigation', 'l/(m^2*year)'],
    'a_1_pod_system': [0.0, 1.0, 'Proportion of area 1 (a_1)', ''],
    'a_2_pod_system': [0.0, 1.0, 'Proportion of area 2 (a_2)', ''],
    'a_3_pod_system': [0.0, 1.0, 'Proportion of area 3 (a_3)', ''],
    'a_4_pod_system': [0.0, 1.0, 'Proportion of area 4 (a_4)', ''],
    }


def validRange(val, param):
    ''' generic function to check parameter range'''
    
    if ( (val < param_rages[param][0]) or (val > param_rages[param][1]) ): 
        raise Exception(f'{param_rages[param][2]} is not valid. Valid range:{param_rages[param][0]} - {param_rages[param][1]} {param_rages[param][3]}')