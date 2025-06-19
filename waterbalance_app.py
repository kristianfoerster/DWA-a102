#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 19:00:59 2025

@author: kristianfoerster
"""

import streamlit as st
import numpy as np
import inspect
from dwa_a102 import StudyArea, watbal
from check_ranges import param_ranges
import pandas as pd
import matplotlib.pyplot as plt
from treelib import Node, Tree


class Element():
    def __init__(self, element_type, element_params, element_info, has_surf=False):
        self.type = element_type
        self.params = element_params
        self.help = element_info
        self.surf=has_surf


def register_measure(f):
    signature = inspect.signature(f)
    list_param = list()
    list_values = list()
    surfaces = False
    for param in signature.parameters.values():
        sparam = str(param)
        if sparam=='self': 
            continue
        split = sparam.split('=')
        if len(split)==1:
            if '*surfaces' in sparam:
                surfaces = True
                continue
            list_param.append(sparam)
            list_values.append(0.0)
        else:
            if 'fasm' in sparam or 'fasf' in sparam:
                continue
            list_param.append(split[0])
            list_values.append(split[1])
    helptext = inspect.getdoc(f)
    return Element(f.__name__,pd.DataFrame([list_values], columns=list_param, 
                    index=['Value']), helptext, surfaces)

def update_data(index, option, cont):
    edited_data = cont.data_editor(st.session_state.data_list[index], key=f'parameters{index}')
    st.session_state.data_list[index] = edited_data


# initalize water balance computations
dict_elements = {}
dict_elements['Gärten, Grünflächen (Garden / Green Area)'] = register_measure(StudyArea.garden)
dict_elements['Versiegelte Fläche (Flat Area)'] = register_measure(StudyArea.flat_area)
dict_elements['wassergebundene Decke (Gravel Cover)'] = register_measure(StudyArea.gravel_cover)
dict_elements['Teildurchlässige Flächenbeläge (Permeable Surface)'] = register_measure(StudyArea.permeable_surface)
dict_elements['Poren-/Sicherstreine, Schotter (Porous Surface)'] = register_measure(StudyArea.porous_surface)
dict_elements['Rasengittersteine (Paver Stonegrid)'] = register_measure(StudyArea.paver_stonegrid)
dict_elements['Steildach (Roof)']=register_measure(StudyArea.roof)
dict_elements['Grünes Dach (Green Roof)']=register_measure(StudyArea.green_roof)
dict_elements['Grünes Dach minimal (Green Roof Shallow)'] = register_measure(StudyArea.green_roof_shallow)
dict_elements['Einstaudach (Storage Roof)'] = register_measure(StudyArea.storage_roof)

dict_measures = {}
dict_measures['Mulde (Infiltration Swale)'] = register_measure(StudyArea.infilt_swale)
#dict_measures['Drainage (Entwässerung)'] = register_measure(StudyArea.drainage) # fix connection types
dict_measures['Flächenversickerung (Surf infiltration)'] = register_measure(StudyArea.surf_infiltration)
dict_measures['Mulde mit Rigole (Swale Trench)'] = register_measure(StudyArea.swale_trench)
dict_measures['Mulden-Rigolen-System (Swale-Trench System)'] = register_measure(StudyArea.swale_trench_system)
dict_measures['Regenwassernutzung (Rainwater Usage)'] = register_measure(StudyArea.rainwater_usage)
dict_measures['Teich (Pond System)'] = register_measure(StudyArea.pond_system)


# Streamlit app
st.title('Berechnung der langjährigen Wasserbilanz (in Anlehnung an DWA-M102-4)')
st.header('*Calculation of the long-term water balance (based on DWA-M102-4)*')

st.write('Diese App basiert auf einer Reihe studentischer Projekte an der \
         Leibniz Universität Hannover und der Hochschule Weihenstephan-\
         Triesdorf. Es sollen einige wenige Berechnungsgrundlagen aus dem \
         DWA-Merkblatt DWA M102 Teil 4 möglichst sehr einfach zugänglich \
         gemacht werden, um studentische Projekte zu untersützen. Ferner soll \
         es bewusst keine Konkurrenz zur Software WABILA darstellen, da der \
         Funktionsumfang der App deutlich kleiner ist. Die usprüngliche \
         Programmierung stammt von EdiSalazar (https://github.com/EdiSalazar/DWA-a102).')


st.markdown('*This app is based on a series of student projects at Leibniz\
         University Hannover and Weihenstephan-Triesdorf University of\
         Applied Sciences. The aim is to make a few calculation principles\
         from DWA guideline DWA M102 Part 4 as accessible as possible in order\
         to support student projects. The original programming was done by\
         EdiSalazar (https://github.com/EdiSalazar/DWA-a102)*')

# show help texts
in_showhelp = st.checkbox('Hilfetexte anzeigen (auf Englisch)? *Show Help?*')

# climate input
in_precip = st.number_input('Mittlere Niederschlagshöhe, *Mean Annual Precipitation Depth* [mm/a]',
                        min_value=param_ranges['P'][0], max_value=param_ranges['P'][1], value=700)

in_corr_needed = st.checkbox('Niederschlag korrigieren? *Correct Precipitation for undercatch?*')

in_precip_corr = st.number_input('Korrektur des Niederschlagsmessfehlers in Prozent, *Precipitation Undercatch Percentage*', 
                        min_value=0, max_value=25, value=0)

in_etp = st.number_input('Potenzielle Verdunstung, *Potential Evapotranspiration* [mm/a]', 
                        param_ranges['ETp'][0], max_value=param_ranges['ETp'][1], value=500)

if in_corr_needed:
    in_precip *= (1 + in_precip_corr / 100)

num_objects = st.number_input('Anzahl der Berechnungselemente, *\# of calculation elements*', min_value=1, value=1, max_value=10) 

if 'data_list' not in st.session_state:
    st.session_state.data_list = []

for i in range(0,num_objects):
    c = st.container(border=True)
    c.write(f':blue[Berechnungselement {i}], *:blue[Calculation Element {i}]*')
    option=c.selectbox(f'Oberflächentyp {i}, *Surface Type {i}*', dict_elements.keys(), key=f'select{i}')

    if option=='Gärten, Grünflächen (Garden / Green Area)':
        c.write('Aufteilungswerte für den natürlichen Referenzzustand (siehe www.naturwb.de):')
        c.markdown('*Partioning factors for natural reference state (see, www.naturwb.de):*')
    # Initialize data_list with default params if not already done
    if len(st.session_state.data_list) <= i:
        st.session_state.data_list.append(dict_elements[option].params)
    else:
        # Update the DataFrame with the selected option's params if the option changes
        st.session_state.data_list[i] = dict_elements[option].params
    
    update_data(i, option, c)
    c.checkbox('An Maßnahme anschließen? *Connect to Rainwater Management Measure?*', False, key=f'check{i}')
    if in_showhelp:
        container = c.container(border=True)
        container.write(dict_elements[option].help)

container_measure = st.container(border=True)
sel_measure = container_measure.selectbox(':blue[Regenwassermaßnahme auswählen], *:blue[Select Rainwater Management Measure]*', dict_measures.keys(), key='select_meas')
table_measure = dict_measures[sel_measure].params
if in_showhelp:
    container_help = container_measure.container(border=True)
    container_help.write(dict_measures[sel_measure].help)
edited_measures = container_measure.data_editor(table_measure, num_rows="dynamic")

if st.button('Berechnung starten'):
    
    list_connected = list()
    list_unconnected = list()
    
    #st.write(in_precip)
    study_area = StudyArea(in_precip, in_etp)
    
    tree = Tree()
    
    tree.create_node('System', 'system')
    
    for i in range(0,num_objects):
        #update_data(i)
        #st.write(st.session_state)
        label_i = st.session_state[f'select{i}']
        function_i = dict_elements[label_i].type

        params_i = st.session_state['data_list'][i].astype(float)
        #st.write(params_i)
        #dict_params = params_i.to_dict()
        #st.write(dict_params)
        
        # parameter checks
        if params_i.at['Value','area']==0.:
            st.write(f'Ignoriere Element {i}, da Fläche null. Ignore element {i} with zero area.')
            continue
        
        if function_i == 'garden':
            wb_check = np.round(np.sum(params_i[['a','v','g']].iloc[0]), 2)
            #st.write('Kontrolle der Aufteilungswerte (sollte 0 ergeben): ', wb_check)
            if wb_check != 1.00:
                raise ValueError('Auteilungswerte ergeben nicht 1.0 in der Summe! Total of partioning factors is not equal 1.')
        
        result = getattr(study_area, function_i)(**params_i.iloc[0])
        
        if st.session_state[f'check{i}']:
            list_connected.append(result)
        else:
            list_unconnected.append(result)
        
        #st.write(result)
    
    if len(list_connected)>0:
        # replace swale by any arbitrary measure
        #measure = study_area.infilt_swale(in_kf, *list_connected)
        
        # get type of measure and parameters
        function_m = dict_measures[sel_measure].type
        params_m = edited_measures.loc['Value'].values.tolist() #.iloc[0].values
        
        #call function
        result = getattr(study_area, function_m)(*params_m, *list_connected)
            
        
        
        list_water_balance=list_unconnected + [result]
        tree.create_node(result.iloc[-1]['Element'], 'measure', parent='system')
        for ni in list_connected:
            tree.create_node(ni.iloc[0]['Element'], parent='measure')
    else:
        list_water_balance = list_unconnected
        if len(list_water_balance)==0:
            raise ValueError('Keine gültigen Berechnungselemente gefunden. Bitte überprüfe die Flächen! No valid elements found. Please check inputs.')
    for ni in list_unconnected:
        tree.create_node(ni.iloc[0]['Element'], parent='system')
    
    
    st.write(tree)
    
    fig, ax = plt.subplots()
    
    st.markdown('Aufteilungsfaktoren für Abfluss $a$, Verdunstung $v$, \nGrundwasserneubildung $g$ (ggf. Entnahme $e$) [-], V kennzeichnet Volumenangaben in m$^3$/a.')
    st.markdown('Partioning factors for runoff $a$, evapotranspiration $v$, \ngroundwater recharge $g$ (withdrawal $e$, if applicable) [-], V denotes volume in m$^3$/yr.')
    
    res = watbal(*list_water_balance)
    
    st.write(res)
    
    
    res.set_index('Element', inplace=True)
    res.drop(columns=['Area','Vp','Va','Vg','Vv'], inplace=True)
    if 'Ve' in res.columns:
        res.drop(columns=['Ve'], inplace=True)
    res.plot(ax=ax, kind='bar')
    #ax.set_ylabel('Aufteilungsfaktoren für Abfluss $a$, Verdunstung $v$, \nGrundwasserneubildung $g$ (ggf. Entnahme $e$) [-]')
    ax.set_ylabel('$a$, $v$, $g$, $e$ [-]')
    st.pyplot(fig)
