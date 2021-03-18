import json
import os
import requests
import argparse
import colorama
from datetime import datetime


def make_json():
    with requests.get('https://ipinfo.io/') as response:
        user_data = json.loads(response.text)

    with open('achievements.json', 'w') as new_json:
        data_set = {}
        data_set['resources'] = []
        data_set['resources'].append({
            'user': {'username': ''},
            'achievements': {}
        })
        data_set['user_info'] = [user_data]
        for element in data_set['user_info']:
            del element['readme']
        json.dump(data_set, new_json, indent=2)
    return True


def add_achievement(my_data):
    with open('achievements.json') as j_source:
        source = json.load(j_source)

    with open('achievements.json', 'w') as f_source:
        now = datetime.now().strftime('%b-%d-%Y | %H:%M:%S%p')
        for element in source['resources']:
            if len(element['achievements']) >= 1:
                element['achievements'][my_data] = now
            else:
                element['achievements'] = {my_data:now}
        json.dump(source, f_source, indent=2)


def delete_achievement(my_data):
    with open('achievements.json') as j_source:
        source = json.load(j_source)

    with open('achievements.json', 'w') as f_source:
        for element in source['resources']:
            if my_data in element['achievements']:
                del element['achievements'][my_data]
                print(colorama.Fore.GREEN,
                        f'[*] Deleted "{my_data}"')
            else:
                print(colorama.Fore.RED,
                        f'[!!] {my_data} does not exist in achievements',
                        colorama.Style.RESET_ALL)
        json.dump(source, f_source, indent=2)


def add_username(uname):
    with open('achievements.json') as j_source:
        source = json.load(j_source)

    for element in source['resources']:
        if element['user']['username'] == uname:
            continue
        elif len(element['user']['username']) >= 1:
            print(colorama.Fore.RED,
                    '[!!] Unable to register, because someone else is already registered.',
                    colorama.Style.RESET_ALL)
        else:
            with open('achievements.json', 'w') as f_source:
                for element in source['resources']:
                    element['user']['username'] = uname
                json.dump(source, f_source, indent=2)


def view_achievements():
    with open('achievements.json') as j_source:
        source = json.load(j_source)

    for element in source['resources']:
        achievement_len = len(element['achievements'])
        print(colorama.Fore.YELLOW,
                f'[!] You have {achievement_len} achievement{plural_s(achievement_len)}\n',
                colorama.Style.RESET_ALL)
        for achievement in element['achievements']:
            print(f'Achievement: {achievement}\nDate: {element["achievements"][achievement]}\n')


def plural_s(v):
    return 's' if not abs(v) == 1 else ''


if __name__ == '__main__':
    colorama.init()
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description="Just list down all your achievements, and reflect on yourself.")

    parser.add_argument('-uname', '--username',
                        nargs=1, metavar='USERNAME',
                        action='store',
                        help="Adds username to JSON. (e.g -uname 'Kungger')")

    parser.add_argument("-a", "--add",
                        nargs='+', metavar='ADD',
                        action='store',
                        help="Add as many achievements you have done for the day. (e.g -a 'Won Spelling Bee Competition')")
    
    parser.add_argument('-d', '--delete',
                        nargs='+', metavar='DELETE',
                        action='store',
                        help="Deletes achievements based on what you input. (e.g -d 'Did 100 push ups today')")

    parser.add_argument('-v', '--view',
                        action='store_true',
                        help="Views all achievements.")

    args = parser.parse_args()

    if not os.path.exists('achievements.json'):
        make_json()
    elif os.path.exists('achievements.json'):
        with open('achievements.json') as read:
            if read.readlines() == []:
                make_json()

    if args.username:
        for name in args.username:
            add_username(name)

    if args.add:
        for achievement in args.add:
            add_achievement(achievement)
        
    if args.delete:
        for achievement in args.delete:
            delete_achievement(achievement)
    
    if args.view:
        view_achievements()