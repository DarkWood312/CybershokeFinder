import requests
from bs4 import BeautifulSoup
from time import sleep
import datetime
import json
import os
from colorama import Fore


def stop():
    input('\n' + Fore.RED + 'Press Enter' + Fore.RESET)
    exit(1)


path = os.getcwd()
today = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y %H-%M')
main_link = 'https://cybershoke.net/servers/retake'
post_link = 'https://apiv2.cybershoke.net:2096/servers/data'
headers = {
    'Host': 'apiv2.cybershoke.net:2096',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Origin': 'https://cybershoke.net'
}


def create_settings(filename='settings.txt'):
    with open(filename, 'w') as f:
        f.write('''save = False
sleep_time = 0.5
searching_with_filters = False
nick = None
sub = None
country = None
level_faceit = None
level_faceit_more_less_or_equal = equal
elo_faceit = None
elo_faceit_more_or_less = less
level_cybershoke = None
level_cybershoke_more_less_or_equal = more
steamid = None
steam_link = None
kills = None
kills_more_or_less = more
headshots = None
headshots_more_or_less = more
deaths = None
deaths_more_or_less = less
time = None
time_more_or_less = more
''')


def create_instructions(filename='instructions.txt'):
    with open(filename, 'w') as f:
        f.write('''Intructions for settings.txt:\n
save - True or False
sleep_time - float like 0.5
searching_with_filters - True or False
nick - None or something
sub - None, LITE or VIP
country - None or something like ru, ua, es, kz
level_faceit - None or integer
level_faceit_more_less_or_equal - More or less
elo_faceit - None or integer
elo_faceit_more_or_less - More or less
level_cybershoke - None or integer
level_cybershoke_more_less_or_equal - More, less or equal
steamid - None or something
steam_link - None or something
kills - None or integer
kills_more_or_less - More or less
headshots - None or integer
headshots_more_or_less - More or less
deaths - None or integer
deaths_more_or_less - More or less
time - None or integer
time_more_or_less - More or less
''')


def process_settings(filename='settings.txt') -> dict:
    settings = {}
    with open(filename, 'r') as f:
        lines = (line.strip() for line in f.readlines())
        f.close()
    for setting in lines:
        k, v = setting.split('=')
        k = k.split()[0]
        v = v.split()[0]
        if '.' in v:
            try:
                v = float(v)
            except ValueError:
                if v.isdecimal():
                    v = int(v)
        elif v.lower() == 'none':
            v = None
        elif v.isdecimal():
            v = int(v)
        elif v.lower() == 'true':
            v = True
        elif v.lower() == 'false':
            v = False
        settings[k] = v
    return settings


if not os.path.exists('settings.txt'):
    create_settings()
    print(Fore.CYAN + 'Settings.txt has created!' + Fore.RESET)
if not os.path.exists('instructions.txt'):
    create_instructions()
    print(Fore.CYAN + 'Instructions.txt has created!' + Fore.RESET)

settings = process_settings()

searching = settings['searching_with_filters']


def output(target, target_value, server_identity: str, n, g, a, c, fl, fe, cl, sid, serip, serport, k, h, d, t,
           addition):
    with open(f'{path}\\dump\\{today}\\found\\{target} {addition}.txt', 'a') as f:
        try:
            f.write(f''''{n}' with {target} '{target_value}' at {server_identity} :
    Nickname - {n}
    Subscription - {g}
    Avatar - {a}
    Country - {c}
    Level faceit - {fl}
    ELO faceit - {fe}
    Level cybershoke - {cl}
    STEAMID - {sid}
    STEAM_LINK - https://steamcommunity.com/profiles/{sid}/
    ServerIP - {serip}
    ServerPort - {serport}
    Kills - {k}
    Headshots - {h}
    Deaths - {d}
    Time - {t}\n\n''')
        except UnicodeEncodeError:
            pass
        f.close()
    print(f"{Fore.LIGHTGREEN_EX}I have found {Fore.LIGHTBLUE_EX} '{n}' {Fore.LIGHTGREEN_EX} with {Fore.LIGHTBLUE_EX} {target} '{target_value}' {Fore.LIGHTGREEN_EX} at {Fore.LIGHTBLUE_EX} {server_identity}" + Fore.RESET)


def main_func(process_count=0):
    if not settings['save'] and not searching:
        print(Fore.LIGHTRED_EX + f'Searching and Saving in {Fore.CYAN}settings.txt{Fore.LIGHTRED_EX} are turned {Fore.RED}off{Fore.LIGHTRED_EX}! There is nothing to do ;(' + Fore.RESET)
        stop()
    try:
        if settings['save']:
            os.makedirs(f'{path}\\dump\\{today}\\json')
            os.makedirs(f'{path}\\dump\\{today}\\txt')
        if searching:
            os.makedirs(f'{path}\\dump\\{today}\\found')
    except FileExistsError:
        pass
    main = requests.get(main_link)
    servers_list = []
    servers = BeautifulSoup(main.content, 'lxml').find_all(class_='home-body-servers')
    for server in servers:
        ip_and_port = server.find(class_='tip').findNext().findNext().findNext().get('href').replace('steam://connect/',
                                                                                                     '')
        name = server.find(class_='block-servers-name').get_text().replace('#', '')
        info = server.find('span', class_='group').find(class_='block-servers-group-info').get_text()
        if ip_and_port is not None:
            servers_list.append([name, ip_and_port, info])

    for request in servers_list:
        iport = request[1]
        servername = request[0]
        server_info = request[2]
        server_identity = f'{servername} ({iport}) {server_info}'
        ip, port = iport.split(':')
        r = requests.post(post_link, headers=headers, data={'ip': ip, 'port': port})
        j = r.json()

        if settings['save']:
            with open(f'{path}\\dump\\{today}\\txt\\output.txt', 'a', encoding='utf-8') as f:
                f.write(f'\n{server_identity} -->')
                f.close()

        for i in j['playersv2']:
            g = str(i['group'])
            n = str(i['name'])
            a = str(i['avatar'])
            c = str(i['country'])
            fl = str(i['faceit_level'])
            cl = str(i['cybershoke_level'])
            sid = str(i['steamid64'])
            slink = f'https://steamcommunity.com/profiles/{sid}/'
            serip = str(i['server_ip'])
            serport = str(i['server_port'])
            k = str(i['kills'])
            h = str(i['headshots'])
            d = str(i['deaths'])
            t = str(i['time'])
            fe = str(i['FACEIT_elo'])

            if searching:
                if settings['nick'] is not None and settings['nick'].lower() in n.lower():
                    output('nick', n, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport, k, h, d, t,
                           f'= {n}')

                if settings['sub'] is not None and settings['sub'].lower() in g.lower():
                    output('subscription', g, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport, k, h, d, t,
                           f'= {g}')

                if settings['country'] is not None and settings['country'].lower() in c.lower():
                    output('country', c, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport, k, h, d, t,
                           f'= {c}')

                if settings['steamid'] is not None and settings['steamid'] == int(sid):
                    output('steamid', sid, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport, k, h, d, t,
                           f'= {sid}')

                if settings['steam_link'] is not None and settings['steam_link'].lower() in slink.lower():
                    output('steam_link', slink, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport, k, h, d,
                           t, f'= {slink}')

                try:
                    if settings['level_faceit']:
                        match settings['level_faceit_more_less_or_equal']:
                            case 'more':
                                if int(fl) >= settings['level_faceit']:
                                    output('level_faceit', fl, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'more {settings["level_faceit"]}')

                            case 'less':
                                if int(fl) <= settings['level_faceit']:
                                    output('level_faceit', fl, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport,
                                           k, h, d, t, f'less {settings["level_faceit"]}')

                            case 'equal':
                                if settings['level_faceit'] == int(fl):
                                    output('level_faceit', fl, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'equal {settings["level_faceit"]}')

                    if settings['elo_faceit']:
                        match settings['elo_faceit_more_or_less']:
                            case 'more':
                                if int(fe) >= settings['elo_faceit']:
                                    output('elo_faceit', fe, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'more {settings["elo_faceit"]}')
                            case 'less':
                                if int(fe) <= settings['elo_faceit']:
                                    output('elo_faceit', fe, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'less {settings["elo_faceit"]}')
                    if settings['level_cybershoke']:
                        match settings['level_cybershoke_more_less_or_equal']:
                            case 'more':
                                if int(cl) >= settings['level_cybershoke']:
                                    output('level_cybershoke', cl, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'more {settings["level_cybershoke"]}')
                            case 'less':
                                if int(cl) <= settings['level_cybershoke']:
                                    output('level_cybershoke', cl, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'less {settings["level_cybershoke"]}')
                            case 'equal':
                                if settings['level_cybershoke'] == int(cl):
                                    output('level_cybershoke', cl, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'equal {settings["level_cybershoke"]}')
                    if settings['time']:
                        match settings['time_more_or_less']:
                            case 'more':
                                if int(t) >= settings['time']:
                                    output('time', t, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'more {settings["time"]}')
                            case 'less':
                                if int(t) <= settings['time']:
                                    output('time', t, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'less {settings["time"]}')
                    if settings['kills']:
                        match settings['kills_more_or_less']:
                            case 'more':
                                if int(k) >= settings['kills']:
                                    output('kills', k, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'more {settings["kills"]}')
                            case 'less':
                                if int(k) <= settings['kills']:
                                    output('kills', fe, server_identity, n, g, a, c, fl, fe, cl, sid, serip,
                                           serport, k, h, d, t, f'less {settings["kills"]}')
                    if settings['headshots']:
                        match settings['headshots_more_or_less']:
                            case 'more':
                                if int(h) >= settings['headshots']:
                                    output('headshots', h, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport,
                                           k, h,
                                           d, t, f'more {settings["headshots"]}')
                            case 'less':
                                if int(h) <= settings['headshots']:
                                    output('headshots', h, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport,
                                           k, h, d, t, f'less {settings["headshots"]}')
                    if settings['deaths']:
                        match settings['deaths_more_or_less']:
                            case 'more':
                                if int(d) >= settings['deaths']:
                                    output('deaths', d, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport, k,
                                           h,
                                           d, t, f'more {settings["deaths"]}')
                            case 'less':
                                if int(d) <= settings['deaths']:
                                    output('deaths', d, server_identity, n, g, a, c, fl, fe, cl, sid, serip, serport,
                                           k, h, d, t, f'less {settings["deaths"]}')

                except ValueError as e:
                    with open(f'{path}\\dump\\{today}\\errors.txt', 'a') as f:
                        f.write(str(e) + '\n\n')

            if settings['save']:

                with open(f'{path}\\dump\\{today}\\json\\{servername}.json', 'w', encoding='utf-8') as f:
                    json.dump(j, f, indent=3)
                    f.close()

                with open(f'{path}\\dump\\{today}\\txt\\output.txt', 'a', encoding='utf-8') as f:
                    try:
                        f.write(f'''
            Nickname - {n}
            Subscription - {g}
            Avatar - {a}
            Country - {c}
            Level faceit - {fl}
            ELO faceit - {fe}
            Level cybershoke - {cl}
            STEAMID - {sid}
            STEAM_LINK - https://steamcommunity.com/profiles/{sid}/
            IP - {serip}
            Port - {serport}
            Kills - {k}
            Headshots - {h}
            Deaths - {d}
            Time - {t}\n''')
                    except UnicodeEncodeError:
                        pass
                    f.close()

        process_count += 1
        print(
            f'{Fore.LIGHTYELLOW_EX}Processing... {process_count}/{len(servers_list)} - {round(process_count / len(servers_list) * 100, 1)}%')
        sleep(settings['sleep_time'])


if __name__ == '__main__':
    main_func()
