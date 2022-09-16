from aircharts import pressure_losses
from aircharts import conf
import dash_table
from dash_table.Format import Format, Scheme


initial_return_network_df = pressure_losses.full_network_df(
    pressure_losses.initial_return_network,
    conf.initial_air_blowing_flow,
    conf.initial_mu_motor
)

initial_supply_network_df = pressure_losses.full_network_df(
    pressure_losses.initial_supply_network,
    conf.initial_air_blowing_flow,
    conf.initial_mu_motor
)

def _table(network_id, initial_df):
    return dash_table.DataTable(
        id=network_id,
        merge_duplicate_headers=True,
        columns = [
            {
                "name": ["", ""],
                "id":"name",
                "editable": True
            },
            {
                "name": ["", "Qty"],
                "id":"qty",
                "editable": True,
                "type": "numeric",
                "format":Format(precision=0, scheme=Scheme.fixed)
            },
            {
                "name": ["Pressure losses", "Pa/ml"],
                "id":"pa_per_ml",
                "editable": True,
                "type": "numeric",
                "format":Format(precision=1, scheme=Scheme.fixed)

            },
            {
                "name": ["Pressure losses", "Pa"],
                "id":"pa",
                "editable": False,
                "type": "numeric",
                "format":Format(precision=1, scheme=Scheme.fixed)

            },
            {
                "name": ["P.", "kW"],
                "id":"kw",
                "type": "numeric",
                "format":Format(precision=2, scheme=Scheme.fixed)
            }

        ],
        data = initial_df.to_dict('records'),
        style_data_conditional=[
            {
                'if': {
                    'column_id': column_id,
                    'filter_query': '{name} != "Global"'

                },
                'backgroundColor': '#AFE1AF',
                'border': "1px solid white"
            }
            for column_id in ('qty', 'pa_per_ml')
        ]
    )

def return_network_table():
    return _table('return-network-table', initial_return_network_df)

def supply_network_table():
    return _table('supply-network-table', initial_supply_network_df)
