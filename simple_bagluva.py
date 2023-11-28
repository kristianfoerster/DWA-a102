#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:38:47 2023

@author: kristianfoerster
"""

import numpy as np



def bagrov(n, step=0.0001,PEmax=4):
    """
    Numerical solution of Bagrov's (1953) differential equation in 
    dimensionless form to compute real evapotranspiration ETR

    Parameters
    ----------
    n : float
        Land-use dependent parameter n
    step : float, optional
        Interval length used to construct the curve. The default is 0.0001.
    PEmax : float, optional
        The maximum ratio corrected precipitation P divided by maximum
        evapotranspiration ETmax used as upper bound for calculations. The  
        default is 4.

    Returns
    -------
    TYPE
        1D numpy array that contains ascending values of P/ETmax (x).
    TYPE
        1D numpy array that contains ascending values of ETR/ETmax (y).

    """
    nEis = np.arange(0,1,step)
    nPEis = np.cumsum(step / (1 - nEis**n))

    return nPEis[nPEis<PEmax],nEis[nPEis<PEmax]

def direct_runoff_ratio(soil,slope,gwd,land):
    """
    Function that yields direct runoff fraction (DWA-M102-4)

    Parameters
    ----------
    soil : int
        Soil type class (1 is a soil with high conductivity like sand, while
                         5 would be a highly cohesive soil with low
                         conductivity like clay)
    slope : float
        Slope in percent
    gwd : float
        Vertical distance to mean ground water table below surface (m)
    land : string
        Land surface class, either 'open' or 'forest'

    Returns
    -------
    result : float
        Fraction runoff that is direct runoff

    """
    
    result = -1

    if gwd < 1: gw = 0
    else: gw = 1
    
    if soil <= 2: soil_class=2
    elif soil <= 4: soil_class=4
    else: soil_class=5
    
    if slope<2: slope_class = 0
    elif slope < 4: slope_class = 2
    elif slope < 10: slope_class = 4
    else: slope_class = 10
    if gw == 0 and land=='open':
    	if soil_class == 2 and slope_class == 0:
    		result = 0.5
    	if soil_class == 2 and slope_class == 2:
    		result = 0.5
    	if soil_class == 2 and slope_class == 4:
    		result = 0.8
    	if soil_class == 2 and slope_class == 10:
    		result = 0.8
    	if soil_class == 4 and slope_class == 0:
    		result = 0.5
    	if soil_class == 4 and slope_class == 2:
    		result = 0.6
    	if soil_class == 4 and slope_class == 4:
    		result = 0.8
    	if soil_class == 4 and slope_class == 10:
    		result = 1.0
    	if soil_class == 5 and slope_class == 0:
    		result = 0.7
    	if soil_class == 5 and slope_class == 2:
    		result = 0.75
    	if soil_class == 5 and slope_class == 4:
    		result = 0.85
    	if soil_class == 5 and slope_class == 10:
    		result = 1.0
    if gw == 0 and land=='forest':
    	if soil_class == 2 and slope_class == 0:
    		result = 0.2
    	if soil_class == 2 and slope_class == 2:
    		result = 0.2
    	if soil_class == 2 and slope_class == 4:
    		result = 0.5
    	if soil_class == 2 and slope_class == 10:
    		result = 0.5
    	if soil_class == 4 and slope_class == 0:
    		result = 0.3
    	if soil_class == 4 and slope_class == 2:
    		result = 0.45
    	if soil_class == 4 and slope_class == 4:
    		result = 0.55
    	if soil_class == 4 and slope_class == 10:
    		result = 0.95
    	if soil_class == 5 and slope_class == 0:
    		result = 0.5
    	if soil_class == 5 and slope_class == 2:
    		result = 0.55
    	if soil_class == 5 and slope_class == 4:
    		result = 0.65
    	if soil_class == 5 and slope_class == 10:
    		result = 0.95
    if gw == 1 and land=='open':
    	if soil_class == 2 and slope_class == 0:
    		result = 0.0
    	if soil_class == 2 and slope_class == 2:
    		result = 0.15
    	if soil_class == 2 and slope_class == 4:
    		result = 0.4
    	if soil_class == 2 and slope_class == 10:
    		result = 0.65
    	if soil_class == 4 and slope_class == 0:
    		result = 0.2
    	if soil_class == 4 and slope_class == 2:
    		result = 0.55
    	if soil_class == 4 and slope_class == 4:
    		result = 0.7
    	if soil_class == 4 and slope_class == 10:
    		result = 1.0
    	if soil_class == 5 and slope_class == 0:
    		result = 0.65
    	if soil_class == 5 and slope_class == 2:
    		result = 0.7
    	if soil_class == 5 and slope_class == 4:
    		result = 0.8
    	if soil_class == 5 and slope_class == 10:
    		result = 1.0
    if gw == 1 and land=='forest':
    	if soil_class == 2 and slope_class == 0:
    		result = 0.0
    	if soil_class == 2 and slope_class == 2:
    		result = 0.05
    	if soil_class == 2 and slope_class == 4:
    		result = 0.35
    	if soil_class == 2 and slope_class == 10:
    		result = 0.45
    	if soil_class == 4 and slope_class == 0:
    		result = 0.05
    	if soil_class == 4 and slope_class == 2:
    		result = 0.42
    	if soil_class == 4 and slope_class == 4:
    		result = 0.57
    	if soil_class == 4 and slope_class == 10:
    		result = 0.9
    	if soil_class == 5 and slope_class == 0:
    		result = 0.4
    	if soil_class == 5 and slope_class == 2:
    		result = 0.45
    	if soil_class == 5 and slope_class == 4:
    		result = 0.6
    	if soil_class == 5 and slope_class == 10:
    		result = 0.9
    return result