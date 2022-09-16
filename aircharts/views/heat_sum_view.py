import dash_html_components as html
import dash_core_components as dcc

def table():
    return html.Table(
        id="heat-sum-table",
        children = [
            html.Thead(
                children = [
                    html.Tr(
                        children = [
                            html.Th(
                                children = ["Heat gains"]
                            ),
                            html.Th(
                            ),
                            html.Th(
                                children = ["kW"],
                                id = "th-unit-heat-sums"
                            )
                        ]
                    )
                ]
            ),
            html.Tbody(
                children = [
                    html.Tr(
                        children = [
                            html.Td(children=["From people"]),
                            html.Td(
                                children=[
                                    dcc.Input(
                                        id="n-persons",
                                        type="number",
                                        min=0,
                                        step=1,
                                        value=8
                                    ),
                                    " persons"
                                ]
                            ),
                            html.Td(id="subtotal-heat-people")
                        ]
                    ),
                    html.Tr(
                        children = [
                            html.Td(children=["From equipment"]),
                            html.Td(),
                            html.Td(
                                id="subtotal-heat-equipment",
                            )
                        ]
                    ),
                    html.Tr(
                        children = [
                            html.Td(children=["From ambiant lighting"]),
                            html.Td(),
                            html.Td(
                                id="subtotal-heat-light",
                            )
                        ]
                    ),
                    html.Tr(
                        children = [
                            html.Td(children=["From ventilation"]),
                            html.Td(),
                            html.Td(
                                id="subtotal-heat-ventilation",
                            )
                        ]
                    ),
                    html.Tr(
                        children = [
                            html.Td(children=["Global dissipation (total)"]),
                            html.Td(),
                            html.Td(
                                id="total-heat-dissipation",
                            )
                        ]
                    )

                ]
            )
        ]
    )
