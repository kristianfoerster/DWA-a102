# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 10:12:05 2021

@author: Edwin Echeverri Salazar
"""

param_ranges = {
    'P': [500, 1700, 'Precipitation', 'mm/a'], 
    'ETp' :[450, 700, 'Evapotranspiration', 'mm/a'], 
    'Sp_roof': [0.1, 0.6, 'Storage height (sp)', 'mm/a'],
    'Sp_flat_area': [0.6, 3, 'Storage height (sp)', 'mm'],
    'h_green_roof': [40, 500, 'Installation height (h)', 'mm'],
    'fg_green_roof': [1., 1.4, 'Greening factor', '-'],
    'AWC_green_roof': [0.3, 0.8, 'Difference (wkmax_wp)', ''],
    'Sp_storage_roof': [3, 10, 'Storage height (sp)', 'mm'],
    'FA_permeable_surface': [2, 10, 'Joint ratio (fa)'],
    'Sp_permeable_surface': [0.1, 2, 'Storage height (sp)', 'mm'],
    'WKmax_WP_permeable_surface': [0.1, 0.2, 'Difference (wkmax_wp)'],
    'kf_permeable_surface': [6, 100, 'Hydraulic conductivity (kf)', 'mm/h'],
    'Sp_porous_surface': [2.5, 4.2, 'Storage height (sp)', 'mm'],
    'h_porous_surface': [50, 100, 'Installation height (h)', 'mm'],
    'kf_porous_surface': [10, 180, 'Hydraulic conductivity (kf)', 'mm/h'],
    'FA_paver_stonegrid': [20, 30, 'Joint ratio (fa)'],
    'Sp_paver_stonegrid': [0.1, 2, 'Storage height (sp)', 'mm'],
    'WKmax_WP_paver_stonegrid': [0.1, 0.2, 'Difference (wkmax_wp)'],
    'h_gravel_cover': [50, 100, 'Installation height (h)', 'mm'],
    'Sp_gravel_cover': [2.5, 4.2, 'Storage height (sp)', 'mm'],
    'kf_gravel_cover': [0.72, 10, 'Hydraulic conductivity (kf)', 'mm/h'],
    'kf_surf_infiltration': [325, 1100, 'Hydraulic conductivity (kf)', 'mm/h'],
    'kf_infilt_swale': [14, 3600, 'Hydraulic conductivity (kf)', 'mm/h'],
    'kf_swale_trench': [3.6, 36, 'Hydraulic conductivity (kf)', 'mm/h'],
    'qDr_swale_trench_system': [1, 10, 'Throttled discharge yield (qdr)'],
    'kf_swale_trench_system': [0.36, 3.6, 'Hydraulic conductivity (kf)', 'mm/h'],
    'VSp_rainwater_usage': [10, 200, 'Specific storage volume (vsp)', 'mm'],
    'VBr_rainwater_usage': [0, 5, 'Available water volume (vbr)', 'mm/d'],
    'FAbw_rainwater_usage': [0, 5, 'Proportion of irrigated area (fabw)', ''],
    'qBw_rainwater_usage': [0, 200, 'Specific annual requirement for irrigation (qbw)', 'l/(m^2*year)'],
    }


def validRange(val, param):
    ''' generic function to check parameter range'''
    
    if ( (val < param_ranges[param][0]) or (val > param_ranges[param][1]) ): 
        raise Exception(f"{param_ranges[param][2]} is not valid."
                        f" Acceptable range: {param_ranges[param][0]} - {param_ranges[param][1]}"
                        f" {param_ranges[param][3]}")