#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataway import Dataway

def print_sep(title):
    line = '-' * 10
    print('{0} [{1}] {2}'.format(line, title, line))

def main():
    dw = Dataway(debug=True)

    points = [
        {
            'measurement': 'M1',
            'tags'       : {'T1': 'X', 'T2': 'Y', 'T3': ''},
            'fields'     : {'F1': 'A', 'F2': 42, 'F3': 4.2, 'F4': True, 'F5': False, 'F6': '', 'F7': None},
            'timestamp'  : 1577808000000000001,
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
        {
            'measurement': '中文指标名',
            'tags'       : {'中文标签': '中文标签值'},
            'fields'     : {'中文字段': '中文字段值'},
        },
        {
            'measurement': u'中文指标名2',
            'tags'       : {u'中文标签2': u'中文标签值2'},
            'fields'     : {u'中文字段2': u'中文字段值2'},
        },
    ]

    print_sep('Dataway.write_point()')
    dw.write_point(**points[0])

    print_sep('Dataway.write_points()')
    dw.write_points(points)

    keyevents = [
        {
            'title'    : 'T1',
            'des'      : 'D1',
            'link'     : 'http://link',
            'source'   : 'S1',
            'tags'     : {'T1': 'X'},
            'timestamp': 1577808000,
        },
        {
            'title'    : 'T1',
            'timestamp': 1577808001,
        },
    ]

    print_sep('Dataway.write_keyevent()')
    dw.write_keyevent(**keyevents[0])

    print_sep('Dataway.write_keyevents()')
    dw.write_keyevents(keyevents)

    flows = [
        {
            'app'      : 'A1',
            'trace_id' : 'TRACE-001',
            'name'     : 'N1',
            'duration' : 10,
            'parent'   : 'P1',
            'tags'     : {'T1': 'X'},
            'fields'   : {'F1': 'A'},
            'timestamp': 1577808000,
        },
        {
            'app'        : 'A1',
            'trace_id'   : 'TRACE-001',
            'name'       : 'N1',
            'duration_ms': 10000,
            'timestamp'  : 1577808001,
        },
    ]

    print_sep('Dataway.write_flow()')
    dw.write_flow(**flows[0])

    print_sep('Dataway.write_flows()')
    dw.write_flows(flows)

if __name__ == '__main__':
    main()
