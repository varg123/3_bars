import json
from math import sqrt, pow
import sys


def print_bar_info(bar):
    bar_atributes = bar["properties"]['Attributes']
    bar_name = bar_atributes['Name']
    address = bar_atributes['Address']
    adm_area = bar_atributes['AdmArea']
    district = bar_atributes['District']
    phone_number = bar_atributes['PublicPhone'][0]['PublicPhone']
    seats_count = bar["properties"]['Attributes']['SeatsCount']
    templ_bar_info = """
        Название бара: {}
        Адрес: {}, {}, {}
        Количество мест: {}
        Телефон: {}
    """
    bar_info = bar_name, adm_area, district, address, seats_count, phone_number
    print(templ_bar_info.format(*bar_info))


def distance_from(user_coords):
    def distance_to(bar):
        x2 = bar['geometry']['coordinates'][0]
        x1 = user_coords[0]
        y2 = bar['geometry']['coordinates'][1]
        y1 = user_coords[1]
        distance = sqrt(pow(x2-x1, 2)+pow(y2-y1, 2))
        return distance
    return distance_to


def get_seats_count(bar):
    return bar["properties"]['Attributes']['SeatsCount']


def main():
    with open(sys.argv[1], "rt", encoding="utf8") as data_file:
        data_bars = json.loads(data_file.read())
    print('Самый большой бар:')
    print_bar_info(max(data_bars["features"], key=get_seats_count))
    print('Cамый маленький бар: ')
    print_bar_info(min(data_bars["features"], key=get_seats_count))
    print("Введите свои координаты через пробел:")
    user_coords = [int(coord) for coord in input().split()]
    print('Самый близкий бар: ')
    print_bar_info(min(data_bars["features"], key=distance_from(user_coords)))

if __name__ == '__main__':
    main()
