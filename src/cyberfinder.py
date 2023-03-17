from datetime import timedelta
import requests


def compare_dicts(own_dict, server_dict):
    for key, value in own_dict.items():
        if value is None or value == '':
            continue

        if key in server_dict:
            if isinstance(server_dict[key], (int, float)) and value[0] in (
                    '>', '<', '='):
                operator = ''
                for char in value:
                    if char in ('>', '<', '='):
                        operator += char
                    else:
                        break
                comparison_value = float(value[len(operator):])
                if operator == '>':
                    if server_dict[key] > comparison_value:
                        continue
                elif operator == '<':
                    if server_dict[key] < comparison_value:
                        continue
                elif operator == '=':
                    if server_dict[key] == comparison_value:
                        continue
                elif operator == '>=':
                    if server_dict[key] >= comparison_value:
                        continue
                elif operator == '<=':
                    if server_dict[key] <= comparison_value:
                        continue
                return False
            elif str(value).lower() != str(server_dict[key]).lower():
                return False
        else:
            return True

    return True


def text_expressing(dict_: dict):
    servers = list(dict_.values())
    text = ''

    for s in servers:
        text += f"""{s['name']} №{s['num']}, >>> {s['category']}
IP --> {s['ip']}:{s['port']}
Server Country --> {s['country']}
Map --> {s['map']}
Prime --> {s['prime']}
Amount Of Players --> {s['players_count']}
Max Players --> {s['maxplayers']}
Average Faceit Level --> {s['faceit_avg']}
Players:\n
"""
        for p in s['players']:
            # r = requests.get(f'https://www.faceitfinder.app/api/user?id={p["steamid64"]}', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'})
            # steam_faceit_data = r.json()[0]
            # steamurl = steam_faceit_data['steamDatas']['profileurl']
            # faceiturl = steam_faceit_data['playerDatas']['faceit_url']
            # cybershokeurl = f'https://cybershoke.net/{p["steamid64"]}'
            player_text = f"""    Group --> {p['group']}
    Nickname --> {p['name']}
    Faceit Level & ELO --> {p['faceit_level']} & {p['FACEIT_elo']}
    Cybershoke Level & Rank & Points --> {p['cybershoke_level']} & {p['rank']} & {p['points']}
    Kills & Headshots & Deaths --> {p['kills']} & {p['headshots']} & {p['deaths']}
    Played Time --> {timedelta(seconds=p['time'])}"""
            # (Steam & Faceit & Cybershoke) URLS --> {steamurl} & {faceiturl} & {cybershokeurl}"""
            text += player_text + '\n\n'
            # time.sleep(3)
        text += '\n' + ('-' * 100) + '\n\n'

    return text


def main(filters: dict, maximum: int = -1):
    return_dict = {}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'accept-encoding': 'gzip, deflate',
        'origin': 'https://cybershoke.net',
        'referer': 'https://cybershoke.net/',
        'connection': 'keep-alive'
    }

    session = requests.session()

    data_response = session.get('https://api.cybershoke.net/api/v1/main/data', headers=headers)
    response_code = data_response.status_code
    data = data_response.json()['data']

    servers = data['modules']['servers']['data']['servers']

    formatted_dict = {}
    for server in servers.values():
        for type_, values in server.items():
            for v in values:
                formatted_dict[f'{v["ip"]}:{v["port"]}'] = {
                    'id': v['id'],
                    'name': v['name_alt'],
                    'ip': v['ip'],
                    'port': v['port'],
                    'mode': v['mode'],
                    'modealt': v['modeAlt'],
                    'num': v['num'],
                    'country': v['country'],
                    'map': v['map'],
                    'prime': True if v['prime'] == 1 else False,
                    'players_count': v['players'],
                    'maxplayers': v['maxplayers'],
                    'status': v['status'],
                    'faceit_avg': v['faceit_avg'],
                    'show_maps_avg_time': v['show_maps_avg_time'],
                    'statusAlt': v['statusAlt'],
                    'category': v['category'],
                    'time_avg_complete': v['time_avg_complete'],
                    'faceit_limiter_enable': v['faceit_limiter_enable'],
                    'faceit_min_elo': v['faceit_min_elo'],
                    'faceit_max_elo': v['faceit_max_elo']
                }
    for server in formatted_dict.keys():
        ip, port = server.split(':')
        if (formatted_dict[server]['status'] != 'Online') or not (
                compare_dicts(filters['server'], formatted_dict[server])):
            continue
        server_request = session.post('https://api.cybershoke.net/servers/data',
                                      headers={
                                          'authority': 'api.cybershoke.net',
                                          'origin': 'https://cybershoke.net',
                                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'},
                                      data={'ip': ip, 'port': int(port)})
        req_dict = server_request.json()
        for player in req_dict['playersv2']:
            # print(player)
            if not (compare_dicts(filters['players'], player)):
                continue

            formatted_dict[server]['players'] = req_dict['playersv2']
            formatted_dict[server]['server'] = req_dict['serversv2']['0']

            return_dict[server] = formatted_dict[server]

            maximum -= 1
            if maximum == 0:
                return return_dict

    return return_dict