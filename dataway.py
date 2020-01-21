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
        raise TypeError("not expecting type '%s'" % type(s))

def ensure_str(s, encoding='utf-8', errors='strict'):
    if not isinstance(s, (text_type, binary_type)):
        raise TypeError("not expecting type '%s'" % type(s))
    if PY2 and isinstance(s, text_type):
        s = s.encode(encoding, errors)
    elif PY3 and isinstance(s, binary_type):
        s = s.decode(encoding, errors)
    return s

if PY3:
    import http.client as httplib
    from urllib.parse import urlsplit, urlparse, urlencode, quote
    long_type = int

else:
    import httplib
    from urllib import urlencode, quote
    from urlparse import urlparse, urlsplit
    long_type = long

TIMESTAMP_OF_20200101_000000 = 1577808000

ESCAPE_REPLACER = r'\\\1'
RE_ESCAPE_TAG_KEY         = re.compile('([,= ])')
RE_ESCAPE_TAG_VALUE       = RE_ESCAPE_TAG_KEY
RE_ESCAPE_FIELD_KEY       = RE_ESCAPE_TAG_KEY
RE_ESCAPE_MEASUREMENT     = re.compile('([, ])')
RE_ESCAPE_FIELD_STR_VALUE = re.compile('(["])')

class Dataway(object):
    CONTENT_TYPE = 'text/plain'
    METHOD       = 'POST'

    def __init__(self, url=None, host=None, port=None, protocol=None, path=None, datakit_uuid=None, access_key=None, secret_key=None, debug=False):
        self.host         = host or 'localhost'
        self.port         = int(port or 9528)
        self.protocol     = protocol or 'http'
        self.path         = path or '/v1/write/metrics'
        self.datakit_uuid = datakit_uuid or 'dataway-python-sdk-nodep'
        self.access_key   = access_key
        self.secret_key   = secret_key
        self.debug        = debug or False

        if self.debug:
            print('[Python Version]\n{0}'.format(sys.version))

        if url:
            splited_url = urlsplit(url)

            if splited_url.netloc:
                host_port_parts = splited_url.netloc.split(':')
                if len(host_port_parts) >= 1:
                    self.host = host_port_parts[0]
                if len(host_port_parts) >= 2:
                    self.port = int(host_port_parts[1])


            if splited_url.scheme:
                self.protocol = splited_url.scheme

            if splited_url.path:
                self.path = splited_url.path

    def _convert_to_ns(self, timestamp):
        timestamp = long_type(timestamp)

        min_ns = TIMESTAMP_OF_20200101_000000 * 1E9
        for i in range(3):
            if timestamp < min_ns:
                timestamp *= 1000

        return timestamp

    def _preapre_point(self, point):
        if not isinstance(point, (dict, OrderedDict)):
            raise Exception('`point` should be a dict or OrderedDict, got {0}'.format(type(point).__name__))

        measurement = point.get('measurement')
        if not isinstance(measurement, string_types):
            raise Exception('`measurement` should be a str or unicode, got {0}'.format(type(measurement).__name__))

        tags = point.get('tags')
        if tags is not None:
            if not isinstance(tags, (dict, OrderedDict)):
                raise Exception('`tags` should be a dict or OrderedDict, got {0}'.format(type(tags).__name__))

            for k, v in tags.items():
                if not isinstance(v, string_types):
                    raise Exception('`tags` value should be a str or unicode, got tags["{0}"] = {1}, {2}'.format(k, v, type(v).__name__))

        fields = point.get('fields')
        if fields is not None and not isinstance(fields, (dict, OrderedDict)):
            raise Exception('`fields` should be a dict or OrderedDict, got {0}'.format(type(fields).__name__))

        timestamp = point.get('timestamp')
        if timestamp is not None and not isinstance(timestamp, (integer_types, float)):
            raise Exception('`timestamp` should be an int, long or float, got {0}'.format(type(timestamp).__name__))

        if timestamp is None:
            timestamp = time.time()

        timestamp = self._convert_to_ns(timestamp)

        point = {
            'measurement': measurement,
            'tags'       : tags or None,
            'fields'     : fields or None,
            'timestamp'  : timestamp,
        }
        return point

    def _prepare_keyevnet(self, keyevent):
        if not isinstance(keyevent, (dict, OrderedDict)):
            raise Exception('`keyevent` should be a dict or OrderedDict, got {0}'.format(type(keyevent).__name__))

        # Check Tags
        tags = keyevent.get('tags') or {}

        source = keyevent.get('source')
        if source is not None and not isinstance(source, string_types):
            raise Exception('`source` should be a str or unicode, got {0}'.format(type(source).__name__))
        else:
            tags['$source'] = source

        fields = {}

        # Check Fields
        title = keyevent.get('title')
        if not isinstance(title, string_types):
            raise Exception('`title` should be a str or unicode, got {0}'.format(type(title).__name__))
        else:
            fields['$title'] = title

        des = keyevent.get('des')
        if des is not None and not isinstance(des, string_types):
            raise Exception('`des` should be a str or unicode, got {0}'.format(type(des).__name__))
        else:
            fields['$des'] = des

        link = keyevent.get('link')
        if link is not None:
            if not isinstance(link, string_types):
                raise Exception('`link` should be a str or unicode, got {0}'.format(type(link).__name__))

            elif not link.lower().startswith('http://') \
                    or not link.lower().startswith('https://') \
                    or link.endswith('://'):
                raise Exception('`link` should be a valid URL with protocol, got {0}'.format(link))

            else:
                fields['$link'] = link

        point = {
            'measurement': '$keyevent',
            'tags'       : tags,
            'fields'     : fields,
            'timestamp'  : keyevent.get('timestamp'),
        }
        return self._preapre_point(point)

    def _prepare_flow(self, flow):
        if not isinstance(flow, (dict, OrderedDict)):
            raise Exception('`flow` should be a dict or OrderedDict, got {0}'.format(type(flow).__name__))

        # Check Tags
        tags = flow.get('tags') or {}

        trace_id = flow.get('trace_id')
        if not isinstance(trace_id, string_types):
            raise Exception('`trace_id` should be a str or unicode, got {0}'.format(type(trace_id).__name__))
        else:
            tags['$traceId'] = trace_id

        name = flow.get('name')
        if not isinstance(name, string_types):
            raise Exception('`name` should be a str or unicode, got {0}'.format(type(name).__name__))
        else:
            tags['$name'] = name

        type_ = flow.get('type')
        if not isinstance(type_, string_types):
            raise Exception('`type` should be a str or unicode, got {0}'.format(type(type_).__name__))
        else:
            tags['$type'] = type_

        parent = flow.get('parent')
        if parent is not None and not isinstance(parent, string_types):
            raise Exception('`parent` should be a str or unicode, got {0}'.format(type(parent).__name__))
        else:
            tags['$parent'] = parent

        fields = flow.get('fields') or {}

        # Check Fields
        duration_ms = flow.get('duration_ms')
        if duration_ms is not None and  not isinstance(duration_ms, integer_types):
            raise Exception('`duration_ms` should be an integer or long, got {0}'.format(type(duration_ms).__name__))

        duration = flow.get('duration')
        if duration is not None and  not isinstance(duration, integer_types):
            raise Exception('`duration` should be an integer or long, got {0}'.format(type(duration).__name__))
        else:
            # to ms
            duration = duration * 1000

        if duration_ms is None and duration is None:
            raise Exception('`duration` or `duration_ms` is missing')

        fields['$duration'] = duration_ms or duration

        point = {
            'measurement': '$flow',
            'tags'       : tags,
            'fields'     : fields,
            'timestamp'  : flow.get('timestamp'),
        }
        return self._preapre_point(point)

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

                    k = re.sub(RE_ESCAPE_TAG_KEY, ESCAPE_REPLACER, k)
                    v = re.sub(RE_ESCAPE_TAG_VALUE, ESCAPE_REPLACER, v)

                    tag_set_list.append('{0}={1}'.format(k, v))

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
                        v = '"{0}"'.format(v)
                    elif isinstance(v, bool):
                        v = '{0}'.format(v).lower()
                    elif isinstance(v, integer_types):
                        v = '{0}i'.format(v)
                    else:
                        v = '{0}'.format(v)

                    field_set_list.append('{0}={1}'.format(k, v))

            field_set = ' {0}'.format(','.join(field_set_list))

            timestamp = p.get('timestamp')
            timestamp = ' {0}'.format(timestamp)

            lines.append('{0}{1}{2}{3}'.format(measurement, tag_set, field_set, timestamp))

        body = '\n'.join(lines)

        return body

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
            'Content-Type'  : self.CONTENT_TYPE,
            'X-Datakit-UUID': self.datakit_uuid,
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

    def _send_points(self, points):
        body = self._prepare_body(points)
        if self.debug:
            print('[Request Body]\n{0}'.format(body))

        headers = self._prepare_headers(body)

        conn = None
        if self.protocol == 'https':
            conn = httplib.HTTPSConnection(self.host, port=self.port)
        else:
            conn = httplib.HTTPConnection(self.host, port=self.port)

        conn.request(self.METHOD, self.path, body=body, headers=headers)

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
            print('[Response Body] {0}'.format(resp_raw_data))

        return resp_status_code, resp_data

    def write_point(self, measurement, tags=None, fields=None, timestamp=None):
        point = {
            'measurement': measurement,
            'tags'       : tags,
            'fields'     : fields,
            'timestamp'  : timestamp,
        }
        prepared_point = self._preapre_point(point)

        self._send_points(prepared_point)

    def write_points(self, points):
        if not isinstance(points, (list, tuple)):
            raise Exception('`points` should be a list or tuple, got {0}'.format(type(points).__name__))

        prepared_points = []
        for p in points:
            prepared_points.append(self._preapre_point(p))

        self._send_points(prepared_points)

    def write_keyevent(self, title, timestamp, des=None, link=None, source=None, tags=None):
        keyevent = {
            'title'    : title,
            'des'      : des,
            'link'     : link,
            'source'   : source,
            'tags'     : tags,
            'timestamp': timestamp,
        }
        prepared_point = self._prepare_keyevnet(keyevent)
        self._send_points(prepared_point)

    def write_keyevents(self, keyevents):
        if not isinstance(keyevents, (list, tuple)):
            raise Exception('`keyevents` should be a list or tuple, got {0}'.format(type(keyevents).__name__))

        prepared_points = []
        for p in keyevents:
            prepared_points.append(self._prepare_keyevnet(p))

        self._send_points(prepared_points)

    def write_flow(self, trace_id, name, type_, timestamp, duration=None, duration_ms=None, parent=None, fields=None, tags=None):
        flow = {
            'trace_id'   : trace_id,
            'name'       : name,
            'type'       : type_,
            'duration'   : duration,
            'duration_ms': duration_ms,
            'parent'     : parent,
            'fields'     : fields,
            'tags'       : tags,
            'timestamp'  : timestamp,
        }
        prepared_point = self._prepare_flow(flow)
        self._send_points(prepared_point)

    def write_flows(self, flows):
        if not isinstance(flows, (list, tuple)):
            raise Exception('`flows` should be a list or tuple, got {0}'.format(type(flows).__name__))

        prepared_points = []
        for p in flows:
            prepared_points.append(self._prepare_flow(p))

        self._send_points(prepared_points)