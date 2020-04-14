# -*- coding: utf-8 -*-

import sys
import time
import types
import json
import re
import hmac
from hashlib import sha1, md5
import base64
from email.utils import formatdate
try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict # New in 2.7

# -----------------------------------------------
# Python2 ~ Python3 Compatibility Code From `six`
# -----------------------------------------------
#
# Copyright (c) 2010-2019 Benjamin Peterson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] >= (3, 4)

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

def ensure_binary(s, encoding='utf-8', errors='strict'):
    if isinstance(s, text_type):
        return s.encode(encoding, errors)
    elif isinstance(s, binary_type):
        return s
    else:
        e = TypeError("not expecting type '%s'" % type(s))
        raise e

def ensure_str(s, encoding='utf-8', errors='strict'):
    if not isinstance(s, (text_type, binary_type)):
        e = TypeError("not expecting type '%s'" % type(s))
        raise e
    if PY2 and isinstance(s, text_type):
        s = s.encode(encoding, errors)
    elif PY3 and isinstance(s, binary_type):
        s = s.decode(encoding, errors)
    return s

if PY3:
    import http.client as httplib
    from urllib.parse import urlsplit, urlparse, urlencode, parse_qs
    long_type = int

else:
    import httplib
    from urllib import urlencode
    from urlparse import urlsplit, urlparse, parse_qs
    long_type = long

MIN_ALLOWED_NS_TIMESTAMP = 1000000000000000000

ESCAPE_REPLACER           = r'\\\1'
RE_ESCAPE_TAG_KEY         = re.compile('([,= ])')
RE_ESCAPE_TAG_VALUE       = RE_ESCAPE_TAG_KEY
RE_ESCAPE_FIELD_KEY       = RE_ESCAPE_TAG_KEY
RE_ESCAPE_MEASUREMENT     = re.compile('([, ])')
RE_ESCAPE_FIELD_STR_VALUE = re.compile('(["\\\\])')

ALERT_LEVELS = ('critical', 'warning', 'info', 'ok')

ASSERT_TYPE_MAPS = {
    'dict': {
        'type'   : (dict, OrderedDict),
        'message': 'should be a dict or OrderedDict',
    },
    'str': {
        'type'   : string_types,
        'message': 'should be a str or unicode',
    },
    'number': {
        'type'   : (integer_types, float),
        'message': 'should be an int or float',
    },
    'int': {
        'type'   : integer_types,
        'message': 'should be an int',
    },
}
def _assert_type(data, data_type, name):
    if not isinstance(data, ASSERT_TYPE_MAPS[data_type]['type']):
        e = Exception('`{0}` {1}, got {2}'.format(name, ASSERT_TYPE_MAPS[data_type]['message'], type(data).__name__))
        raise e
    return data

def assert_dict(data, name):
    return _assert_type(data, 'dict', name)
def assert_str(data, name):
    return _assert_type(data, 'str', name)
def assert_number(data, name):
    return _assert_type(data, 'number', name)
def assert_int(data, name):
    return _assert_type(data, 'int', name)

def assert_enum(data, name, options):
    if data not in options:
        e = Exception('`{0}` should be one of {1}, got {2}'.format(name, ','.join(options), data))
        raise e
    return data

def assert_tags(data, name):
    assert_dict(data, name)
    for k, v in data.items():
        assert_str(k, 'Key of `{0}`: {1}'.format(name, k))
        assert_str(v, 'Value of `{0}["{1}"]`: {2}'.format(name, k, v))

    return data

def assert_json_str(data, name):
    if isinstance(data, string_types):
        try:
            data = json.dumps(json.loads(data), ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        except Exception as e:
            e = Exception('`{0}` should be a JSON or JSON string, got {1}'.format(name, data))
            raise e

    elif isinstance(data, (dict, OrderedDict, list, tuple)):
        try:
            data = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
        except Exception as e:
            e = Exception('`{0}` should be a JSON or JSON string. Error occured during serialization: {1}'.format(name, e))
            raise e

    else:
        e = Exception('`check_value` should be a JSON or JSON string')
        raise e

    return data

class DataWay(object):
    CONTENT_TYPE = 'text/plain'
    METHOD       = 'POST'

    def __init__(self, url=None, host=None, port=None, protocol=None, path=None, token=None, rp=None, timeout=None, access_key=None, secret_key=None, debug=False):
        self.host       = host or 'localhost'
        self.port       = int(port or 9528)
        self.protocol   = protocol or 'http'
        self.path       = path or '/v1/write/metrics'
        self.token      = token
        self.rp         = rp or None
        self.timeout    = timeout or 3
        self.access_key = access_key
        self.secret_key = secret_key
        self.debug      = debug or False

        if self.debug:
            print('[Python Version]\n{0}'.format(sys.version))

        if url:
            splited_url = urlsplit(url)

            if splited_url.scheme:
                self.protocol = splited_url.scheme

            if splited_url.path:
                self.path = splited_url.path

            if splited_url.query:
                parsed_query = parse_qs(splited_url.query)
                if 'token' in parsed_query:
                    self.token = parsed_query['token'][0]

            if splited_url.netloc:
                host_port_parts = splited_url.netloc.split(':')
                if len(host_port_parts) >= 1:
                    self.host = host_port_parts[0]
                    if self.protocol == 'https':
                        self.port = 443
                    else:
                        self.port = 80

                if len(host_port_parts) >= 2:
                    self.port = int(host_port_parts[1])

        if not self.token:
            e = Exception('`token` is required')
            raise e

    def _convert_to_ns(self, timestamp):
        timestamp = long_type(timestamp)

        for i in range(3):
            if timestamp < MIN_ALLOWED_NS_TIMESTAMP:
                timestamp *= 1000
            else:
                break

        return timestamp

    def _get_body_md5(self, body=None):
        h = md5()
        h.update(ensure_binary(body or ''))

        md5_res = h.digest()
        md5_res = base64.standard_b64encode(md5_res).decode()

        return md5_res

    def _get_sign(self, str_to_sign):
        h = hmac.new(ensure_binary(self.secret_key), ensure_binary(str_to_sign), sha1)

        sign = h.digest()
        sign = base64.standard_b64encode(sign).decode()

        return sign

    def _prepare_headers(self, body):
        headers = {
            'Content-Type': self.CONTENT_TYPE,
        }

        if not self.access_key or not self.secret_key:
            return headers

        body_md5 = self._get_body_md5(body)
        date_str = formatdate(timeval=None, localtime=False, usegmt=True)
        str_to_sign = '\n'.join([self.METHOD, body_md5, self.CONTENT_TYPE, date_str])

        sign = self._get_sign(str_to_sign)

        if self.debug:
            print('\n[String to sign] {0}'.format(json.dumps(str_to_sign)))
            print('[Signature] {0}'.format(json.dumps(sign)))

        headers.update({
            'Date'         : date_str,
            'Authorization': 'DWAY {0}:{1}'.format(self.access_key, sign),
        })

        return headers

    def _prepare_body(self, points):
        if not isinstance(points, (list, tuple)):
            points = [points]

        lines = []

        for p in points:
            # Influx DB line protocol
            # https://docs.influxdata.com/influxdb/v1.7/write_protocols/line_protocol_tutorial/
            measurement = p.get('measurement')
            measurement = re.sub(RE_ESCAPE_MEASUREMENT, ESCAPE_REPLACER, measurement)

            tag_set_list = []
            tags = p.get('tags') or None
            if tags:
                key_list = sorted(tags.keys())
                for k in key_list:
                    v = tags[k]
                    if not v:
                        continue

                    k = re.sub(RE_ESCAPE_TAG_KEY, ESCAPE_REPLACER, k)
                    v = re.sub(RE_ESCAPE_TAG_VALUE, ESCAPE_REPLACER, v)

                    tag_set_list.append('{0}={1}'.format(ensure_str(k), ensure_str(v)))

            tag_set = ''
            if len(tag_set_list) > 0:
                tag_set = ',{0}'.format(','.join(tag_set_list))

            field_set_list = []
            fields = p.get('fields') or None
            if fields:
                key_list = sorted(fields.keys())
                for k in key_list:
                    v = fields[k]

                    k = re.sub(RE_ESCAPE_FIELD_KEY, ESCAPE_REPLACER, k)
                    if isinstance(v, string_types):
                        v = re.sub(RE_ESCAPE_FIELD_STR_VALUE, ESCAPE_REPLACER, v)
                        v = '"{0}"'.format(ensure_str(v))

                    elif isinstance(v, bool):
                        v = '{0}'.format(v).lower()

                    elif isinstance(v, integer_types):
                        v = '{0}i'.format(v)

                    else:
                        v = '{0}'.format(v)

                    field_set_list.append('{0}={1}'.format(ensure_str(k), ensure_str(v)))

            field_set = ' {0}'.format(','.join(field_set_list))

            timestamp = p.get('timestamp')
            timestamp = ' {0}'.format(timestamp)

            lines.append('{0}{1}{2}{3}'.format(ensure_str(measurement), ensure_str(tag_set), ensure_str(field_set), ensure_str(timestamp)))

        body = '\n'.join(lines)
        body = ensure_binary(body)

        return body

    def _send_points(self, points):
        body = self._prepare_body(points)
        if self.debug:
            print('[Request Body]\n{0}'.format(ensure_str(body)))

        headers = self._prepare_headers(body)

        conn = None
        if self.protocol == 'https':
            conn = httplib.HTTPSConnection(self.host, port=self.port, timeout=self.timeout)
        else:
            conn = httplib.HTTPConnection(self.host, port=self.port, timeout=self.timeout)

        url = self.path + '?token={0}'.format(self.token)
        if self.rp:
            url += '&rp={0}'.format(self.rp)

        conn.request(self.METHOD, url, body=body, headers=headers)
        resp = conn.getresponse()

        resp_status_code = resp.status
        resp_raw_data    = resp.read()

        resp_content_type = resp.getheader('Content-Type')
        if isinstance(resp_content_type, string_types):
            resp_content_type = resp_content_type.split(';')[0].strip()

        resp_data = resp_raw_data
        if resp_content_type == 'application/json':
            resp_data = json.loads(ensure_str(resp_raw_data))

        if self.debug:
            print('\n[Response Status Code] {0}'.format(resp_status_code))
            print('[Response Body] {0}'.format(ensure_str(resp_raw_data)))

        return resp_status_code, resp_data

    # point
    def _preapre_point(self, point):
        assert_dict(point, name='point')

        measurement = assert_str(point.get('measurement'), name='measurement')

        tags = point.get('tags')
        if tags is not None:
            assert_dict(tags, name='tags')
            assert_tags(tags, name='tags')

        fields = assert_dict(point.get('fields'), name='fields')

        timestamp = point.get('timestamp')
        if timestamp is not None:
            assert_number(timestamp, name='timestamp')
        else:
            timestamp = time.time()

        timestamp = self._convert_to_ns(timestamp)

        point = {
            'measurement': measurement,
            'tags'       : tags   or None,
            'fields'     : fields or None,
            'timestamp'  : timestamp,
        }
        return point

    def write_point(self, measurement, tags=None, fields=None, timestamp=None, ):
        point = {
            'measurement': measurement,
            'tags'       : tags,
            'fields'     : fields,
            'timestamp'  : timestamp,
        }
        prepared_point = self._preapre_point(point)

        return self._send_points(prepared_point)

    def write_points(self, points):
        if not isinstance(points, (list, tuple)):
            e = Exception('`points` should be a list or tuple, got {0}'.format(type(points).__name__))
            raise e

        prepared_points = []
        for p in points:
            prepared_points.append(self._preapre_point(p))

        return self._send_points(prepared_points)

    # $keyevent
    def _prepare_keyevent(self, keyevent):
        assert_dict(keyevent, name='keyevent')

        # Check Tags
        tags = keyevent.get('tags') or {}
        assert_tags(tags, name='tags')

        # Tags.$source
        source = keyevent.get('source')
        if source is not None:
            tags['$source'] = assert_str(source, name='source')

        # Check Fields
        fields = {}

        # Fields.$title
        fields['$title'] = assert_str(keyevent.get('title'), name='title')

        # Fields.$des
        des = keyevent.get('des')
        if des is not None:
            fields['$des'] = assert_str(des, name='des')

        # Fields.$link
        link = keyevent.get('link')
        if link is not None:
            assert_str(link, name='link')

            if not link.lower().startswith('http://') \
                    and not link.lower().startswith('https://') \
                    or link.endswith('://'):
                e = Exception('`link` should be a valid URL with protocol, got {0}'.format(link))
                raise e

            fields['$link'] = link

        point = {
            'measurement': '$keyevent',
            'tags'       : tags,
            'fields'     : fields,
            'timestamp'  : keyevent.get('timestamp'),
        }
        return self._preapre_point(point)

    def write_keyevent(self, title, timestamp,
        des=None, link=None, source=None, tags=None):
        keyevent = {
            'title'    : title,
            'des'      : des,
            'link'     : link,
            'source'   : source,
            'tags'     : tags,
            'timestamp': timestamp,
        }
        prepared_point = self._prepare_keyevent(keyevent)
        return self._send_points(prepared_point)

    def write_keyevents(self, keyevents):
        if not isinstance(keyevents, (list, tuple)):
            e = Exception('`keyevents` should be a list or tuple, got {0}'.format(type(keyevents).__name__))
            raise e

        prepared_points = []
        for p in keyevents:
            prepared_points.append(self._prepare_keyevent(p))

        return self._send_points(prepared_points)

    # $flow
    def _prepare_flow(self, flow):
        assert_dict(flow, name='flow')

        # Check Tags
        tags = flow.get('tags') or {}
        assert_tags(tags, name='tags')

        # Measurements.$flow_*
        assert_str(flow.get('app'), name='app')

        # Tags.$traceId
        tags['$traceId'] = assert_str(flow.get('trace_id'), name='trace_id')

        # Tags.$name
        tags['$name'] = assert_str(flow.get('name'), name='name')

        # Tags.$parent
        parent = flow.get('parent')
        if parent is not None:
            tags['$parent'] = assert_str(parent, name='parent')

        # Check Fields
        fields = flow.get('fields') or {}
        assert_dict(fields, name='fields')

        # Fields.$duration
        duration_ms = flow.get('duration_ms')
        if duration_ms is not None:
            assert_int(duration_ms, name='duration_ms')

        duration = flow.get('duration')
        if duration is not None:
            assert_int(duration, name='duration')

        # to ms
        if duration:
            duration = duration * 1000

        if duration_ms is None and duration is None:
            e = Exception('`duration` or `duration_ms` is missing')
            raise e

        fields['$duration'] = duration_ms or duration

        point = {
            'measurement': '$flow_{0}'.format(flow['app']),
            'tags'       : tags,
            'fields'     : fields,
            'timestamp'  : flow.get('timestamp'),
        }
        return self._preapre_point(point)

    def write_flow(self, app, trace_id, name, timestamp, duration=None, duration_ms=None,
        parent=None, fields=None, tags=None):
        flow = {
            'app'        : app,
            'trace_id'   : trace_id,
            'name'       : name,
            'duration'   : duration,
            'duration_ms': duration_ms,
            'parent'     : parent,
            'fields'     : fields,
            'tags'       : tags,
            'timestamp'  : timestamp,
        }
        prepared_point = self._prepare_flow(flow)
        return self._send_points(prepared_point)

    def write_flows(self, flows):
        if not isinstance(flows, (list, tuple)):
            e = Exception('`flows` should be a list or tuple, got {0}'.format(type(flows).__name__))
            raise e

        prepared_points = []
        for p in flows:
            prepared_points.append(self._prepare_flow(p))

        return self._send_points(prepared_points)

    # $alert
    def _prepare_alert(self, alert):
        assert_dict(alert, name='alert')

        # Check Tags
        tags = alert.get('tags') or {}
        assert_tags(tags, name='tags')

        # Tags.$level
        tags['$level'] = assert_enum(alert.get('level'), name='level', options=ALERT_LEVELS)

        # Tags.$alertId
        tags['$alertId'] = assert_str(alert.get('alert_id'), name='alert_id')

        # Tags.$ruleId
        rule_id = alert.get('rule_id')
        if rule_id is not None:
            tags['$ruleId'] = assert_str(rule_id, name='rule_id')

        # Tags.$noData
        no_data = alert.get('no_data')
        if no_data:
            tags['$noData'] = 'noData'

        # Tags.$alertItem_*
        alert_item_tags = alert.get('alert_item_tags')
        if alert_item_tags is not None:
            assert_tags(alert_item_tags, name='alert_item_tags')

            for k, v in alert_item_tags.items():
                tags['$alertItem_' + k] = v

        # Tags.$actionType
        action_type = alert.get('action_type')
        if action_type is not None:
            tags['$actionType'] = assert_str(action_type, name='action_type')

        # Check Fields
        fields = {}

        # Fields.$duration
        duration_ms = alert.get('duration_ms')
        if duration_ms is not None:
            assert_int(duration_ms, name='duration_ms')

        duration = alert.get('duration')
        if duration is not None:
            assert_int(duration, name='duration')

        # to ms
        if duration:
            duration = duration * 1000

        if duration_ms is None and duration is None:
            e = Exception('`duration` or `duration_ms` is missing')
            raise e

        fields['$duration'] = duration_ms or duration

        # Fields.$checkValueJSON
        fields['$checkValueJSON'] = assert_json_str(alert.get('check_value'), name='check_value')

        # Fields.$ruleName
        rule_name = alert.get('rule_name')
        if rule_name is not None:
            fields['$ruleName'] = assert_str(rule_name, name='rule_name')

        # Fields.$actionContentJSON
        action_content = alert.get('action_content')
        if action_content is not None:
            fields['$actionContentJSON'] = assert_json_str(action_content, name='action_content')

        point = {
            'measurement': '$alert',
            'tags'       : tags,
            'fields'     : fields,
            'timestamp'  : alert.get('timestamp'),
        }
        return self._preapre_point(point)

    def write_alert(self, level, alert_id, check_value, timestamp, duration=None, duration_ms=None,
        rule_id=None, rule_name=None, no_data=False, action_type=None, action_content=None, alert_item_tags=None, tags=None):
        alert = {
            'level'          : level,
            'alert_id'       : alert_id,
            'rule_id'        : rule_id,
            'rule_name'      : rule_name,
            'no_data'        : no_data,
            'duration'       : duration,
            'duration_ms'    : duration_ms,
            'check_value'    : check_value,
            'action_type'    : action_type,
            'action_content' : action_content,
            'alert_item_tags': alert_item_tags,
            'tags'           : tags,
            'timestamp'      : timestamp,
        }
        prepared_point = self._prepare_alert(alert)
        return self._send_points(prepared_point)

    def write_alerts(self, alerts):
        if not isinstance(alerts, (list, tuple)):
            e = Exception('`alerts` should be a list or tuple, got {0}'.format(type(alerts).__name__))
            raise e

        prepared_points = []
        for p in alerts:
            prepared_points.append(self._prepare_alert(p))

        return self._send_points(prepared_points)


Dataway = DataWay
