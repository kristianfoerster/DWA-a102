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

class Element():
    def __init__(self, element_type, element_params):
        self.type = element_type
        self.params = element_params

def register_measure(f):
    signature = inspect.signature(f)
    list_param = list()
    list_values = list()
    for param in signature.parameters.values():
        sparam = str(param)
        if sparam=='self': 
            continue
        split = sparam.split('=')
        if len(split)==1:
            list_param.append(sparam)
            list_values.append(0.0)
        else:
            list_param.append(split[0])
            list_values.append(split[1])
    return Element(f.__name__,pd.DataFrame([list_values], columns=list_param, index=['Wert']))

def update_data(index, option):
    edited_data = st.data_editor(st.session_state.data_list[index], key=f'parameters{index}')
    st.session_state.data_list[index] = edited_data

# initalize water balance computations
dict_elements = {}
dict_elements['Steildach']=register_measure(StudyArea.roof)
dict_elements['Grünes Dach']=register_measure(StudyArea.green_roof)
dict_elements['Grünes Dach (minimal)'] = register_measure(StudyArea.green_roof_shallow)
dict_elements['Einstaudach'] = register_measure(StudyArea.storage_roof)
dict_elements['Versiegelte Fläche'] = register_measure(StudyArea.flat_area)
dict_elements['wassergebundene Decke'] = register_measure(StudyArea.gravel_cover)
dict_elements['Teildurchlässige Flächenbeläge'] = register_measure(StudyArea.permeable_surface)
dict_elements['Poren-/Sicherstreine, Schotter'] = register_measure(StudyArea.porous_surface)
dict_elements['Rasengittersteine'] = register_measure(StudyArea.paver_stonegrid)
dict_elements['Gärten'] = register_measure(StudyArea.garden)

# Streamlit app
st.title('Wasserbilanzberechnung (in Anlehnung an DWA-M102-4)')

# climate input
in_precip = st.number_input('Mittlere Niederschlagshöhe [mm/a]',
                        min_value=param_ranges['P'][0], max_value=param_ranges['P'][1], value=700)

in_corr_needed = st.checkbox('Niederschlag korrigieren?')

in_precip_corr = st.number_input('Korrektur des Niederschlagsmessfehlers in Prozent', 
                        min_value=0, max_value=25, value=0)

in_etp = st.number_input('Potenzielle Verdunstung  [mm/a]', 
                        param_ranges['ETp'][0], max_value=param_ranges['ETp'][1], value=500)

if in_corr_needed:
    in_precip *= (1 + in_precip_corr / 100)

in_kf = st.number_input('Hydraulische Leitfähigkeit Versickerungsmulde [mm/h]', 
                        param_ranges['kf_infilt_swale'][0], max_value=param_ranges['kf_infilt_swale'][1], value=200)

# in_a = st.number_input('Aufteilungswert Direktabfluss [-]', format='%.2f',
#                         min_value=0., max_value=1.0, value=0.2, step=0.01)

# in_e = st.number_input('Aufteilungswert Verdunstung [-]',  format='%.2f',
#                         min_value=0., max_value=1.0, value=0.6, step=0.01)

# in_g = st.number_input('Aufteilungswert Grundwasserneubildung [-]', format='%.2f', 
#                         min_value=0., max_value=1.0, value=0.2, step=0.01)


num_objects = st.number_input('Anzahl der Berechnungselemente', min_value=1, value=1, max_value=5) 

if 'data_list' not in st.session_state:
    st.session_state.data_list = []

for i in range(0,num_objects):
    st.write(f'Berechnungselement {i}')
    option=st.selectbox(f'Oberflächentyp {i}', dict_elements.keys(), key=f'select{i}')
    if option=='Gärten':
        st.write('Aufteilungswerte für den natürlichen Referenzzustand (siehe www.naturwb.de):')
    # Initialize data_list with default params if not already done
    if len(st.session_state.data_list) <= i:
        st.session_state.data_list.append(dict_elements[option].params)
    else:
        # Update the DataFrame with the selected option's params if the option changes
        st.session_state.data_list[i] = dict_elements[option].params
    
    update_data(i, option)
    st.checkbox('An Maßnahme anschließen?', False, key=f'check{i}')



if st.button('Berechnungstarten'):
    
    list_connected = list()
    list_unconnected = list()
    
    #st.write(in_precip)
    study_area = StudyArea(in_precip, in_etp)
    
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
        if params_i.at['Wert','area']==0.:
            st.write(f'Ignoriere Element {i}, da Fläche null.')
            continue
        
        if function_i == 'garden':
            wb_check = np.round(np.sum(params_i[['a','v','g']].iloc[0]), 2)
            #st.write('Kontrolle der Aufteilungswerte (sollte 0 ergeben): ', wb_check)
            if wb_check != 1.00:
                raise ValueError('Auteilungswerte ergeben nicht 1.0 in der Summe!')
        
        result = getattr(study_area, function_i)(**params_i.iloc[0])
        
        if st.session_state[f'check{i}']:
            list_connected.append(result)
        else:
            list_unconnected.append(result)
        
        #st.write(result)
    
    if len(list_connected)>0:
        swale = study_area.infilt_swale(in_kf, *list_connected)
        list_water_balance=list_unconnected + [swale]
    else:
        list_water_balance = list_unconnected
        if len(list_water_balance)==0:
            raise ValueError('Keine gültigen Berechnungselemente gefunden. Bitte überprüfe die Flächen!')
    
    
    fig, ax = plt.subplots()
    
    res = watbal(*list_water_balance)
    
    st.write(res)
    
    
    res.set_index('Element', inplace=True)
    res.drop(columns=['Area','Vp','Va','Vg','Vv'], inplace=True)
    res.plot(ax=ax, kind='bar')
    ax.set_ylabel('a, v, g [-]')

    st.pyplot(fig)
    #plot_watbal(*list_water_balance)
    
    
        
