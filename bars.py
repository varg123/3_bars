import json
from math import sqrt, pow
import sys
import argparse


def print_bar_info(bar):
    bar_atributes = bar['properties']['Attributes']
    bar_name = bar_atributes['Name']
    address = bar_atributes['Address']
    adm_area = bar_atributes['AdmArea']
    district = bar_atributes['District']
    phone_number = bar_atributes['PublicPhone'][0]['PublicPhone']
    seats_count = bar['properties']['Attributes']['SeatsCount']
    templ_bar_info = '''
        Название бара: {}
        Адрес: {}, {}, {}
        Количество мест: {}
        Телефон: {}
    '''
    bar_info = bar_name, adm_area, district, address, seats_count, phone_number
    print(templ_bar_info.format(*bar_info))


def get_distance_from(user_coords):
    def get_distance_to(bar):
        x2 = bar['geometry']['coordinates'][0]
        x1 = user_coords[0]
        y2 = bar['geometry']['coordinates'][1]
        y1 = user_coords[1]
        distance = sqrt(pow(x2-x1, 2)+pow(y2-y1, 2))
        return distance
    return get_distance_to


def get_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def load_data(filepath):
    with open(filepath, 'rt', encoding='utf8') as data_file:
        return json.loads(data_file.read())


def parse_filepath():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-f', '--filepath', 
        type = argparse.FileType(),
        required=True, 
        help='Имя файла с данными')
    namespace = parser.parse_args()
    namespace.filepath.close()
    return namespace.filepath.name

def main():
    filepath_data_bars = parse_filepath()
    data_bars = load_data(filepath_data_bars)
    print(dict(data_bars))
    exit()
    
    print('Самый большой бар:')
    print_bar_info(max(data_bars['features'], key=get_seats_count))
    print('Cамый маленький бар: ')
    print_bar_info(min(data_bars['features'], key=get_seats_count))
    print('Введите свои координаты через пробел:')
    user_coords = [float(coord) for coord in input().split()]
    print('Самый близкий бар: ')
    print_bar_info(min(data_bars['features'], key=get_distance_from(user_coords)))

if __name__ == '__main__':
    main()
