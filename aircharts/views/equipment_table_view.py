from aircharts import equipment_gains
import dash_table
from dash_table.Format import Format, Scheme

initial_equipment_df = equipment_gains.full_df(
    equipment_gains.initial_equipment_gains,
    len(equipment_gains.initial_equipment_gains.index)
)

def table():
    return dash_table.DataTable(
        columns = [
            {
                "id": "equipment",
                "name": "Equipments",
                "editable": True
            },
            {
                "id": "heat_gains_w",
                "name": "Heat gains W",
                "editable": True,
                "type": "numeric",
                "format":Format(precision=1, scheme=Scheme.fixed)
            },
            {
                "id": "qty",
                "name": "Qty",
                "editable":True,
                "type": "numeric"
            },
            {
                "id": "kw",
                "name": "kW",
                "type": "numeric",
                "format":Format(precision=2, scheme=Scheme.fixed)
            }
        ],
        id = 'equipment-gain-table',
        data = initial_equipment_df.to_dict('records'),
        style_data_conditional=[{
            'if': {
                'column_id': 'heat_gains_w'
            },
            'backgroundColor': '#AFE1AF',
            'border': "1px solid white"

        }]
    )
