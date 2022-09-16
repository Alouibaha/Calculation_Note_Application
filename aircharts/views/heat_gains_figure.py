import plotly.express as px

blue = '#006db0'

def figure(people, equipments, lighting, ventilation):
    total = people + equipments + lighting + ventilation
    people, equipments, lighting, ventilation = (
        x*100.0/total for x in (
            people, equipments, lighting, ventilation
        )
    )
    fig = px.bar(
        x = ["People", "Equipments", "Lighting", "Ventilation"],
        y = [people, equipments, lighting, ventilation],
        labels = {
            "x": "",
            "y": "Subdivision (%)"
        },
        title = "Heat gains"
    )
    fig.update_traces(marker_color=blue)
    return fig
