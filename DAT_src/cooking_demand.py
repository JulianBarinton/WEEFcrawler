#%% Import packages

import ramp
import pandas as pd
import numpy as np
import copy
from  time import perf_counter

# Define timeseries for which demand profiles will be generated
days_nr = 3  # Number of days
timeseries = pd.date_range("2018-01-01", periods=days_nr * 24 * 60, freq="Min")  # 2018 starts on Monday
days_timeseries = pd.date_range("2018-01-01", periods=days_nr, freq="D")


#%% Dummy dict of cooking demands

cooking_demand_dict = {
    'low_income_hh': {
        'num_users': 20,
        'months_present': [1, 2, 3, 4, 7, 8, 9, 10, 11, 12],
        'working_days': [0, 1, 2, 3, 4, 5, 6],
        'cooking_demands': {
            'lunch':
                {
                    'stove': 'three_stone_fire',  # stove used for this cooking demand -> to match metadata
                    'fuel': 'firewood',  # fuel used -> to match meta data
                    'fuel_amount': 0.3,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                    'cooking_window_start': 5,  # start of time window of this cooking demand [h]
                    'cooking_window_end': 8,  # end of time window of this cooking demand [h]
                    'cooking_time': 1.5,  # average duration of this meal preparation
                 },
            'dinner':
                {
                    'stove': 'three_stone_fire',  # stove used for this cooking demand -> to match metadata
                    'fuel': 'firewood',  # fuel used -> to match meta data
                    'fuel_amount': 0.3,  # amount of fuel used for this demand [unit depending on fuel -> metadata]
                    'cooking_window_start': 5,  # start of time window of this cooking demand [h]
                    'cooking_window_end': 8,  # end of time window of this cooking demand [h]
                    'cooking_time': 1.5,  # average duration of this meal preparation
                },
        }
    }
}

# Admin meta data regarding cooking demands
admin_input = {
    'cooking_metadata': {
        'cooking_time_variability': 0.2,
        'cooking_window_variability': 0.2,
        'cooking_fuels': {
            'firewood': {
                'energy_content': 3,  # energy content per unit of this fuel
                'unit': 'kg'
            },
            'charcoal': {
                'energy_content': 5,
                'unit': 'kg'
            },
            'biogas': {
                'energy_content': 10,
                'unit': 'l'
            }
        },
        'cooking_stoves': {
            'three_stone_fire': {
                'efficiency': 0.1
            },
            'advanced_firewood_stove': {
                'efficiency': 0.2
            }
        }
    }
}

#%%
from DAT_src.ramp_control import RampControl

ramp_control = RampControl(365, '2018-01-01')

cooking_demand_use_case = ramp_control.generate_cooking_demand_use_cases(cooking_demand_dict, admin_input)
df = ramp_control.run_use_cases(cooking_demand_use_case, cooking_demand_dict)
