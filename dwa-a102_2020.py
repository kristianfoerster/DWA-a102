# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:05:35 2020
Following new DWA-102 (Dec. 2020)

@author: Edwin Echeverri
"""
# install git
# conda install pip
# pip install git+https://github.com/woodcrafty/PyETo#egg=PyETo
import numpy as np
import pandas as pd
import pyeto as pyeto
from check_ranges import validRange
from pyeto import thornthwaite, monthly_mean_daylight_hours, deg2rad


#%% Berechnungsansatz B.3.1: Steildach (alle Deckungsmaterialien),
#### Flachdach (Metall, Glas)  
def steep_roof(Area, P, ETp, Sp=0.3):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). Storage height (Sp) in roofs varies
    between 0.1 and 0.6 mm. Standard storage value for steep roof
    in general is 0.3 mm, in case of glass or metal cover use 0.6 mm
    '''  
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(Sp, 'Sp_steep_roof')  
    a = 0.9115 + 0.00007063*P - 0.000007498*ETp - 0.2063*np.log(Sp + 1)
    g = 0
    v = 1-a-g
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000    
    # pfractions = (a, g, v)
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
steep_roof(Area=1000, P=800, ETp=500)

mmdlh = pyeto.monthly_mean_daylight_hours(pyeto.deg2rad(52.38), 2014)
monthly_t = [3.1, 3.5, 5.0, 6.7, 9.3, 12.1, 14.3, 14.1, 11.8, 8.9, 5.5, 3.8]
ETP_Thornthwaite = sum(pyeto.thornthwaite(monthly_t, mmdlh))

steep_roof(Area=1000, P=800, ETp=ETP_Thornthwaite)

#%% Berechnungsansatz B.3.2: Flachdach (Dachpappe, Faserzement, Kies),
#### Asphalt, fugenloser Beton, Pflaster mit dichten Fugen  
def flat_roof(Area, P, ETp, Sp=1.0):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). Storage (Sp) in flat roofs varies between 0.6
    and 3 mm. Standard Sp-values are:
    Flat roof with rough cover = 1;
    Flat roof with gravel cover = 2;
    Flat roof with asphalt or jointless concrete cover = 2.5;
    Flat roof with plaster (tight joints) cover = 1.5
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(Sp, 'Sp_flat_roof') 
    
    a = 0.8658 + 0.0001659*P - 0.00009945*ETp - 0.1542*np.log(Sp + 1)
    g = 0
    v = 1-a-g
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000    
    # pfractions = (a, g, v)
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)
# Test
flat_roof(1000, 500, 450, 0.6)
flat_roof(1000, 550, 450, 0.6)
# sum(flat_roof(550, 450, 0.6))

#%% Berechnungsansatz B.3.3: Gründach
def green_roof(Area, P, ETp, h, kf=70, WKmax_WP=0.5):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). Heigth (h) corresponds to the 
    installation heigth of the green roof (mm), kf stands for hydraulic
    conductivity (mm/h), WKmax corresponds to maximal water capacity (-)
    and WP to wilting point (-). Standard value for the difference 
    (WKmax - WP) is 0.5
    '''
    
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(h, 'h_green_roof')
    validRange(kf, 'kf_green_roof')
    validRange(WKmax_WP, 'WKmax_WP_green_roof')
    
    a = (-2.182 + 0.4293*np.log(P) - 0.0001092*P + (236.1/ETp) + 0.0001142*h
         + 0.0002297*kf + 0.01628*np.log(WKmax_WP)
         - 0.1214*np.log(WKmax_WP*h))
    g = 0
    v = 1-a-g
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
green_roof(Area= 1000, P=550, ETp=450, h=100)

#%% Berechnungsansatz B.3.4: Einstaudach (Speicherhöhe > 3mm)
def storage_roof(Area, P, ETp, Sp=5):
    ''' Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). Sp stands for storage heigth (Sp),
    which should be bigger than 3 mm and lower than 10 mm.
    Standard value for Sp = 5.
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(Sp, 'Sp_storage_roof') 
    
    a = 0.9231 + 0.000254*P - 0.0003226*ETp - 0.1472*np.log(Sp+1)
    g = 0
    v = 1-a-g
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
storage_roof(Area=1000, P=550, ETp=450)

#%% Berechnungsansatz B.3.5 & B.3.6: Teildurchlässige Flächenbeläge
### (Fugenanteil 2 % bis 10 %)
# Partially permeable surfaces (Joint ratio 2 % to 10 %)
def permeable_surface(Area, P, ETp, FA, kf, Sp=1, WKmax_WP=0.15):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). FA corresponds to the joint ratio of
    the pavers or partially permable elements. The standard storage
    heigth (Sp) is 1 mm for FA = 4, or FA = 8. WKmax corresponds to 
    maximal water capacity (-) and WP to wilting point (-).
    Standard value for difference (WKmax - WP) is 0.15. kf stands for
    hydraulic conductivity (mm/h), standard values are 18 mm/h,
    and 36 mm/h for FA = 4, and FA = 8, repectively.    
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(FA, 'FA_permeable_surface')
    validRange(kf, 'kf_permeable_surface')
    validRange(Sp, 'Sp_permeable_surface')
    validRange(WKmax_WP, 'WKmax_WP_permeable_surface')
    
### Berechnungsansatz B.3.5: Teildurchlässige Flächenbeläge
### (Fugenanteil 2 % bis 5 %)
# Partially permeable surfaces (Joint ratio 2 % to 5 %)   
    if (FA >= 2 and FA <= 5):
        a = (0.0800734*np.log(P) - 0.0582828*FA - 0.0501693*Sp
             - 0.385767*WKmax_WP + (8.7040284/(11.9086896+kf)))
        # DWA-a-102 2020 equation:
        # g = (-0.2006 - 0.000253*ETp + 0.05615*FA - 0.0636*np.log(1 + Sp)
        #      + 0.1596*np.log(1 + kf) + 0.2778*(WKmax - WP))
        v = (0.8529 - 0.1248*np.log(P) + 0.00005057*ETp + 0.002372*FA
             + 0.1583*np.log(1 + Sp))
        # To fullfill the conservation mass (a+g+v=1). My decision is to apply:
        g = 1-a-v

### Berechnungsansatz B.3.6: Teildurchlässige Flächenbeläge
### (Fugenanteil 6 % bis 10 %)
# Partially permeable surfaces (Joint ratio 6 % to 10 %)
# This funtion can be joint with the previous one and add the param "slope"     
    if (FA >= 6 and FA <= 10):
        a = (0.05912*np.log(P) - 0.02749*FA - 0.03671*Sp
             - 0.30514*WKmax_WP + (4.97687/(4.7975 + kf)))
        # DWA-a-102 2020 equation:
        # g = (0.00004941*P - 0.0002817*ETp + 0.02566*FA - 0.03823*Sp
        #      + 0.691*np.exp(-6.465/kf))
        v = (0.9012 - 0.1325*np.log(P) + 0.00006661*ETp + 0.002302*FA
             + 0.1489*np.log(1 + Sp))
        g = 1 - (a + v)

    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)
    
# Test
permeable_surface(Area=1000, P=650, ETp=500, FA=8, kf=36)
permeable_surface(1000, 650, 500, 4, 18)  

#%% Berechnungsansatz B.3.7: Teildurchlässige Flächenbeläge
### (Porensteine, Sickersteine), Kiesbelag, Schotterrasen
# Partially permeable surfaces
# (pore stones, seepage stones), gravel surface, gravel lawn
def porous_surface(Area, P, ETp, Sp=3.5, h=100, kf=180):
    ''' Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). Sp stands for storage heigth (mm),
    h stands for installation heigth (mm), kf corresponds to hydraulic
    conductivity (mm/h). Standard values are:
    Sp = 3.5 mm, h = 100 mm, kf = 180
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(Sp, 'Sp_porous_surface')
    validRange(h, 'h_porous_surface')
    validRange(kf, 'kf_porous_surface')

    a = (0.000001969*P - 0.005116*np.log(Sp) - 0.0001051*h
         + 0.01753*np.exp(4.576/kf))
    # g = (0.2468883*np.log(P) - 0.0003938*ETp + 0.0017083*Sp
    #      - 0.0015998*h - 0.6703502*np.exp(0.1122885/kf))
    v = (0.2111 - 0.2544*np.log(P) + 0.2073*np.log(ETp)
         + 0.0006249*Sp + 0.123*np.log(h) - 0.000002806*kf)
    g = max((1 - (a + v)), 0.0)
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
porous_surface(Area=1000, P=1000, ETp=650, Sp=4, h=100, kf=180)

#%% Berechnungsansatz B.3.8: Rasengittersteine
# Lawn grid stones / paver stone grids
def paver_stonegrid(Area, P, ETp, FA=25, Sp=1, WKmax_WP=0.15):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). FA corresponds to the joint ratio of
    the pavers or partially permable elements (FA standard value = 25).
    The standard storage heigth (Sp) is 1 mm. WKmax corresponds to the 
    maximal water capacity (-) and WP to wilting point (-). Standard value
    for the difference (WKmax - WP) is 0.15.
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(FA, 'FA_paver_stonegrid')
    validRange(Sp, 'Sp_paver_stonegrid')
    validRange(WKmax_WP, 'WKmax_WP_paver_stonegrid') 

    a = (0.145704 - 0.059177*np.log(FA) - 0.007354*Sp
         - 0.050531*np.log(WKmax_WP))
    # g = (- 0.02927 + 0.1483*np.log(P) - 0.000269*ETp
    #      - 0.09913*np.log(1 + Sp) + 0.05222*(WKmax - WP))
    v = (1.106 - 0.1625*np.log(P) + 0.0001282*ETp
         + 0.1131*np.log(1 + Sp) + 0.2848*WKmax_WP)
    g = max((1 - (a + v)), 0.0)
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
paver_stonegrid(Area=1000, P=800, ETp=650)

#%% Berechnungsansatz B.3.9: Wassergebundene Decke
# Wassergebundene Decke, offiziell Deckschicht ohne Bindemittel (Kürzel: DoB)
# gravel ground cover
def gravel_cover(Area, P, ETp, h=100, Sp=3.5, kf=1.8):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). h stands for installation heigth (mm),
    Sp stands for storage heigth (mm), kf corresponds to hydraulic
    conductivity (mm/h). Standard values are:
    h = 100 mm, Sp = 3.5 mm, kf = 180
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(h, 'h_gravel_cover')
    validRange(Sp, 'Sp_gravel_cover')
    validRange(kf, 'kf_gravel_cover')     
    
    a = 0.00004517*P - 0.03454*np.log(Sp) + (0.1958/(0.2873 + kf))
    # g = (0.19761*np.log(P) - 0.000506*ETp + 0.016372*Sp - 0.001618*h
    #      - 0.327742*np.exp(0.346808/kf))
    v = (0.2111 - 0.2544*np.log(P) + 0.2073*np.log(ETp)
         + 0.0006249*Sp + 0.123*np.log(h) - 0.000002806*kf)
    g = max((1 - (a + v)), 0.0)
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
gravel_cover(Area=1000, P=1000, ETp=650)

#%% Berechnungsansatz B.4 Aufteilungswerte und Berechnungsansätze für Anlagen
# Ableitung: Rohr, Rinne, steiler Graben
# Drainage: pipe, channel, steep ditch
def drainage(Area, P, ETp, drainage_type):
    '''Area corresponds to the surface of the element in m2,
    P stands for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). drainge_type is a text input, the possible
    input options are:
    "pipe", "Pipe", "PIPE", "Rohr", "rohr", "ROHR", "channel","Channel",
    "CHANNEL", "Rinne", "rinne", "RINNE", "steep ditch", "Steep Ditch",
    "STEEP DITCH", "steiler graben","steiler Graben", "STEILER GRABEN",
    "Shallow ditches with vegetation", "Ditch with vegetation",
    "ditch with vegetation", "Flache Gräben mit Bewuchs",
    "Gräben mit Bewuchs"
    '''
    drainages = ("pipe", "Pipe", "PIPE", "Rohr", "rohr", "ROHR",
                 "channel", "Channel", "CHANNEL", "Rinne", "rinne",
                 "RINNE", "steep ditch", "Steep Ditch", "STEEP DITCH",
                 "steiler graben", "steiler Graben", "STEILER GRABEN")
    veg_drainage = ("Shallow ditches with vegetation",
                    "Ditch with vegetation", "ditch with vegetation",
                    "Flache Gräben mit Bewuchs", "Gräben mit Bewuchs")

    validRange(P, 'P')
    validRange(ETp, 'ETp')

    if ((drainage_type in drainages) or
        (drainage_type in veg_drainage))  == False:
        return ("Wrong input as drinage-type")
    if (drainage_type in drainages) == True:   
        a = 1
        g = 0
        v = 0
    if (drainage_type in veg_drainage) == True:
        a = 0.7
        g = 0.1
        v = 0.2
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)
# Test
drainage(Area=1000, P=800, ETp=500, drainage_type="ditch with vegetation")
drainage(Area=1000, P=800, ETp=500, drainage_type="Rohr")
drainage(Area=1000, P=800, ETp=500, drainage_type="Pip3")

#%% Berechnungsansatz B.4.1: Flächenversickerung
# Surface infiltration
def surf_infiltration(Area, P, ETp, kf, FAsf="FAsf_standard"):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). kf stands for hydraulic 
    conductivity (mm/h). FAsf (%) stands for percentage of infiltration
    area. The standard value is calculated in terms of kf as:
    FAsf_standard = 94741*kf*exp(-1.195)
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(kf, 'kf_surf_infiltration') 
    
    if (FAsf == "FAsf_standard"):
        FAsf = 94741*kf**(-1.195)
        
    a = 0.004264 + 0.001121*np.log(P) - 0.002757*np.log(FAsf)
    # g = (0.6207904 + 0.0899322*np.log(P) - 0.0001152*ETp
    #      - 0.0719723*np.log(FAsf))
    v = 0.3999 - 0.09317*np.log(P) + 0.00009746*ETp + 0.07474*np.log(FAsf)
    g = max((1 - (a + v)), 0.0)
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
surf_infiltration(Area=1000, P=800, ETp=600, kf=500)

#%% Berechnungsansatz B.4.2: Versickerungsmulde
# Infiltration swale
def infilt_swale(Area, P, ETp, kf, FAsm="FAsm_standard"):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). kf stands for hydraulic 
    conductivity (mm/h). FAsm (%) stands for percentage of percolation
    area (swale). The standard value is calculated in terms of kf as:
    FAsm_standard = 42.323*kf*exp(-0.314)
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(kf, 'kf_infilt_swale') 
    
    if (FAsm == "FAsm_standard"):
        FAsm = 42.323*kf**(-0.314)       
    
    g = (0.8608 + 0.02385*np.log(P) - 0.00005331*ETp - 0.002827*FAsm
          - 0.000002493*kf + 0.0009514*np.log(kf/FAsm))
    v = 0.000008562*ETp + (2.611/(P-64.35))*FAsm**0.9425 - 0.000001211*kf
    # a = 1 - g - v
    # To force positive values or zero
    a = max((1 - (g + v)), 0.0)
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
infilt_swale(Area=1000, P=800, ETp=700, kf=500)

#%% Berechnungsansatz B.4.3: Mulde-Rigolen-Elemente
# Swale-trench element
def swale_trench(Area, P, ETp, kf, FAsm="FAsm_standard"):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). kf stands for hydraulic 
    conductivity (mm/h). FAsm (%) stands for percentage of percolation
    area (swale). The standard value is calculated in terms of kf as:
    FAsm_standard = 21.86*kf*exp(-0.348)
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(kf, 'kf_swale_trench')
    
    if (FAsm == "FAsm_standard"):
        FAsm = 21.86*kf**(-0.348)
        
    a = (-0.03867 + 0.007684*np.log(P) + 0.000003201*FAsm + 0.0002564*kf
         - 0.0001187*FAsm*kf + 0.004161*np.log(kf/FAsm))
    # g = (0.8803 + 0.01866*np.log(P) - 0.00004867*ETp
    #      - 0.001997*FAsm + 0.0002365*kf)
    v = 0.000008879*ETp + (2.528/(P-81.65))*FAsm**0.9496 - 0.00007768*kf
    g = max((1 - (a + v)), 0.0)
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
swale_trench(Area=1000, P=700, ETp=500, kf=10)

#%% Berechnungsansatz B.4.4: Mulden-Rigolen-System
# Swale-trench system
def swale_trench_system(Area, P, ETp, qDr, kf, FAsm="FAsm_standard"):
    '''Area corresponds to the surface of the element in m2, P stands
    for precipititaion (mm/a). ETp corresponds to potential
    evapotranspiration (mm/yr). qDr stands for the throttled discharge
    yield (l/(s*ha)), and kf stands for hydraulic conductivity (mm/h).
    FAsm stands for percentage of percolation area (%) calculated in
    terms of the hydraulic conductivity kf (mm/h) and qDr as:
    FAsm_standard = 11.79 - 3.14*LN(qDR) - 0.18594*kf
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(qDr, 'qDr_swale_trench_system')
    validRange(kf, 'kf_swale_trench_system')
    
    
    if (FAsm == "FAsm_standard"):
        FAsm = 11.79 - 3.14*np.log(qDr) - 0.18594*kf
        
    a = (0.8112 + 0.0003473*P - 0.00001845*ETp - 0.04793*FAsm
          + 0.0007481*qDr - 0.4389*np.log(kf + 1))
    # g = (1.669 - 0.3005*np.log(P) - 0.00006933*ETp
    #       + 0.3044*np.log(FAsm) + 0.4581*np.log(kf + 1))
    v = (0.1428 - 0.02661*np.log(P) + 0.00005668*ETp + 0.0288*np.log(FAsm)
          - 0.0001825*qDr - 0.01823*np.log(kf + 1))
    g = max((1 - (a + v)), 0.0)
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
swale_trench_system(Area=1000, P=800, ETp=500, qDr=6, kf=2)

#%% Berechnungsansatz B.4.5: Regenwassernutzung
# Rainwater usage
def rainwater_usage(P, ETp, VSp, VBr, FAbw=2, qBw=60):
    '''VSp stands for Specific storage volume (mm) in relation to the 
    connected, flow-effective area. VBr correspond to the available 
    water volume to use in relation to the connected, effective runoff
    area (mm/d). FAbw corresponds to proportion of irrigated area in 
    relation to the connected, effective runoff area (-).
    qBw stands for specific annual requirement for irrigation 
    (l/(m^2*year))
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(VSp, 'VSp_rainwater_usage')
    validRange(VBr, 'VBr_rainwater_usage')
    validRange(FAbw, 'FAbw_rainwater_usage')
    validRange(qBw, 'qBw_rainwater_usage')
    
    
    VBw = FAbw*qBw
    Vnmin = min(P, 365*VBr + VBw)
    if VBw == 0:
        v = 0
    else:
        v = (- 0.0001927*P + 0.0001831*ETp + 0.0006083*VBw
             - 0.0000003127*VBw**2 - 0.3092*np.exp(3.269/VSp)
             + (1.424/(2.782 + VBr)) + 0.0001885*Vnmin)
    if VBr == 0:
        e = 0
    else:
        e = (0.4451 - 0.0003529*P - 0.00007728*ETp + 0.06821*np.log10(VSp)
             - 0.0002507*VBw + 0.2349*np.log10(VBr) + 0.0001738*Vnmin)
    a = max((1 - (v + e)), 0.0)
    g = 0.0
    RD = P*a
    GWN = P*g
    ETP = P*v
    results = [{'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "e", 'Unit': "-", 'Value': e},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
rainwater_usage(P=800, ETp=500, VSp=100, VBr=2.5)

#%% Berechnungsansatz B.4.6: Teichanlage mit Zufluss von befestigten Flächen
# Pond system with inflow from paved areas
def pod_system(P, ETp, Aw, A_1, a_1, A_2= 0, a_2= 0.0, A_3= 0, a_3= 0.0,
               A_4= 0, a_4= 0.0):
    '''P stands for precipititaion (mm/a). ETp corresponds to 
    potential evapotranspiration (mm/yr). Aw stands for pod surface (m2),
    A_i corresponds to the Area i, which directs its runoff to the 
    pond (m2), a_i corresonds to proportion of area i (0.0-1.0),
    which directs its runoff to the pond (-)
    '''
    validRange(P, 'P')
    validRange(ETp, 'ETp')
    validRange(a_1, 'a_1_pod_system')
    validRange(a_2, 'a_2_pod_system')
    validRange(a_3, 'a_1_pod_system')
    validRange(a_4, 'a_1_pod_system')
    
    v = (ETp*Aw)/(P*(Aw + A_1*a_1 + A_2*a_2 + A_3*a_3 + A_4*a_4))
    a = 1 - v
    g = 0
    Area = Aw + A_1 + A_2 + A_3 + A_4
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000   
    results = [{'Name' : "Pod area (Aw)", 'Unit': "m2", 'Value': Aw},
               {'Name' : "Total area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)

# Test
pod_system(P=800, ETp=500, Aw=1000, A_1=0, a_1=0.5)
pod_system(P=800, ETp=500, Aw=800, A_1=200, a_1=0.5)