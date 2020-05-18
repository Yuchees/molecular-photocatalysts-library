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
                html.H1(
                    id='chart-title',
                    children='Small-molecule photocatalysts')
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
                        {'label': '5D explorer', 'value': '5d'},
                        {'label': '2D chemical space', 'value': 'cluster'}
                    ],
                    value='cluster'
                ),
                html.Div(
                    id='color-bar-control',
                    className='dropdown-control',
                    children=[
                        html.H3('Symbol colour:'),
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
                        html.H3('Symbol size:'),
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
                html.P('Dropdown menus for symbol colour, symbol size, '
                       'X, Y, and Z axes are only active for 5D explorer.')
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


def structure_viewer(interactive_data, chart_name):

    def single_3d_viewer(json_file):
        mol_data, style_data = load_json(json_file)
        mol_3d = bio.Molecule3dViewer(
            id='mol-3d-viewer',
            selectionType='atom',
            styles=style_data,
            modelData=mol_data
        )
        return mol_3d

    try:
        if chart_name == '5d':
            index = int(interactive_data['points'][0]['pointNumber'])
            structure_name = df.iloc[index].name
        else:
            index = int(interactive_data['points'][0]['pointIndex'])
            cluster_idx = interactive_data['points'][0]['curveNumber'] + 1
            structure_name = df[df.group == cluster_idx].iloc[index].name
        json_path = './data/json_data/{}.json'.format(structure_name)
    # Default structure
    except TypeError:
        json_path = './data/json_data/340.json'
    return single_3d_viewer(json_path)


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
        colors = {1: 'red', 2: 'purple', 4: 'blue', 5: 'orange',  3: 'green'}
        for cluster in [1, 2, 3, 4, 5]:
            fig.add_trace(go.Scatter(
                x=df[df.group == cluster].loc[:, 'pos_0'],
                y=df[df.group == cluster].loc[:, 'pos_1'],
                mode='markers',
                text=df[df.group == cluster].iloc[:, 0],
                name=cluster,
                marker=dict(
                    symbol='circle',
                    opacity=0.5,
                    color=colors[int(cluster)],
                    line=dict(color='white', width=1),
                    size=df[df.group == cluster].iloc[:, 0] + 8
                )
            ))
        fig.update_layout(
            clickmode='event',
            hovermode='closest',
            hoverdistance=-1,
            title=dict(
                text='2D UMAP embeddings of SOAP+REMatch chemical space',
                font=dict(family='Arial', size=20),
                y=0.95
            ),
            xaxis=axis_template,
            yaxis=axis_template,
            showlegend=True,
            legend=dict(
                font=dict(family='Arial'),
                itemsizing='constant'
            ),
            margin={'t': 55, 'b': 10, 'l': 30},
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
                marker=dict(
                    size=size,
                    color=df[colour_column_value],
                    colorbar=dict(
                        thicknessmode='pixels',
                        thickness=25,
                        title=dict(
                            text=colour_column_value,
                            side='right'
                        )
                    ),
                    colorscale='RdBu',
                    reversescale=True,
                    showscale=True
                )
            )
        )
        fig.update_layout(
            title=dict(
                text='5D explorer of hydrogen evolution activity '
                     'and molecular properties',
                font=dict(family='Arial', size=20),
                y=0.95
            ),
            scene=dict(
                xaxis={'title': x_axis_column_name, 'zeroline': True},
                yaxis={'title': y_axis_column_name, 'zeroline': True},
                zaxis={'title': z_axis_column_name, 'zeroline': True},
            ),
            margin={'t': 55, 'b': 10, 'l': 30},
            font=dict(family='Arial'),
            width=800,
            height=600
        )
    return fig


@app.callback(dash.dependencies.Output('loading_hover', 'children'),
              [dash.dependencies.Input('clickable_plot', 'hoverData'),
               dash.dependencies.Input('chart_type', 'value')])
def display_hover_image(hoverData, chart_type_value):
    return structure_viewer(interactive_data=hoverData,
                            chart_name=chart_type_value)


@app.callback(dash.dependencies.Output('loading_selected', 'children'),
              [dash.dependencies.Input('clickable_plot', 'clickData'),
               dash.dependencies.Input('chart_type', 'value')])
def display_selected_data(clickData, chart_type_value):
    return structure_viewer(interactive_data=clickData,
                            chart_name=chart_type_value)


if __name__ == '__main__':
    app.run_server(debug=True)
