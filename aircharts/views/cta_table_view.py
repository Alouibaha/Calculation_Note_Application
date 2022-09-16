from aircharts import pressure_losses
from aircharts import conf
import dash_table
from dash_table.Format import Format, Scheme


initial_cta_df = pressure_losses.full_cta_df(
    pressure_losses.initial_cta,
    conf.initial_air_blowing_flow,
    conf.initial_mu_motor

)

def table():
    return dash_table.DataTable(
        id="cta-table",
        merge_duplicate_headers=True,
        columns = [
            {
                "name": ["", ""],
                "id":"name",
                "editable": True
            },
            {
                "name": ["Pressure losses", "Range Pa"],
                "id":"range_pa",
                "editable": True
            },
            {
                "name": ["Pressure losses", "Value Pa"],
                "id":"value_pa",
                "editable": True,
                "type": "numeric",
                "format":Format(precision=2, scheme=Scheme.fixed)

            },
            {
                "name": ["P.", "kW"],
                "id":"kw",
                "type": "numeric",
                "format":Format(precision=2, scheme=Scheme.fixed)
            }

        ],
        data = initial_cta_df.to_dict('records'),
        style_data_conditional=[{
            'if': {
                'column_id': 'value_pa',
                'filter_query': '{name} != "Totaux"'

            },
            'backgroundColor': '#AFE1AF',
            'border': "1px solid white"

        }]
    )
