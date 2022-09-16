import pandas as pd
import psychrolib

initial_summer_data = pd.DataFrame(
    {
        "TDryBulb": [21.0, 19.0, 34.0],
        "RelHumPercent": [70.0, 65.0, 80.0]
    },
    index = ["Mixed air", "Ambiant air", "Fresh air"]
)

initial_winter_data = pd.DataFrame(
    {
        "TDryBulb": [25.0, 27.0, 17.0],
        "RelHumPercent": [37.0, 32.0, 55.0]
    },
    index = ["Mixed air", "Ambiant air", "Fresh air"]
)

def full_df(df, pressure, dew_point = False, dew_point_name = 'Blowing air'):
    if dew_point:
        TDewPoint = psychrolib.GetTDewPointFromRelHum(
            df.loc['Ambiant air', 'TDryBulb'],
            df.loc['Ambiant air', 'RelHumPercent'] / 100.0
        )
        df = df.append(
            pd.Series(
                {'TDryBulb': TDewPoint, "RelHumPercent": 100.0},
                name=dew_point_name
            )
        )
    hum_ratio_series = df.apply(
        lambda row: psychrolib.GetHumRatioFromRelHum(
            row['TDryBulb'], row['RelHumPercent'] / 100.0, pressure
        ),
        axis = 1
    )
    hum_ratio_series.name = 'HumRatio'
    new_df = df.join(hum_ratio_series)
    moist_air_enthalpy_series = new_df.apply(
        lambda row: (
            psychrolib.GetMoistAirEnthalpy(row['TDryBulb'], row['HumRatio'])
            /
            1000.0
        ),
        axis = 1
    )
    moist_air_enthalpy_series.name = 'MoistAirEnthalpyKJ'
    new_df = new_df.join(moist_air_enthalpy_series)
    return new_df.reindex(
        ['TDryBulb', 'RelHumPercent', 'MoistAirEnthalpyKJ', 'HumRatio'],
        axis = 1,
    )

if __name__ == '__main__':
    from aircharts import conf
    from aircharts.altitude_to_pressure import altitude_to_pressure
    pressure = altitude_to_pressure(conf.initial_altitude)
    psychrolib.SetUnitSystem(psychrolib.SI)
    print("Summer:\n")
    print(full_df(initial_summer_data, pressure, dew_point = True))
    print()
    print("Winter:\n")
    print(full_df(initial_winter_data, pressure))
