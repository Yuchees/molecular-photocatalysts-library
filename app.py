# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive 2D molecular structure visualisation application
Using T-SNE for dimensionality reduction
@author: Yu Che
"""
import dash
import dash_bio as bio
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from utils import load_json

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('./data/electronic_features.csv', index_col='ID')
columns_dict = [{'label': i, 'value': i} for i in df.columns[:12]]
size_dict = columns_dict + [{'label': 'Constant', 'value': 5}]
axis_template = dict(
    showgrid=False,
    zeroline=False,
    showline=False,
    showticklabels=False,
)

app.layout = html.Div(
    id='main',
    className='app_main',
    children=[
        # Dash title and icon
        html.Div(
            id='mol3d-title',
            children=[
                html.Img(
                    id='dash-logo',
                    src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/"
                        "logo/new-branding/dash-logo-by-plotly-stripe.png"
                ),
                html.H1(id='chart-title', children='Photo catalysis libraries')
            ]
        ),
        # Dash graph
        dcc.Graph(id='clickable_plot'),
        # Axises controller
        html.Div(
            id='plot-controller',
            children=[
                dcc.RadioItems(
                    id='chart_type',
                    options=[
                        {'label': '5D scatter chart', 'value': '5d'},
                        {'label': 'SOAP cluster chart', 'value': 'cluster'}
                    ],
                    value='cluster'
                ),
                html.Div(
                    id='color-bar-control',
                    className='dropdown-control',
                    children=[
                        html.H3('Colour bar:'),
                        dcc.Dropdown(
                            id='colour_column',
                            options=columns_dict,
                            value='Hydrogen evolution rate / µmol/h'
                        )
                    ]
                ),
                html.Div(
                    id='size-control',
                    className='dropdown-control',
                    children=[
                        html.H3('Size:'),
                        dcc.Dropdown(
                            id='size_column',
                            options=size_dict,
                            value=5
                        )
                    ]
                ),
                html.Div(
                    id='x-axis',
                    className='dropdown-control',
                    children=[
                        html.H3('X-axis:'),
                        dcc.Dropdown(
                            id='x_axis_column',
                            className='axis_controller',
                            options=columns_dict,
                            value='IP / V vs. SHE'
                        )
                    ]
                ),
                html.Div(
                    id='y-axis',
                    className='dropdown-control',
                    children=[
                        html.H3('Y-axis:'),
                        dcc.Dropdown(
                            id='y_axis_column',
                            className='axis_controller',
                            options=columns_dict,
                            value='EA / V vs. SHE'
                        )
                    ]
                ),
                html.Div(
                    id='z-axis',
                    className='dropdown-control',
                    children=[
                        html.H3('Z-axis:'),
                        dcc.Dropdown(
                            id='z_axis_column',
                            className='axis_controller',
                            options=columns_dict,
                            value='S1T1 / eV'
                        )
                    ]
                ),
                html.P('The  colour, size, X, Y and Z axis controller are '
                       'disabled when choose cluster chart.')
            ]
        ),
        html.Div(
            id='hover_structure',
            children=[
                html.H3(className='viewer-title', children='Hover structure:'),
                dcc.Loading(id='loading_hover', className='loading')
            ]),
        html.Div(
            id='selected_structure',
            children=[
                html.H3(className='viewer-title', children='Selected structure:'),
                dcc.Loading(id='loading_selected', className='loading')
            ])
    ]
)


def structure_viewer(interactive_data, chart_name, click_data=None):

    def single_3d_viewer(json_file):
        mol_data, style_data = load_json(json_file)
        mol_3d = bio.Molecule3dViewer(
            id='mol-3d-viewer',
            selectionType='atom',
            styles=style_data,
            modelData=mol_data
        )
        return mol_3d

    mol_div = []
    try:
        for i in range(len(interactive_data['points'])):
            if chart_name == '5d':
                print(click_data)
                index = int(interactive_data['points'][i]['pointNumber'])
                structure_name = df.iloc[index].name
            else:
                print(interactive_data)
                index = int(interactive_data['points'][i]['pointIndex'])
                cluster_idx = interactive_data['points'][i]['curveNumber']
                structure_name = df[df.group == cluster_idx].iloc[index].name
            json_path = './data/json_data/{}.json'.format(structure_name)
            mol_div.append(single_3d_viewer(json_path))
    # Default structure
    except TypeError:
        json_path = './data/json_data/340.json'
        mol_div.append(single_3d_viewer(json_path))
    return mol_div


@app.callback(
    dash.dependencies.Output('clickable_plot', 'figure'),
    [dash.dependencies.Input('chart_type', 'value'),
     dash.dependencies.Input('x_axis_column', 'value'),
     dash.dependencies.Input('y_axis_column', 'value'),
     dash.dependencies.Input('z_axis_column', 'value'),
     dash.dependencies.Input('colour_column', 'value'),
     dash.dependencies.Input('size_column', 'value')]
)
def update_graph(chart_type_value, x_axis_column_name, y_axis_column_name,
                 z_axis_column_name, colour_column_value, size_column_value):
    fig = go.Figure()
    if chart_type_value == 'cluster':
        for cluster in range(5):
            fig.add_trace(go.Scatter(
                x=df[df.group == cluster].loc[:, 'pos_0'],
                y=df[df.group == cluster].loc[:, 'pos_1'],
                mode='markers',
                text=df[df.group == cluster].iloc[:, 0],
                name=cluster,
                marker=dict(size=df[df.group == cluster].iloc[:, 0] + 5)
            ))
        fig.update_layout(
            clickmode='event+select',
            xaxis=axis_template,
            yaxis=axis_template,
            showlegend=True,
            width=800,
            height=600
        )
    elif chart_type_value == '5d':
        if isinstance(size_column_value, int):
            size = 5
        else:
            size = df.loc[:, size_column_value] + 8
        fig.add_trace(
            go.Scatter3d(
                x=df[x_axis_column_name],
                y=df[y_axis_column_name],
                z=df[z_axis_column_name],
                mode='markers',
                marker={'size': size,
                        'color': df[colour_column_value],
                        'colorbar': {'title': colour_column_value},
                        'colorscale': 'RdBu',
                        'showscale': True}
            )
        )
        fig.update_layout(
            title='5D scatter graph',
            scene=dict(
                xaxis={'title': x_axis_column_name, 'zeroline': True},
                yaxis={'title': y_axis_column_name, 'zeroline': True},
                zaxis={'title': z_axis_column_name, 'zeroline': True},
            ),
            width=800,
            height=600
        )
    return fig


@app.callback(dash.dependencies.Output('hover_structure', 'children'),
              [dash.dependencies.Input('clickable_plot', 'hoverData'),
               dash.dependencies.Input('chart_type', 'value')])
def display_hover_image(hoverData, chart_type_value):
    return structure_viewer(interactive_data=hoverData,
                            chart_name=chart_type_value)


@app.callback(dash.dependencies.Output('selected_structure', 'children'),
              [dash.dependencies.Input('clickable_plot', 'selectedData'),
               dash.dependencies.Input('clickable_plot', 'clickData'),
               dash.dependencies.Input('chart_type', 'value')])
def display_selected_data(selectedData, clickData, chart_type_value):
    return structure_viewer(interactive_data=selectedData,
                            click_data=clickData,
                            chart_name=chart_type_value)


if __name__ == '__main__':
    app.run_server(debug=True)
