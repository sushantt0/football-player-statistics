"""Per-90 calculations and percentile rankings."""
import pandas as pd

from .config import INVERTED_STATS


def compute_per90(df: pd.DataFrame, stats_config: list) -> pd.DataFrame:
    """Divide raw stats by 90s played to get per-90 values."""
    df = df.copy()
    for stat in stats_config:
        col = stat['col']
        if stat['per90']:
            new_col = f'{col}_per90'
            df[new_col] = (df[col] / df['90s']).round(3)
            df[new_col] = df[new_col].fillna(0)
        else:
            df[col] = df[col].fillna(0)
    return df


def _value_col(stat: dict) -> str:
    """Get the right column name for this stat."""
    return f"{stat['col']}_per90" if stat['per90'] else stat['col']


def compute_percentile(df: pd.DataFrame, col: str, value: float, invert: bool = False) -> float:
    """How does this value rank vs everyone else (0-100)? For bad stats like fouls, lower is better so we flip it."""
    series = df[col].dropna()
    if len(series) == 0:
        return 50.0
    if invert:
        pct = (series >= value).mean() * 100
    else:
        pct = (series <= value).mean() * 100
    return round(float(pct), 1)


def get_player_stats(df: pd.DataFrame, player: str, stats_config: list) -> dict:
    """Get raw and percentile stats for a single player."""
    row = df[df['Player'] == player].iloc[0]
    result = {
        'player': player,
        'squad': row['Squad'],
        'age': int(row['Age']) if pd.notna(row['Age']) else None,
        'minutes': int(row['Min']),
        'nation': row['Nation_clean'],
        'comp': row['Comp_clean'],
        'raw': {},
        'percentile': {},
    }
    for stat in stats_config:
        col_to_read = _value_col(stat)
        invert = stat['col'] in INVERTED_STATS
        value = float(row[col_to_read])
        result['raw'][stat['label']] = round(value, 2)
        result['percentile'][stat['label']] = compute_percentile(
            df, col_to_read, value, invert=invert
        )
    return result
