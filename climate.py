# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 13:02:41 2021

@author: Edwin Echeverri Salazar
"""

#  Source: DWD, climatology 1991-2020, values aggregated and extracted from
#  https://opendata.dwd.de/climate_environment/CDC/grids_germany/multi_annual/precipitation/
#  https://opendata.dwd.de/climate_environment/CDC/grids_germany/multi_annual/evapo_p/
climate_dict = {
    'Augsburg' : [820.0, 619.5],
    'Berlin' : [570.0, 666.4],
    'Bielefeld' : [867.0, 599.8],
    'Bonn' : [649.0, 661.6],
    'Braunschweig' : [611.0, 629.9],
    'Bremen' : [730.0, 608.6],
    'Bremerhaven' : [757.0, 597.1],
    'Chemnitz' : [768.0, 613.5],
    'Coburg' : [778.0, 603.9],
    'Cottbus' : [569.0, 687.4],
    'Dortmund' : [797.0, 625.5],
    'Dresden' : [589.0, 673.1],
    'Duisburg' : [761.0, 640.9],
    'Düsseldorf' : [772.0, 646.1],
    'Emden' : [829.0, 597.3],
    'Erfurt' : [531.0, 631.9],
    'Essen' : [761.0, 609.0],
    'Flensburg' : [915.0, 573.1],
    'Frankfurt am Main' : [628.0, 665.8],
    'Freiburg im Breisgau' : [987.0, 643.6],
    'Fürth' : [613.0, 638.1],
    'Gera' : [649.0, 640.3],
    'Gießen' : [596.0, 638.7],
    'Göttingen' : [637.0, 620.4],
    'Hamburg' : [790.0, 600.8],
    'Hannover' : [658.0, 619.2],
    'Heidelberg' : [671.0, 681.0],
    'Hof' : [707.0, 569.3],
    'Ingolstadt' : [685.0, 631.4],
    'Jena' : [567.0, 652.4],
    'Karlsruhe' : [746.0, 689.1],
    'Kassel' : [595.0, 627.3],
    'Kiel' : [798.0, 577.4],
    'Koblenz' : [638.0, 661.4],
    'Köln' : [787.0, 656.4],
    'Leipzig' : [589.0, 661.6],
    'Lübeck' : [681.0, 593.5],
    'Magdeburg' : [503.0, 656.2],
    'Mainz' : [555.0, 671.7],
    'Mannheim' : [605.0, 682.2],
    'München' : [973.0, 610.2],
    'Münster' : [745.0, 617.9],
    'Nürnberg' : [639.0, 632.7],
    'Oldenburg' : [781.0, 606.8],
    'Osnabrück' : [827.0, 604.1],
    'Passau' : [882.0, 631.6],
    'Potsdam' : [554.0, 670.1],
    'Regensburg' : [669.0, 629.2],
    'Rosenheim' : [1125.0, 626.5],
    'Rostock' : [645.0, 588.7],
    'Saarbrücken' : [829.0, 661.3],
    'Schwerin' : [665.0, 593.0],
    'Stralsund' : [645.0, 584.7],
    'Stuttgart' : [683.0, 656.0],
    'Ulm' : [723.0, 626.2],
    'Wiesbaden' : [631.0, 650.5],
    'Wuppertal' : [1290.0, 572.8],
    'Würzburg' : [618.0, 652.9],
}

def climate(place):
    p = climate_dict[place][0]
    etp = climate_dict[place][1]
    return p, etp