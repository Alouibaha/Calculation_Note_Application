from aircharts import conf
import dash_html_components as html
import dash_core_components as dcc

def table():
    return html.Table(
        id="ventilation-table",
        children = [
            html.Thead(
                children = [
                    html.Tr(
                        children = [
                            html.Th(
                                children = []
                            ),
                            html.Th(
                                children = ["kW"]
                            )
                        ]
                    )
                ]
            ),
            html.Tbody(
                children = [
                    html.Tr(
                        children = [
                            html.Td(children=["η motor"]),
                            html.Td(children=[
                                dcc.Input(
                                    id='mu-motor',
                                    type="number",
                                    value=conf.initial_mu_motor,
                                    min=0,
                                    max=1000,
                                    step=0.01
                                )
                            ])
                        ]
                    )
                ] + [
                    html.Tr(
                        children = [
                            html.Td(children=[name]),
                            html.Td(
                                id = id,
                                children=[str(initial_value)]
                            )
                        ]
                    )
                    for (id, name, initial_value) in (
                        ('electric-power', 'Electric Power', 6.05),
                        ('consumpt-ahu', 'Consumpt. AHU', 1.99),
                        ('consumpt-network', 'Consumpt. Network', 2.18),
                        ('heat-gains', 'Heat gains', 1.9)
                    )
                ]
            )
        ]
    )
