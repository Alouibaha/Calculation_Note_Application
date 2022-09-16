from aircharts import conf
conf.set_system_of_units()

from aircharts.views import (
    main_view, psychro_img, electric_consumption_figure, heat_gains_figure
)
from aircharts.altitude_to_pressure import altitude_to_pressure
from aircharts import seasons_tables, pressure_losses, equipment_gains
from dash.dependencies import Input, Output
import dash
import pandas as pd

app = dash.Dash(__name__)
app.layout = main_view.div(app)

@app.callback(
    Output("pressure-table", "data"),
    Input("general-parameters-table", "data")
)
def compute_pressure(general_data):
    return [{"pressure": _compute_pressure(general_data)}]

@app.callback(
    Output("summer-table", "data"),
    Input("general-parameters-table", "data"),
    Input("summer-table", "data")
)
def compute_summer_table(general_data, summer_data):
    summer_data = summer_data[:3]
    two_cols = _two_cols_season_df(summer_data)
    df = seasons_tables.full_df(
        two_cols, pressure = _compute_pressure(general_data),
        dew_point = True
    )
    df['air'] = df.index
    return df.to_dict('records')

@app.callback(
    Output("winter-table", "data"),
    Input("general-parameters-table", "data"),
    Input("winter-table", "data")
)
def compute_winter_table(general_data, winter_data):
    two_cols = _two_cols_season_df(winter_data)
    df = seasons_tables.full_df(
        two_cols, pressure = _compute_pressure(general_data)
    )
    df['air'] = df.index
    return df.to_dict('records')

@app.callback(
    Output("psychrograph-img", "src"),
    Input("general-parameters-table", "data"),
    Input("winter-table", "data"),
    Input("summer-table", "data")
)
def compute_psychrograph(general_data, winter_data, summer_data):
    return psychro_img.build_figure(
        _two_cols_season_df(summer_data[:3]),
        _two_cols_season_df(winter_data),
        float(general_data[0]['altitude'] or 0)
    )

@app.callback(
    Output("cta-table", "data"),
    Output("return-network-table", "data"),
    Output("supply-network-table", "data"),
    Output("equipment-gain-table", "data"),
    Output("electric-power", "children"),
    Output("consumpt-ahu", "children"),
    Output("consumpt-network", "children"),
    Output("heat-gains", "children"),
    Output("electric-consumption-graph", "figure"),
    Output("subtotal-heat-people", "children"),
    Output("subtotal-heat-equipment", "children"),
    Output("subtotal-heat-light", "children"),
    Output("subtotal-heat-ventilation", "children"),
    Output("total-heat-dissipation", "children"),
    Output("heat-gains-graph", "figure"),
    Input("general-parameters-table", "data"),
    Input("cta-table", "data"),
    Input("return-network-table", "data"),
    Input("supply-network-table", "data"),
    Input("mu-motor", "value"),
    Input("n-persons", "value"),
    Input("equipment-gain-table", "data"),
    Input("equipment-add-row", "n_clicks"),
    Input("equipment-del-row", "n_clicks")
)
def update_first_two_sections(
 general_data, cta_data, return_network_data, supply_network_data, mu_motor,
 n_persons, equipment_data, n_add_clicks, n_del_clicks
):
    try:
        air_blowing_flow = float(general_data[0]['air-blowing-flow'])
    except (TypeError, ValueError):
        air_blowing_flow = 0
    try:
        mu_motor = float(mu_motor)
    except (TypeError, ValueError):
        mu_motor = 10**-12

    cta_df = pd.DataFrame(cta_data)[['name', 'range_pa', 'value_pa']]
    cta_df = cta_df[cta_df['name'] != 'Totaux']
    full_cta_df = pressure_losses.full_cta_df(cta_df, air_blowing_flow, mu_motor)

    return_network_df = pd.DataFrame(return_network_data)[['name', 'qty', 'pa_per_ml']]
    return_network_df = return_network_df[return_network_df['name'] != 'Global']
    full_return_network_df = pressure_losses.full_network_df(
        return_network_df, air_blowing_flow, mu_motor
    )

    supply_network_df = pd.DataFrame(supply_network_data)[['name', 'qty', 'pa_per_ml']]
    supply_network_df = supply_network_df[supply_network_df['name'] != 'Global']
    full_supply_network_df = pressure_losses.full_network_df(
        supply_network_df, air_blowing_flow, mu_motor
    )

    def get_total(full_df, total_key):
        return full_df[full_df['name'] == total_key].iloc[0]['kw']

    cta_sum = get_total(full_cta_df, 'Totaux')
    return_network_sum = get_total(full_return_network_df, 'Global')
    supply_network_sum = get_total(full_supply_network_df, 'Global')
    network_sum = return_network_sum + supply_network_sum
    electric_power = (cta_sum + network_sum) / mu_motor
    heat_gains_ventilation = electric_power - electric_power * mu_motor

    people_heat = float(n_persons) * (
        general_data[0]['people-heat-gains'] or 0
    ) / 1000.0

    full_equipments_gain_df = _compute_new_equipment_gains_full_df(
        equipment_data, n_add_clicks, n_del_clicks
    )

    equipment_heat = full_equipments_gain_df['kw'].sum()

    area = float(general_data[0]['area'] or 0)
    lighting_heat_gains = float(general_data[0]['lighting-heat-gains'] or 0)
    lighting_heat = area*lighting_heat_gains/1000.0

    return (
        full_cta_df.to_dict('records'),
        full_return_network_df.to_dict('records'),
        full_supply_network_df.to_dict('records'),
        full_equipments_gain_df.to_dict('records'),
        round(electric_power, 2),
        round(cta_sum, 2),
        round(network_sum, 2),
        round(heat_gains_ventilation, 2),
        electric_consumption_figure.figure(cta_sum, return_network_sum, supply_network_sum),
        round(people_heat, 2),
        round(equipment_heat, 2),
        round(lighting_heat, 2),
        round(heat_gains_ventilation, 2),
        round(people_heat + equipment_heat + lighting_heat + heat_gains_ventilation, 2),
        heat_gains_figure.figure(
            people_heat, equipment_heat, lighting_heat, heat_gains_ventilation
        )
    )

def _compute_new_equipment_gains_full_df(equipment_data, n_add_clicks, n_del_clicks):
    df = pd.DataFrame(
        equipment_data,
        columns = ['equipment', 'heat_gains_w', 'qty', 'kw']
    ).drop('kw', axis=1)
    n_rows = (
        conf.initial_equipment_table_n_rows
        +
        (n_add_clicks or 0)
        -
        (n_del_clicks or 0)
    )
    return equipment_gains.full_df(df, n_rows)

def _compute_pressure(general_data):
    try:
        altitude = float(
            general_data[0]['altitude']
        )
    except (TypeError, ValueError):
        altitude = 0
    return altitude_to_pressure(altitude)

def _two_cols_season_df(season_table_data):
    return pd.DataFrame(
        [
            [row['TDryBulb'], row['RelHumPercent']]
            for row in season_table_data
        ],
        index = [row['air'] for row in season_table_data],
        columns = ['TDryBulb', 'RelHumPercent']
    )
