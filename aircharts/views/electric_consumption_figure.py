import plotly.graph_objs as go

blue = '006db0'
gray = 'c4c3d0'
orange = 'ff7e50'

def figure(cta_ahu_consumpt, return_network_consumpt, supply_network_consumpt):
    pie = go.Pie(
        hole = 0.1,
        values = (
            cta_ahu_consumpt,
            return_network_consumpt,
            supply_network_consumpt
        ),
        labels = (
            "Consumpt. CTA / AHU",
            "Consumpt. Air return",
            "Consumpt. Supply network"
        ),
        marker = {
            'colors': [blue, gray, orange],
            'line': {'color': 'white', 'width': 5}
        }
    )
    layout = go.Layout(title = "Electric consumption subdivision")
    return go.Figure(data = [pie], layout = layout)
