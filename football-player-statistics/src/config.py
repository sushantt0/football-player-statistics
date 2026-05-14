"""Configuration for the football player comparison dashboard."""

# ignore players with very few minutes — their per-90 stats are unreliable
MIN_90S = 5

# max players you can compare at once
MAX_PLAYERS = 3

# colours for each player slot on the radar chart
LINE_COLORS = ['#000000', '#E63946', '#2D9831']  # black, red, green

# for these stats, lower is actually better (so we flip the percentile)
INVERTED_STATS = {'Fls', 'CrdY', 'CrdR'}

# stats shown for each position
# col = CSV column name, label = what shows on the chart, per90 = whether to divide by minutes
POSITION_CONFIG = {
    'DF': {
        'display_name': 'Defenders',
        'icon': '🛡️',
        'stats': [
            {'col': 'TklW', 'label': 'Tackles Won',      'per90': True},
            {'col': 'Int',  'label': 'Interceptions',    'per90': True},
            {'col': 'Fls',  'label': 'Fouls Committed',  'per90': True},
            {'col': 'CS%',  'label': 'Clean Sheet %',    'per90': False},
            {'col': 'CrdY', 'label': 'Yellow Cards',     'per90': True},
        ],
    },
    'MF': {
        'display_name': 'Midfielders',
        'icon': '🎯',
        'stats': [
            {'col': 'Int',  'label': 'Interceptions',    'per90': True},
            {'col': 'TklW', 'label': 'Tackles Won',      'per90': True},
            {'col': 'Ast',  'label': 'Assists',          'per90': True},
            {'col': 'Gls',  'label': 'Goals',            'per90': True},
            {'col': 'SoT',  'label': 'Shots on Target',  'per90': True},
        ],
    },
    'FW': {
        'display_name': 'Forwards',
        'icon': '⚡',
        'stats': [
            {'col': 'Gls',  'label': 'Goals',            'per90': True},
            {'col': 'Ast',  'label': 'Assists',          'per90': True},
            {'col': 'SoT',  'label': 'Shots on Target',  'per90': True},
            {'col': 'Crs',  'label': 'Crosses',          'per90': True},
            {'col': 'Fld',  'label': 'Fouls Drawn',      'per90': True},
        ],
    },
}
