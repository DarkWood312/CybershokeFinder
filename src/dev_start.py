from cyberfinder import main

filters = {'server': {
    'mode': '',
    'country': '',
    'prime': None,  # bool
    'players_count': '',  # int
    'maxplayers': None,  # int
    'status': 'Online',
    'faceit_avg': None,  # int
    'faceit_limiter_enable': None  # int
}, 'players': {
    'group': '',
    'name': '',
    'points': None,  # int
    'country': '',
    'faceit_level': None,  # int
    'cybershoke_level': None,  # int
    'steamid64': '',
    'kills': '',  # int
    'headshots': '',  # int
    'deaths': None,  # int
    'time': None,  # int
    'FACEIT_elo': None,  # int
    'rank': None  # int
}}

data = main(filters=filters, maximum=3)

