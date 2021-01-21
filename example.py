#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataway import DataWay

def print_sep(title):
    line = '-' * 10
    print('\n{0} [{1}] {2}'.format(line, title, line))

def main():
    dw = DataWay(protocol='https', host='openway.dataflux.cn', port=443, token='<TOKEN>', rp='<RP>', debug=True, dry_run=False)

    points = [
        {
            'measurement': 'M1',
            'tags'       : {'T1': 'X', 'T2': 'Y', 'T3': ''},
            'fields'     : {'F1': 'A', 'F2': 42, 'F3': 4.2, 'F4': True, 'F5': False, 'F6': '', 'F7': None},
            'timestamp'  : 1577808000000000001,
        }, {
            'measurement': 'M1',
            'tags'       : {'T1': 'X'},
            'fields'     : {'F1': 'A'},
            'timestamp'  : 1577808001,
        }, {
            'measurement': 'M1',
            'tags'       : None,
            'fields'     : {'F1': 'A'},
            'timestamp'  : 1577808002,
        }, {
            'measurement': 'M1',
            'fields'     : {'F1': 'A'},
        }, {
            'measurement': '中文指标名',
            'tags'       : {'中文标签': '中文标签值'},
            'fields'     : {'中文字段': '中文字段值'},
        }, {
            'measurement': u'中文指标名2',
            'tags'       : {u'中文标签2': u'中文标签值2'},
            'fields'     : {u'中文字段2': u'中文字段值2'},
        },
    ]

    print_sep('Class Method')
    line_protocol = DataWay.prepare_line_protocol(points)
    print(type(line_protocol))
    print(line_protocol)

    print_sep('DataWay ping')
    dw.get(path='/ping')

    print_sep('DataWay post line protocol')
    dw.post_line_protocol(points=points, with_rp=True)

if __name__ == '__main__':
    main()
