#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive 2D molecular structure visualisation application
Using T-SNE for dimensionality reduction
@author: Yu Che
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash(__name__)
server = app.server

df = pd.read_pickle('./computed_data.pkl')
axis_template = dict(
    showgrid=False,
    zeroline=False,
    showline=False,
    showticklabels=False,
)
app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='clickable_plot',
            style={'float': 'left', 'display': 'inline-block'}
        ),
        dcc.RadioItems(
            id='cluster_name',
            options=[
                {'label': '3', 'value': 3},
                {'label': '4', 'value': 4},
                {'label': '5', 'value': 5},
                {'label': '6', 'value': 6},
                {'label': '7', 'value': 7},
                {'label': '8', 'value': 8},
                {'label': '9', 'value': 9},
                {'label': '10', 'value': 10},
                {'label': '11', 'value': 11},
                {'label': '12', 'value': 12},
                {'label': '13', 'value': 13},
                {'label': '14', 'value': 14},
                {'label': '15', 'value': 15},
                {'label': '16', 'value': 16},
                {'label': '17', 'value': 17},
                {'label': '18', 'value': 18},
                {'label': '19', 'value': 19},
                {'label': '20', 'value': 20},
                {'label': '25', 'value': 25},
                {'label': '29', 'value': 29}
            ],
            value=10
        )
    ]),
    html.Div([
        html.H3('Hover molecule:'),
        html.Div(id='hover_molecule'),
        html.H3('Selected molecules:'),
        html.Div(id='selected_molecule')],
        style={'display': 'inline-block'}
    )
])


def images_component(data, cluster_name):
    html_images = []

    def html_image(name):
        one_image = html.Img(
            src='https://res.cloudinary.com/yucheimages/image/upload'
                '/c_crop,g_west,h_300,w_300'
                '/v1585751604/572_dataset/{}.png'.format(name),
            style={'width': '300px', 'height': '300px'}
        )
        return one_image

    cluster_series = df['kmeans_{}'.format(cluster_name)]
    try:
        number_molecules = len(data['points'])
        print(data)
        for i in range(number_molecules):
            index = int(data['points'][i]['pointIndex'])
            label_idx = data['points'][i]['curveNumber']
            idx = df[cluster_series == label_idx].iloc[index].name
            print(idx)
            html_images.append(html_image(idx))
    except TypeError:
        html_images.append(html_image('807'))
    return html.Div(html_images)


@app.callback(
    dash.dependencies.Output('clickable_plot', 'figure'),
    [dash.dependencies.Input('cluster_name', 'value')]
)
def update_graph(cluster_name_value):
    cluster_series = df['kmeans_{}'.format(cluster_name_value)]
    fig = go.Figure()
    for label in range(cluster_name_value):
        fig.add_trace(go.Scatter(
            x=df[cluster_series == label].loc[:, 'umap_soap_pos0'],
            y=df[cluster_series == label].loc[:, 'umap_soap_pos1'],
            mode='markers',
            text=df[cluster_series == label].loc[:, 'HER'],
            name=label,
            marker=dict(size=df[cluster_series == label].loc[:, 'HER'] + 5)
        ))
    fig.update_layout(
        clickmode='event+select',
        title='SOAP distance matrix only, '
              'using UMAP and KMeans algorithms',
        hovermode='closest',
        xaxis=axis_template,
        yaxis=axis_template,
        showlegend=True,
        width=800,
        height=600
    )
    return fig


@app.callback(dash.dependencies.Output('hover_molecule', 'children'),
              [dash.dependencies.Input('clickable_plot', 'hoverData'),
               dash.dependencies.Input('cluster_name', 'value')])
def display_hover_image(hoverData, cluster_name_value):
    return images_component(hoverData, cluster_name_value)


@app.callback(dash.dependencies.Output('selected_molecule', 'children'),
              [dash.dependencies.Input('clickable_plot', 'selectedData'),
               dash.dependencies.Input('cluster_name', 'value')])
def display_selected_data(selectedData, cluster_name_value):
    return images_component(selectedData, cluster_name_value)


if __name__ == '__main__':
    app.run_server(debug=True)
