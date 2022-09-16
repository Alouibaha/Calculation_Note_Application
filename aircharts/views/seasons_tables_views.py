from aircharts import seasons_tables
from aircharts.conf import initial_pressure
import dash_table
from dash_table.Format import Format, Scheme

initial_summer_df = seasons_tables.full_df(
    seasons_tables.initial_summer_data,
    initial_pressure,
    dew_point = True
)
initial_summer_df['air'] = initial_summer_df.index
initial_winter_df = seasons_tables.full_df(
    seasons_tables.initial_winter_data,
    initial_pressure
)
initial_winter_df['air'] = initial_winter_df.index

def _table(id, initial_df):
    return dash_table.DataTable(
        id=id,
        columns = [
            {"name": "", "id": "air"},
            {
                "name": "Temp (°C)",
                "id": "TDryBulb",
                "editable":True,
                "type": "numeric",
                "format":Format(precision=1, scheme=Scheme.fixed)
            },
            {
                "name": "Rel.Hum (%)",
                "id": "RelHumPercent",
                "editable":True,
                "type": "numeric"
            },
            {
                "name": "Enthalpy (kJ/kgas)",
                "id": "MoistAirEnthalpyKJ",
                "type": "numeric",
                "format":Format(precision=1, scheme=Scheme.fixed)
            },
            {
                "name": "Water W. (kg/kgas)",
                "id": "HumRatio",
                "type": "numeric",
                "format":Format(precision=4, scheme=Scheme.fixed)
            }
        ],
        data = initial_df.to_dict('records'),
        style_data_conditional=[{
            'if': {
                'column_editable': True,
                'filter_query': '{air} != "Blowing air"'

            },
            'backgroundColor': '#AFE1AF',
            'border': "1px solid white"

        }]
    )

def summer_table():
    return _table("summer-table", initial_summer_df)

def winter_table():
    return _table("winter-table", initial_winter_df)
