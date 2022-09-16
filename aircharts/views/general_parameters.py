from aircharts.views.common import editable_cell_style
from aircharts import conf
import dash_html_components as html
import dash_table
from dash_table.Format import Format, Scheme

initial_parameters = {
    "altitude": conf.initial_altitude,
    "area": conf.initial_area,
    "air-blowing-flow": conf.initial_air_blowing_flow,
    "people-heat-gains": conf.initial_people_heat_gains,
    "lighting-heat-gains": conf.initial_lighting_heat_gains
}

def div():
    return html.Div(
        id="general-parameters",
        children = [
            html.H2('General parameters', className="title padded"),
            html.Div(
                className = "aircharts-row",
                children = [
                    html.Div(
                        className = "aircharts-col padded",
                        children = [
                            dash_table.DataTable(
                                id = "general-parameters-table",
                                columns = [
                                    {
                                        "name": "Altitude of the site (m)",
                                        "id": "altitude",
                                        "editable": True,
                                        "type": "numeric",
                                        "format":Format(precision=0, scheme=Scheme.fixed)
                                    },
                                    {
                                        "name": "Area (m²)",
                                        "id": "area",
                                        "editable": True,
                                        "type": "numeric",
                                        "format": Format(precision=2, scheme=Scheme.fixed)
                                    },
                                    {
                                        "name": "Air blowing flow (m³/h)",
                                        "id": "air-blowing-flow",
                                        "editable": True,
                                        "type": "numeric",
                                        "format": Format(precision=0, scheme=Scheme.fixed)
                                    },
                                    {
                                        "name": "People heat gains (w/person)",
                                        "id": "people-heat-gains",
                                        "editable": True,
                                        "type": "numeric",
                                        "format": Format(precision=0, scheme=Scheme.fixed)
                                    },
                                    {
                                        "name": "Lighting heat gains (w/m²)",
                                        "id": "lighting-heat-gains",
                                        "editable": True,
                                        "type": "numeric",
                                        "format": Format(precision=0, scheme=Scheme.fixed)
                                    }
                                ],
                                data = [initial_parameters],
                                style_data_conditional=[editable_cell_style]
                            )
                        ]
                    ),
                    html.Div(
                        className = "aircharts-col padded contents-1-3",
                        children = [
                            dash_table.DataTable(
                                id = "pressure-table",
                                columns = [
                                    {
                                        "name": "Atmospheric pressure of the site (Pa)",
                                        "id": "pressure",
                                        "editable": False,
                                        "type": "numeric",
                                        "format":Format(precision=5, scheme=Scheme.fixed)
                                    }
                                ],
                                data = [{"pressure": conf.initial_pressure}]
                            )
                        ]
                    )
                ]
            )
        ]
    )
