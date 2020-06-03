#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataway import DataWay

def print_sep(title):
    line = '-' * 10
    print('{0} [{1}] {2}'.format(line, title, line))

def main():
    dw = DataWay(protocol='https', host='openway.dataflux.cn', port=443, token=None, rp='rp0', debug=True, dry_run=True)

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

    keyevents = [
        {
            'title'    : 'T1',
            'timestamp': 1577808000,
        }, {
            'title'          : 'T2',
            'event_id'       : 'event-001',
            'source'         : 'SRC1',
            'status'         : 'info',
            'rule_id'        : 'rule-001',
            'rule_name'      : 'R1',
            'type'           : 'TYPE-1',
            'alert_item_tags': {'AT1': 'X', 'AT2': 'Y'},
            'action_type'    : 'A1',
            'content'        : 'C1',
            'suggestion'     : 'SUG-1',
            'duration'       : 10,
            'dimensions'     : ['D-1', u'维度2', '维度3'],
            'tags'           : {'T1': 'X', 'T2': 'Y'},
            'fields'         : {'F1': 'A', 'F2': 'B'},
            'timestamp'      : 1577808001,
        },
    ]

    objects = {
        'object':[
            {
                '$class': 'objectClass',
                '$name' : 'objectName',
                '$tags' : { 'a': 'b', 'c': 'd' }
            }, {
                '$class': 'objectClass',
                '$name' : 'objectName',
                '$tags' : { 'a': 'b2', 'c': 'd2' }
            }
        ]
    }

    print_sep('DataWay ping')
    dw.get(path='/ping')

    print_sep('DataWay post line protocol')
    dw.post_line_protocol(points=points, with_rp=True)

    print_sep('DataWay post json')
    dw.post_json(json_obj=objects, path='/v1/write/object')

    print_sep('DataWay write metric')
    dw.write_metric(**points[0])

    print_sep('DataWay write metrics')
    dw.write_metrics(points)

    print_sep('DataWay write keyevent')
    dw.write_keyevent(**keyevents[0])

    print_sep('DataWay write keyevents')
    dw.write_keyevents(keyevents)

if __name__ == '__main__':
    main()
