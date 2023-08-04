#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:38:47 2023

@author: kristianfoerster
"""

import numpy as np



def bagrov(n, step=0.0001,PEmax=4):
    """
    Original Bagrov (1953) equation in dimensionless form to compute real
    evapotranspiration ETR

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
        1D numpy array that contains ascending values of P/ETmax.
    TYPE
        1D numpy array that contains ascending values of ETR/ETmax.

    """
    nEis = np.arange(0,1,step)
    nPEis = np.cumsum(step / (1 - nEis**n))

    return nPEis[nPEis<PEmax],nEis[nPEis<PEmax]
