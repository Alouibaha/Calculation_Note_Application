from aircharts import seasons_tables
from aircharts.altitude_to_pressure import altitude_to_pressure
import base64
import io
import psychrochart

def style(altitude_m):
    return {
         "figure": {
             "figsize": [12, 8],
             "base_fontsize": 12,
             "title": "",
             "x_label": "°C",
             "y_label": "g/kgas",
             "partial_axis": False
         },
         "saturation": {"color": [0, .3, 1.], "linewidth": 2},
         "constant_rh": {
             "color": [0.0, 0.498, 1.0, .7], "linewidth": 2.5,
             "linestyle": ":"
         },
         "limits": {
             "range_temp_c": [-15, 50],
             "range_humidity_g_kg": [0, 30],
             "altitude_m": altitude_m,
             "step_temp": .5
         },
         "chart_params": {
             "with_constant_rh": True,
             "constant_rh_curves": [25, 50, 75],
             "constant_rh_labels": [25, 50, 75],
             "with_constant_v": True,
             "with_constant_h": False,
             "with_constant_wet_temp": True,
             "with_zones": False
         }
    }


def build_figure(summer_data, winter_data, altitude, psychrochart_style = style):

    pressure = altitude_to_pressure(altitude)

    summer_df = seasons_tables.full_df(
        summer_data, pressure, dew_point =  True
    )
    winter_df = seasons_tables.full_df(winter_data, pressure)

    buf = io.BytesIO()
    chart = psychrochart.PsychroChart(
        style(altitude),
        use_unit_system_si=True
    )

    ax = chart.plot()

    points = {}
    connectors = []
    ambiant_color = [0.016, 0.216, 0.949]
    fresh_color = [0.031, 0.094, 0.659]
    mixed_color = [1.0, 0.498, 0.314, 1.0]
    connector_color = [0.118, 0.518, 0.89, 1.0]
    blowing_color = [0.255, 0.412, 0.882, 1.0]
    # https://matplotlib.org/stable/api/markers_api.html
    for prefix, markers, caption, df in (
        ('summer_', ('o', 'o', 'o'), '', summer_df),
        ('winter_', ('X', 'X', 'X') , '', winter_df)

    ):
        for _, row in df.iterrows():
            points[prefix + 'fresh_air'] = {
                'label': 'Fresh air' + caption,
                'style': {
                    'color': fresh_color,
                    'marker': markers[0],
                    'markersize': 15
                },
                'xy': (
                    df.loc['Fresh air', 'TDryBulb'],
                    df.loc['Fresh air', 'RelHumPercent']
                )
            }
            points[prefix + 'ambiant_air'] = {
                'label': 'Ambiant air' + caption,
                'style': {
                    'color': ambiant_color,
                    'marker': markers[2],
                    'markersize': 15
                },
                'xy': (
                    df.loc['Ambiant air', 'TDryBulb'],
                    df.loc['Ambiant air', 'RelHumPercent']
                )
            }
            points[prefix + 'mixed_air'] = {
                'label': 'Mixed air' + caption,
                'style': {
                    'color': mixed_color,
                    'marker': markers[1],
                    'markersize': 15
                },
                'xy': (
                    df.loc['Mixed air', 'TDryBulb'],
                    df.loc['Mixed air', 'RelHumPercent']
                )
            }
            connectors.append(
                {
                    'start': prefix + 'ambiant_air',
                    'end': prefix + 'fresh_air',
                    'style': {
                        'color': connector_color,
                        "linewidth": 1, "linestyle": "-"
                    }
                }
            )
    points['blowing_air'] = {
        'label': 'Blowing air',
        'style': {
            'color': blowing_color,
            'marker': 'H',
            'markersize': 15
        },
        'xy': (
            summer_df.loc['Blowing air', 'TDryBulb'],
            summer_df.loc['Blowing air', 'RelHumPercent']
        )
    }

    chart.plot_points_dbt_rh(points, connectors)

    chart.plot_legend(markerscale=.7, frameon=False, fontsize=10, labelspacing=1.2)

    ax.get_figure().savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('utf-8')
    return "data:image/png;base64,{}".format(data)
