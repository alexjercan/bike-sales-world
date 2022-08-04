import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

df = pd.read_csv("Sales.csv")
df["Sales"] = 1
df = df.groupby(["Year", "Country"])["Sales"].count().reset_index()
years = df["Year"].unique()
filter_countries = set()

app.layout = html.Div(
    [
        html.H1("Web Application Dashboards with Dash", style={"text-align": "center"}),
        dcc.Dropdown(
            id="slct_year",
            options=[{"label": i, "value": i} for i in years],
            multi=False,
            value=years[0],
            style={"width": "40%"},
        ),
        html.Div(id="output_container", children=[]),
        html.Br(),
        dcc.Graph(id="my_sales_map", figure={}),
        html.Br(),
        dcc.Graph(
            id="my_australia_sales",
            figure={},
        ),
    ]
)


@app.callback(
    [
        Output(component_id="output_container", component_property="children"),
        Output(component_id="my_sales_map", component_property="figure"),
    ],
    [Input(component_id="slct_year", component_property="value")],
)
def update_graph(option_slctd):
    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df[df["Year"] == option_slctd]

    fig = px.choropleth(
        data_frame=dff,
        locationmode="country names",
        locations="Country",
        scope="world",
        color="Sales",
        hover_data=["Country", "Sales"],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={"Sales": "Sales"},
    )

    return container, fig


@app.callback(
    Output(component_id="my_australia_sales", component_property="figure"),
    [Input(component_id="my_sales_map", component_property="clickData")],
)
def update_graph(click_data):
    if click_data is None:
        return {}

    print(click_data)

    location = click_data["points"][0]["location"]
    if location in filter_countries:
        filter_countries.remove(location)
    else:
        filter_countries.add(location)

    if not filter_countries:
        return {}

    dff = df[df["Country"].isin(filter_countries)]
    fig = px.line(dff, x="Year", y="Sales", color="Country")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
