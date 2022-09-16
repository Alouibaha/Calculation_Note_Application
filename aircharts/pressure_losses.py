import numpy as np
import pandas as pd

initial_cta = pd.DataFrame(
    [
        ['Pre-filter', '0 à 300', 300.0],
        ['Cooling coil', '100 à 150', 120],
        ['Heating coil', '0 à 80', 25],
        ['Sound Attenuator', '10 à 50', 15],
        ['Filter F9', '100 à 450', 300]
    ],
    columns = ['name', 'range_pa', 'value_pa']
)

def full_cta_df(df, air_blowing_flow, mu_motor):
    df = df.assign(
        kw = (air_blowing_flow * df['value_pa'] / 3600)
        /
        (mu_motor * 1000.0)
    )
    return df.append(
        pd.Series(
            {
                'name': "Totaux",
                'range_pa': "",
                "value_pa": df['value_pa'].sum(),
                "kw": df['kw'].sum()
            }
        ),
        ignore_index = True
    )

initial_return_network = pd.DataFrame(
    [
        ['Damper', 1, 15],
        ['Fire Damper', 1, 10],
        ['Duct', 30, 1.5],
        ['Accident', 1, 5],
        ['Filter F7', 1, 200]
    ],
    columns = ['name', 'qty', 'pa_per_ml']
)

initial_supply_network = pd.DataFrame(
    [
        ['Damper', 1, 15],
        ['Fire Damper', 1, 10],
        ['Duct', 30, 1.5],
        ['Accident', 8, 5],
        ['HEPA filter', 1, 450]
    ],
    columns = ['name', 'qty', 'pa_per_ml']
)

def full_network_df(df, air_blowing_flow, mu_motor):
    pa_series = df['qty']*df['pa_per_ml']
    kw_series = air_blowing_flow*(pa_series/3600.0)/(mu_motor*1000.0)
    df = df.assign(pa = pa_series, kw = kw_series)
    return df.append(
        pd.Series(
            {
                'name': "Global",
                'qty': np.NaN,
                "pa_per_ml": np.NaN,
                "pa": df['pa'].sum(),
                "kw": df['kw'].sum()
            }
        ),
        ignore_index = True
    )
