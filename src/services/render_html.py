from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go


app_layout = html.Div(
    [
        html.H1("Прогноз погоды по городам"),
        html.Div(
            id="input-container",
            children=[
                dcc.Input(id="location-0", type="text", placeholder="Введите название города"),
                dcc.Input(id="location-1", type="text", placeholder="Введите название города"),
            ],
        ),
        html.Button("Добавить новый город", id="add-location-btn", n_clicks=0),
        html.Button("Удалить город", id="delete-location-btn", n_clicks=0),
        html.Button("Получить данные о погоде на день", id="fetch-weather-btn", n_clicks=0, value="1212121"),
        html.Button("Получить данные о погоде на 5 дней", id="fetch-weather-btn-5", n_clicks=0),
        html.Button("Получить данные о погоде на 10 дней", id="fetch-weather-btn-10", n_clicks=0),
        html.Button("Получить данные о погоде на 15 дней", id="fetch-weather-btn-15", n_clicks=0),
        dcc.Graph(id="weather-chart"),
        html.Div(id="error-display", style={"color": "red"}),
    ]
)


def generate_city_input(index: int) -> dcc.Input:
    return dcc.Input(
        id=f"location-{index}",
        type="text",
        placeholder="Введите название города",
    )


def create_line_chart(data: pd.DataFrame, value_column: str, chart_title: str, line_color: str, dashed: bool = False) -> go.Scatter:
    line_style = {"color": line_color}
    
    if dashed:
        line_style["dash"] = "dash"
    return go.Scatter(
        x=data["date"],
        y=data[value_column],
        mode="lines+markers",
        name=chart_title,
        line=line_style,
    )
