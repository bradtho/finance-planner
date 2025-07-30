import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for gunicorn or K8s use

app.layout = dbc.Container([
    html.H2("Financial Planner", className="mt-4"),

    dbc.Row([
        dbc.Col([
            dbc.Label("Annual Pay ($)"),
            dbc.Input(id="input-pay", type="number", value=120000),
            dbc.Label("Superannuation (%)"),
            dbc.Input(id="input-super", type="number", value=10),
            dbc.Label("Mortgage Amount ($)"),
            dbc.Input(id="input-mortgage", type="number", value=500000),
            dbc.Label("Monthly Repayment ($)"),
            dbc.Input(id="input-monthly", type="number", value=3000),
            dbc.Label("Extra Payment ($/month)"),
            dbc.Input(id="input-extra", type="number", value=500),
            dbc.Button("Calculate", id="submit-btn", color="primary", className="mt-3")
        ], width=4),

        dbc.Col([
            dcc.Graph(id="mortgage-chart"),
            html.Div(id="summary-output", className="mt-3")
        ], width=8),
    ])
], fluid=True)

@app.callback(
    Output("mortgage-chart", "figure"),
    Output("summary-output", "children"),
    Input("submit-btn", "n_clicks"),
    State("input-pay", "value"),
    State("input-super", "value"),
    State("input-mortgage", "value"),
    State("input-monthly", "value"),
    State("input-extra", "value"),
)
def update_output(n_clicks, pay, super_rate, mortgage, monthly_payment, extra):
    if n_clicks is None:
        return dash.no_update

    interest_rate = 0.06 / 12  # 6% annual -> monthly
    balance = mortgage
    timeline = []
    balances = []
    month = 0

    while balance > 0 and month < 600:  # cap at 50 years
        interest = balance * interest_rate
        principal = monthly_payment + extra - interest
        balance -= principal
        balance = max(balance, 0)
        balances.append(balance)
        timeline.append(month)
        month += 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeline, y=balances, mode='lines', name='Mortgage Balance'))
    fig.update_layout(title="Mortgage Reduction Over Time", xaxis_title="Months", yaxis_title="Remaining Balance ($)")

    return fig, f"Mortgage paid off in {month} months ({round(month/12, 1)} years) with extra ${extra}/month."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
