"""Load and preprocess the players CSV."""
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).parent.parent / 'data' / 'players_data_light-2025_2026.csv'


def load_players(data_path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the CSV and add a few helper columns for cleaner display."""
    df = pd.read_csv(data_path)

    df['Nation_clean'] = df['Nation'].astype(str).str.split().str[-1]
    df['Comp_clean'] = df['Comp'].astype(str).str.split(n=1).str[-1]
    df['PrimaryPos'] = df['Pos'].astype(str).str.split(',').str[0]

    # Drop rows with missing essential data
    df = df.dropna(subset=['Player', 'PrimaryPos', '90s'])

    return df


def filter_by_position(df: pd.DataFrame, position: str, min_90s: float = 5) -> pd.DataFrame:
    """Return only players whose primary position matches and who've played enough minutes."""
    mask = (df['PrimaryPos'] == position) & (df['90s'] >= min_90s)
    return df[mask].sort_values('Player').reset_index(drop=True)
