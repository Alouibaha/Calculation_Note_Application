from aircharts.views import (
    general_parameters, seasons_tables_views, ventilation_view,
    cta_table_view, equipment_table_view, heat_sum_view, networks_tables_views
)
import dash_html_components as html
import dash_core_components as dcc


def div(app):
    return html.Div(
        id="main",
        children = [
            general_parameters.div(),
            html.Div(
                children = [
                    html.H2(
                        "Estimation of Losses of pressure for fan motor calculation",
                        className="title padded"
                    ),
                    html.Div(
                        className = "aircharts-row",
                        children = [
                            html.Div(
                                className = "aircharts-col padded",
                                children = [
                                    html.P(
                                        "1.CTA / AHU",
                                        className = "subtitle"
                                    ),
                                    cta_table_view.table()
                                ]
                            ),
                            html.Div(
                                className = "aircharts-col padded",
                                children = [
                                    html.P(
                                        "2.Return network",
                                        className = "subtitle"
                                    ),
                                    networks_tables_views.return_network_table()
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className = "aircharts-row",
                        children = [
                            html.Div(
                                className = "aircharts-col padded",
                                children = [
                                    html.P(
                                        "3.Supply network",
                                        className = "subtitle"
                                    ),
                                    networks_tables_views.supply_network_table()
                                ]
                            ),
                            html.Div(
                                className = "aircharts-col padded",
                                children = [
                                    html.P(
                                        "4.Ventilation",
                                        className = "subtitle"
                                    ),
                                    ventilation_view.table()
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className = "aircharts-row",
                        id = "electric-consumption-row",
                        children = [
                            dcc.Graph(
                                id="electric-consumption-graph",
                                config={
                                    'displayModeBar': False
                                }
                            )
                        ]
                    ),
                    html.H2(
                        "Heat gains: Equipment - People - Light",
                        className="title padded"
                    ),
                    html.Div(
                        className = "aircharts-row",
                        children = [
                            html.Div(
                                className = "aircharts-col padded",
                                children = [
                                    equipment_table_view.table(),
                                    html.Br(),
                                    html.Button(
                                        "+",
                                        id="equipment-add-row",
                                    ),
                                    html.Button(
                                        "-",
                                        id="equipment-del-row",
                                    )
                                ]
                            ),
                            html.Div(
                                className = "aircharts-col padded",
                                children = [
                                    heat_sum_view.table()
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className = 'aircharts-row',
                        children = [
                            html.Div(
                                className = 'aircharts-col padded',
                                children = [
                                    dcc.Graph(
                                        id="heat-gains-graph",
                                        config={
                                            'displayModeBar': False
                                        }
                                    )
                                ]
                            ),
                            html.Div(
                                className = 'aircharts-col'
                            )
                        ]
                    ),
                    html.H2(
                        'Psychrometric point for power sizing : "Heat - Cold- Steam"',
                        className="title padded"
                    ),
                    html.Div(
                        className = "aircharts-row",
                        children = [
                            html.Div(
                                className = "aircharts-col padded",
                                children = [
                                    html.P(
                                        className="subtitle",
                                        children = [
                                            "Summer operating",
                                            html.Img(
                                                src= app.get_asset_url("sunny-outline.png"),
                                                width="30px",
                                                className="margin-sun"
                                            )
                                        ]
                                    ),
                                    seasons_tables_views.summer_table(),
                                    html.Br(),
                                    html.P(
                                        className="subtitle",
                                        children = [
                                            "Winter operating",
                                            html.Img(
                                                src= app.get_asset_url("snow-outline.png"),
                                                width="30px",
                                                className="margin-snow"
                                            )
                                        ]
                                    ),
                                    seasons_tables_views.winter_table()
                                ]
                            ),
                            html.Div(
                                className = "aircharts-col padded",
                                children = [html.Img(id="psychrograph-img")]
                            )
                        ]
                    )
                ]
            )
        ]
    )
