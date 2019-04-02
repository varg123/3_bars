import json
from math import sqrt
import argparse


def print_bar_info(bar):
    templ_bar_info = '''
        Название бара: {}
        Адрес: {}, {}, {}
        Количество мест: {}
        Телефон: +7{}
    '''
    bar_info = templ_bar_info.format(
        bar['properties']['Attributes']['Name'],
        bar['properties']['Attributes']['AdmArea'],
        bar['properties']['Attributes']['District'],
        bar['properties']['Attributes']['Address'],
        bar['properties']['Attributes']['SeatsCount'],
        bar['properties']['Attributes']['PublicPhone'][0]['PublicPhone'],
    )
    print(bar_info)


def get_distance_from(user_coords):
    def get_distance_to(bar):
        x2 = bar['geometry']['coordinates'][0]
        x1 = user_coords[0]
        y2 = bar['geometry']['coordinates'][1]
        y1 = user_coords[1]
        distance = sqrt((x2-x1)**2 + (y2-y1)**2)
        return distance
    return get_distance_to


def get_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def load_data(filepath):
    with open(filepath, 'rt', encoding='utf8') as data_file:
        data_bars = json.loads(data_file.read())
        return data_bars['features']


def parse_filepath():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', required=True)
    namespace = parser.parse_args()
    return namespace.filepath


def main():
    filepath_data_bars = parse_filepath()
    try:
        data_bars = load_data(filepath_data_bars)
    except (TypeError, json.decoder.JSONDecodeError):
        exit("bars.py: error: the data file is incorrect.")
    except FileNotFoundError:
        exit("bars.py: error: the data file was not found.")
    print('Самый большой бар:')
    print_bar_info(max(data_bars, key=get_seats_count))
    print('Cамый маленький бар: ')
    print_bar_info(min(data_bars, key=get_seats_count))
    print('Введите свои координаты через пробел:')
    try:
        user_coords = [float(coord) for coord in input().split()]
    except ValueError:
        exit("bars.py: error: input coordinates is incorrect")
    print('Самый близкий бар: ')
    print_bar_info(min(data_bars, key=get_distance_from(user_coords)))

if __name__ == '__main__':
    main()
