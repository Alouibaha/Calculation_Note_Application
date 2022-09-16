import pandas as pd
import numpy as np

initial_equipment_gains = pd.DataFrame(
    [
        ['Scialytique', 100.0, 2],
        ['Bistouri électrique',	50.0, 1],
        ['Respirateur', 50.0, 1],
        ['Moniteur', 50.0, 1],
        ['Colonne de coelioscopie', 150.0, np.NaN],
        ['Microscope', np.NaN, np.NaN],
        ['Ampli de brillance', np.NaN, np.NaN],
        ['Echographe', np.NaN, np.NaN],
        ['Couverture chauffante', np.NaN, np.NaN]
    ],
    columns = ['equipment', 'heat_gains_w', 'qty'],

)

def append_empty_rows(df, number_of_rows_to_add):
    return pd.concat([
        df,
        pd.DataFrame(
            [[np.NaN]*len(df.columns)]*number_of_rows_to_add,
            columns = df.columns
        )
    ]).reset_index(drop=True)


def full_df(df, number_of_rows):
    current_number_of_rows = len(df.index)
    if number_of_rows > current_number_of_rows:
        df = append_empty_rows(df, number_of_rows - current_number_of_rows)
    elif number_of_rows < current_number_of_rows:
        df = df.iloc[:number_of_rows]
    return df.assign(kw=df['heat_gains_w']*df['qty']/1000.0)
