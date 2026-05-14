"""Build the radar/spider chart for player comparison."""
import plotly.graph_objects as go

from .config import LINE_COLORS


def build_radar(players_data: list, stat_labels: list) -> go.Figure:
    """Build a radar chart comparing the given players."""
    fig = go.Figure()

    for i, player_data in enumerate(players_data):
        # get percentile values in the right order
        values = [player_data['percentile'][label] for label in stat_labels]
        # repeat the first point to close the shape
        values_closed = values + [values[0]]
        labels_closed = stat_labels + [stat_labels[0]]

        color = LINE_COLORS[i]

        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            mode='lines+markers',
            name=player_data['player'],
            line=dict(color=color, width=2.5),
            marker=dict(color=color, size=8),
            fill='none',
            hovertemplate=(
                '<b>%{fullData.name}</b><br>'
                '%{theta}: %{r:.0f}th percentile<extra></extra>'
            ),
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[20, 40, 60, 80, 100],
                ticktext=['20', '40', '60', '80', '100'],
                gridcolor='#E5E5E5',
                tickfont=dict(size=10, color='#999'),
            ),
            angularaxis=dict(
                gridcolor='#E5E5E5',
                tickfont=dict(size=13, color='#333'),
            ),
            bgcolor='white',
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5,
            font=dict(size=12),
        ),
        margin=dict(l=80, r=80, t=40, b=80),
        height=550,
        paper_bgcolor='white',
    )

    return fig
