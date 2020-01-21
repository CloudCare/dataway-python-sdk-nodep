#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataway import Dataway

def print_sep(title):
    line = '-' * 10
    print('{0} [{1}] {2}'.format(line, title, line))

def main():
    dataway = Dataway(debug=True, access_key='x', secret_key='x')

    points = [
        {
            'measurement': 'M1',
            'tags'       : {'T1': 'X', 'T2': 'Y'},
            'fields'     : {'F1': 'A', 'F2': 42, 'F3': 4.2, 'F4': True, 'F5': False},
            'timestamp'  : 1577808000,
        },
        {
            'measurement': 'M1',
            'tags'       : {'T1': 'X'},
            'fields'     : {'F1': 'A'},
            'timestamp'  : 1577808001,
        },
        {
            'measurement': 'M1',
            'tags'       : None,
            'fields'     : {'F1': 'A'},
            'timestamp'  : 1577808002,
        },
        {
            'measurement': 'M1',
            'fields'     : {'F1': 'A'},
        },
    ]

    print_sep('dataway.write_point()')
    dataway.write_point(**points[0])

    print_sep('dataway.write_points()')
    dataway.write_points(points)

if __name__ == '__main__':
    main()