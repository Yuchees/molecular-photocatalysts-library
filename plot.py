import plotly.graph_objs as go
import pandas as pd

axis_template = dict(
    showgrid=False,
    zeroline=False,
    showline=False,
    showticklabels=False,
)


def cluster_plot(fig, df):
    colors = {1: 'red', 2: 'purple', 4: 'blue', 5: 'orange', 3: 'green'}
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
                size=df[df.group == cluster].iloc[:, 3] + 10
            )
        ))
    fig.update_layout(
        clickmode='event+select',
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
            font=dict(family='Arial', size=16),
            itemsizing='constant'
        ),
        margin={'t': 55, 'b': 10, 'l': 30},
        width=800,
        height=600
    )
    return fig


def multi_plot(fig, df, x_axis_column_name, y_axis_column_name,
               z_axis_column_name, size_column_value, colour_column_value):
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
            text=df.iloc[:, 0],
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
        clickmode='event+select',
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


def val_plot(fig, df):
    fig.add_trace(go.Scatter(
        x=df.loc[:816, 'b3lypsoapval_pos0'],
        y=df.loc[:816, 'b3lypsoapval_pos1'],
        mode='markers',
        name='572-molecule library',
        text=df.loc[:816, 'ID in paper'],
        marker=dict(
            symbol='circle',
            opacity=0.5,
            color='blue',
            line=dict(color='white', width=1),
            size=df.loc[:816, 'Hydrogen evolution rate / µmol/h'] * 1.5 + 10
        )
    ))
    fig.add_trace(go.Scatter(
        x=df.loc[816:, 'b3lypsoapval_pos0'],
        y=df.loc[816:, 'b3lypsoapval_pos1'],
        mode='markers',
        name='Blind test',
        text=df.loc[816:, 'ID in paper'],
        marker=dict(
            symbol='circle',
            opacity=0.8,
            color='red',
            line=dict(color='white', width=1),
            size=df.loc[816:, 'Hydrogen evolution rate / µmol/h'] * 1.5 + 10
        )
    ))
    fig.update_layout(
        clickmode='event+select',
        hovermode='closest',
        hoverdistance=-1,
        title=dict(
            text='2D UMAP embeddings of the chemical space of the '
                 '572-molecule library and blind tests set',
            font=dict(family='Arial', size=18),
            y=0.95
        ),
        xaxis=axis_template,
        yaxis=axis_template,
        showlegend=True,
        legend=dict(
            font=dict(family='Arial', size=16),
            itemsizing='constant',
            bgcolor='rgba(0,0,0,0)',
            x=0.005, y=0.99
        ),
        margin={'t': 55, 'b': 10, 'l': 30},
        width=800,
        height=600
    )
    return fig
