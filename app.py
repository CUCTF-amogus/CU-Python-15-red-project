from dash import Dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from config.config import Config, load_config
from src.services.weather import Weather
from src.services import render_html


app = Dash(__name__)
app.layout = render_html.app_layout
colors = px.colors.qualitative.Plotly


@app.callback(
    Output("input-container", "children", allow_duplicate=True),
    Input("add-location-btn", "n_clicks"),
    State("input-container", "children"),
    prevent_initial_call=True,
)
def add_location_input(n_clicks, children):
    if n_clicks > 0:
        children.append(render_html.generate_city_input(n_clicks))
    return children


@app.callback(
    Output("input-container", "children", allow_duplicate=True),
    Input("delete-location-btn", "n_clicks"),
    State("input-container", "children"),
    prevent_initial_call=True,
)
def delete_location_input(n_clicks, children):
    if n_clicks > 0:
        children.pop(-1)
    return children


@app.callback(
    Output("weather-chart", "figure"),
    Output("error-display", "children"),
    Input("fetch-weather-btn", "n_clicks"),
    Input("input-container", "children"),
)
def update_chart(n_clicks, location_inputs):
    if n_clicks <= 0:
        return go.Figure(), ""

    dataFrames = []
    error_messages = []
    location_names = []
    for input_component in location_inputs:
        if "props" in input_component.keys() and "value" in input_component["props"].keys():
            location_names.append(input_component["props"]["value"])
        else:
            input_id = input_component.get("props", {}).get("id", "ID не найден")
            error_messages.append(f"Город {input_id} не найден")

    weather_api = Weather()
    for location_name in location_names:
        try:
            from_location_weathers = weather_api.get_weather(location_name)
        except Exception as e:
            error_messages.append(f"Ошибка для города '{location_name}': {e}")
            continue

        dataFrames.append(pd.DataFrame(from_location_weathers))

    fig = go.Figure()

    for i, (df, location) in enumerate(zip(dataFrames, location_names)):
        color = colors[i % len(colors)]
        fig.add_trace(
            render_html.create_line_chart(
                df,
                "temperature_avg",
                f"Средняя температура в {location}",
                color,
            )
        )
        

    fig.update_layout(
        title="Прогноз погоды на 5 дней",
        xaxis_title="Дата",
        yaxis_title="Температура (°C)",
        legend_title="Города",
    )

    return fig, " и ".join(error_messages)


if __name__ == "__main__":
    app.run_server(debug=True)
