"""Football player comparison dashboard. Run with: streamlit run app.py"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# makes src importable no matter where you run streamlit from
sys.path.insert(0, str(Path(__file__).parent))

from src.config import LINE_COLORS, MAX_PLAYERS, MIN_90S, POSITION_CONFIG
from src.data_loader import filter_by_position, load_players
from src.radar_chart import build_radar
from src.stats import compute_per90, get_player_stats


# page setup
st.set_page_config(
    page_title='Football Player Comparison',
    page_icon='⚽',
    layout='centered',
)


# session state
def init_state():
    st.session_state.setdefault('screen', 'home')      # home or compare
    st.session_state.setdefault('position', None)      # DF, MF, or FW
    st.session_state.setdefault('selected_players', [])

init_state()


def go_home():
    """Go back to the home screen and clear everything."""
    st.session_state.screen = 'home'
    st.session_state.position = None
    st.session_state.selected_players = []


def select_position(pos: str):
    st.session_state.position = pos
    st.session_state.screen = 'compare'
    st.session_state.selected_players = []


def remove_player(player_name: str):
    st.session_state.selected_players = [
        p for p in st.session_state.selected_players if p != player_name
    ]


# load data (cached so it doesn't reload on every rerun)
@st.cache_data
def get_data() -> pd.DataFrame:
    return load_players()


df = get_data()


# header
header_left, header_right = st.columns([5, 1])
with header_left:
    st.markdown('## ⚽ Football Player Comparison')
    st.caption('2025/26 season · Big 5 European leagues')
with header_right:
    if st.session_state.screen != 'home':
        st.write('')  # nudge the button down to align with the title
        if st.button('🏠 Home', use_container_width=True):
            go_home()
            st.rerun()

st.divider()


# home screen — pick a position
if st.session_state.screen == 'home':
    st.markdown('### Choose a position to start')
    st.write('')

    cols = st.columns(3)
    for col, pos_key in zip(cols, ['DF', 'MF', 'FW']):
        cfg = POSITION_CONFIG[pos_key]
        with col:
            label = f"{cfg['icon']}\n\n**{cfg['display_name']}**"
            if st.button(label, use_container_width=True, key=f'btn_{pos_key}'):
                select_position(pos_key)
                st.rerun()

    st.write('')
    st.info(
        f'Each position uses 5 position-specific stats, all calculated per 90 minutes. '
        f'Compare up to {MAX_PLAYERS} players side-by-side on a radar chart. '
        f'Only players with at least {MIN_90S} full 90-minute periods are included.'
    )


# compare screen — search players and show the radar chart
else:
    pos = st.session_state.position
    config = POSITION_CONFIG[pos]
    stats_config = config['stats']
    stat_labels = [s['label'] for s in stats_config]

    pos_df = filter_by_position(df, pos, min_90s=MIN_90S)
    pos_df = compute_per90(pos_df, stats_config)

    st.markdown(f"### {config['icon']} Comparing **{config['display_name']}**")
    st.caption(f'{len(pos_df)} eligible players · primary position = {pos}')

    # player search
    selected = st.session_state.selected_players
    if len(selected) < MAX_PLAYERS:
        available = [p for p in pos_df['Player'].tolist() if p not in selected]
        choice = st.selectbox(
            f"Search for a {config['display_name'][:-1].lower()}  "
            f"({len(selected)}/{MAX_PLAYERS} selected)",
            options=['— Type to search —'] + available,
            key=f'search_{len(selected)}',
        )
        if choice and choice != '— Type to search —' and choice not in selected:
            st.session_state.selected_players.append(choice)
            st.rerun()
    else:
        st.info(f'Maximum {MAX_PLAYERS} players selected — remove one to add another.')

    # show selected players as cards
    if selected:
        st.markdown('#### Selected')
        chip_cols = st.columns(MAX_PLAYERS)
        for i, player in enumerate(selected):
            color = LINE_COLORS[i]
            row = pos_df[pos_df['Player'] == player].iloc[0]
            with chip_cols[i]:
                st.markdown(
                    f"<div style='border-left: 6px solid {color}; padding: 10px 14px; "
                    f"background: #f8f9fa; border-radius: 6px; margin-bottom: 6px;'>"
                    f"<strong style='font-size: 15px;'>{player}</strong><br>"
                    f"<small style='color:#666'>"
                    f"{row['Squad']} · age {int(row['Age']) if pd.notna(row['Age']) else '?'} "
                    f"· {row['Comp_clean']}"
                    f"</small></div>",
                    unsafe_allow_html=True,
                )
                if st.button(f'✕ Remove', key=f'rm_{player}', use_container_width=True):
                    remove_player(player)
                    st.rerun()

        # stats table and radar chart
        players_data = [get_player_stats(pos_df, p, stats_config) for p in selected]

        # percentile table
        st.markdown('#### Percentile Rankings')
        st.caption('100 = best in position group · 0 = worst')
        pct_rows = []
        for pdata in players_data:
            row = {'Player': pdata['player'], 'Squad': pdata['squad']}
            row.update({lbl: pdata['percentile'][lbl] for lbl in stat_labels})
            row['Minutes'] = pdata['minutes']
            pct_rows.append(row)
        st.dataframe(pd.DataFrame(pct_rows), hide_index=True, use_container_width=True)

        # radar chart
        fig = build_radar(players_data, stat_labels)
        st.plotly_chart(fig, use_container_width=True)

        # raw per-90 values
        with st.expander('Show raw per-90 values'):
            raw_rows = []
            for pdata in players_data:
                row = {'Player': pdata['player']}
                row.update({lbl: pdata['raw'][lbl] for lbl in stat_labels})
                raw_rows.append(row)
            st.dataframe(pd.DataFrame(raw_rows), hide_index=True, use_container_width=True)

    else:
        st.info(
            f"Use the search box above to add up to {MAX_PLAYERS} "
            f"{config['display_name'].lower()} to compare."
        )
