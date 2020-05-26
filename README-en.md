# DataFlux DataWay Python SDK -nodep

A DataFlux DataWay SDK for Python.

[中文版](README.md)

## Feature

1. Compatible with Python 2.x and Python 3.x. Tested in Python versions:
    - `2.6.9` / `2.7.15`
    - `3.4.10` / `3.5.9` / `3.6.9` / `3.7.5` / `3.8.0`

2. Compatible with different timestamp:
    - second
    - millisecond (1/1000 second)
    - microsecond (1/1000,000 second)
    - nanosecond (1/1000,000,000 second)

3. `Keyevent` / `FLow` / `Alert` Support.

4. DataWay Authorization support.

5. HTTP/HTTPS support.

6. All-in-one file.

7. No third-party package dependency.

## Installation

No need to `pip`/`easy_install`, just copy the only file `dataway.py` to your project and `import` it.

See [example.py](example.py)

## Quick Example

```python
from dataway import DataWay

dw = DataWay(url='http://localhost:9528/v1/write/metrics?token=xxxxxx')

# Write a point
dw.write_point(measurement='M1', tags={'T1': 'X'}, fields={'F1': 'A'}, timestamp=1577808001)

# Write many points
dw.write_points([
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
    }
])
```

## API Document

###### *class* `DataWay(url=None, host=None, port=None, protocol=None, path=None, token=None, rp=None, access_key=None, secret_key=None, debug=False)`

DataWay class

|         Parameter         |     Type    | Required |     Default Value     |                                      Description                                      |
|---------------------------|-------------|----------|-----------------------|---------------------------------------------------------------------------------------|
| `url`                     | `str`       | Optional | `None`                | DataWay full access URL, e.g. `"http://localhost:9528/v1/write/metrics?token=xxxxxx"` |
| `host`                    | `str`       | Optional | `"localhost"`         | DataWay host                                                                          |
| `port`                    | `int`       | Optional | `9528`                | DataWay port                                                                          |
| `protocol`                | `str`       | Optional | `"http"`              | DataWay protocol. `"http"`/`"https"`                                                  |
| `path`                    | `str`       | Optional | `"/v1/write/metrics"` | DataWay report path                                                                   |
| `token`                   | `str`       | Optional | `None`                | DataFlux Workspace Token. Only for OpenWay and Internal DataWay                       |
| `rp`                      | `str`       | Optional | `None`                | Target `retention policy`                                                             |
| `access_key`/`secret_key` | `str`/`str` | Optional | `None`/`None`         | DataWay AccessKey and SecretKey for authorization                                     |
| `debug`                   | `bool`      | Optional | `False`               | Print detailed debug info or not                                                      |

The following instantiation are equivalent:
- `DataWay(url="http://localhost:9528/v1/write/metrics?token=xxxxxx")`
- `DataWay(host="localhost", port="9528", protocol="http", path="/v1/write/metrics", token='xxxxxx')`

`token` can be place in `url` or be passed as `token` parameter.

`access_key`/`secret_key` is required when the authorization of DataWay opened. To open the authorization of DataWay:

```shell
sudo vim /usr/local/cloudcare/forethought/dataway/dataway.yaml
```

Change the content

```yaml
routes_config:
    - name: default
      ak_open: false # set true to open, false to close
      lua:
```

Finally, the AccessKey and SecretKey are the `access_key` and `secret_key` in the YAML file.



---



###### *method* `DataWay.write_point(measurement, tags=None, fields=None, timestamp=None)`

Write one point

|   Parameter   |         Type         | Required |   Default Value   |                                                 Description                                                  |
|---------------|----------------------|----------|-------------------|--------------------------------------------------------------------------------------------------------------|
| `measurement` | `str`                | Required |                   | measurement                                                                                                  |
| `tags`        | `dict`               | Optional | `None`            | tags. Both key and value should be a string                                                                  |
| `fields`      | `dict`               | Optional | `None`            | fields. Key should be a string, value should be a string/integer/float/boolean value                         |
| `timestamp`   | `int`/`long`/`float` | Optional | Current Timestamp | timestamp, Support second/millisecond/microsecond/nanosecond. SDK will detect and auto convert to nanosecond |



---



###### *method* `DataWay.write_points(points)`

Write many points

|         Parameter          |         Type         | Required |   Default Value   |                                                 Description                                                  |
|----------------------------|----------------------|----------|-------------------|--------------------------------------------------------------------------------------------------------------|
| `points`                   | `list`               | Required |                   | data point list                                                                                              |
| `points[#]`                | `dict`               | Required |                   | data point data                                                                                              |
| `points[#]["measurement"]` | `str`                | Required |                   | measurement                                                                                                  |
| `points[#]["tags"]`        | `dict`               | Optional | `None`            | tags. Both key and value should be a string                                                                  |
| `points[#]["fields"]`      | `dict`               | Optional | `None`            | fields. Key should be a string, value should be a string/integer/float/boolean value                         |
| `points[#]["timestamp"]`   | `int`/`long`/`float` | Optional | Current Timestamp | timestamp, Support second/millisecond/microsecond/nanosecond. SDK will detect and auto convert to nanosecond |



---


###### *method* `DataWay.write_keyevent(title, timestamp, event_id=None, source=None, status=None, rule_id=None, rule_name=None, type_=None, alert_item_tags=None, action_type=None, content=None, suggestion=None, duration=None, duration_ms=None, dimensions=None, tags=None, fields=None)`

Write a key event

|     Parameter     |         Type         | Required |   Default Value   |                                                 Description                                                  |
|-------------------|----------------------|----------|-------------------|--------------------------------------------------------------------------------------------------------------|
| `title`           | `str`                | Required |                   | title                                                                                                        |
| `timestamp`       | `int`/`long`/`float` | Optional | Current Timestamp | timestamp, Support second/millisecond/microsecond/nanosecond. SDK will detect and auto convert to nanosecond |
| `event_id`        | `str`                | Optional | `None`            | event ID                                                                                                     |
| `source`          | `str`                | Optional | `None`            | source                                                                                                       |
| `status`          | `str`                | Optional | `None`            | one of "critical" / "error" / "warning" / "info" / "ok"                                                      |
| `rule_id`         | `str`                | Optional | `None`            | rule ID                                                                                                      |
| `rule_name`       | `str`                | Optional | `None`            | rule name                                                                                                    |
| `type_`           | `str`                | Optional | `None`            | type (Note: `type` as a keyword of Python, here use `type_`)                                                 |
| `alert_item_tags` | `str`                | Optional | `None`            | alert item extra tags. Both key and value should be a string                                                 |
| `action_type`     | `str`                | Optional | `None`            | action type                                                                                                  |
| `content`         | `str`                | Optional | `None`            | content                                                                                                      |
| `suggestion`      | `str`                | Optional | `None`            | suggestion                                                                                                   |
| `duration`        | `int`/`long`         | Optional | `None`            | duration of the flow on the node (second)                                                                    |
| `duration_ms`     | `int`/`long`         | Optional | `None`            | duration of the flow on the node (millisecond)                                                               |
| `dimensions`      | [`str`]              | Optional | `None`            | dimensions                                                                                                   |
| `tags`            | `dict`               | Optional | `None`            | tags. Both key and value should be a string                                                                  |
| `fields`          | `dict`               | Optional | `None`            | fields. Key should be a string, value should be a string/integer/float/boolean value                         |



---



###### *method* `DataWay.write_keyevents(keyevents)`

Write many key events

|           Parameter           |         Type         | Required |   Default Value   |                                                 Description                                                  |
|-------------------------------|----------------------|----------|-------------------|--------------------------------------------------------------------------------------------------------------|
| `keyevents`                   | `list`               | Required |                   | key event list                                                                                               |
| `keyevents[#]`                | `dict`               | Required |                   | key event data                                                                                               |
| `keyevents[#]title`           | `str`                | Required |                   | title                                                                                                        |
| `keyevents[#]timestamp`       | `int`/`long`/`float` | Optional | Current Timestamp | timestamp, Support second/millisecond/microsecond/nanosecond. SDK will detect and auto convert to nanosecond |
| `keyevents[#]event_id`        | `str`                | Optional | `None`            | event ID                                                                                                     |
| `keyevents[#]source`          | `str`                | Optional | `None`            | source                                                                                                       |
| `keyevents[#]status`          | `str`                | Optional | `None`            | one of "critical" / "error" / "warning" / "info" / "ok"                                                      |
| `keyevents[#]rule_id`         | `str`                | Optional | `None`            | rule ID                                                                                                      |
| `keyevents[#]rule_name`       | `str`                | Optional | `None`            | rule name                                                                                                    |
| `keyevents[#]type`            | `str`                | Optional | `None`            | type                                                                                                         |
| `keyevents[#]alert_item_tags` | `str`                | Optional | `None`            | alert item extra tags. Both key and value should be a string                                                 |
| `keyevents[#]action_type`     | `str`                | Optional | `None`            | action type                                                                                                  |
| `keyevents[#]content`         | `str`                | Optional | `None`            | content                                                                                                      |
| `keyevents[#]suggestion`      | `str`                | Optional | `None`            | suggestion                                                                                                   |
| `keyevents[#]duration`        | `int`/`long`         | Optional | `None`            | duration of the flow on the node (second)                                                                    |
| `keyevents[#]duration_ms`     | `int`/`long`         | Optional | `None`            | duration of the flow on the node (millisecond)                                                               |
| `keyevents[#]dimensions`      | [`str`]              | Optional | `None`            | dimensions                                                                                                   |
| `keyevents[#]tags`            | `dict`               | Optional | `None`            | tags. Both key and value should be a string                                                                  |
| `keyevents[#]fields`          | `dict`               | Optional | `None`            | fields. Key should be a string, value should be a string/integer/float/boolean value                         |



---



###### *method* `DataWay.write_flow(app, trace_id, name, timestamp, duration=None, duration_ms=None, parent=None, fields=None, tags=None)`

Write a flow

|   Parameter   |         Type         |   Required  | Default Value |                                                 Description                                                  |
|---------------|----------------------|-------------|---------------|--------------------------------------------------------------------------------------------------------------|
| `app`         | `str`                | Required    |               | app name                                                                                                     |
| `trace_id`    | `str`                | Required    |               | flow trace ID                                                                                                |
| `name`        | `str`                | Required    |               | node name                                                                                                    |
| `timestamp`   | `int`/`long`/`float` | Required    |               | timestamp, Support second/millisecond/microsecond/nanosecond. SDK will detect and auto convert to nanosecond |
| `duration`    | `int`/`long`         | Alternative |               | duration of the flow on the node (second)                                                                    |
| `duration_ms` | `int`/`long`         | Alternative |               | duration of the flow on the node (millisecond)                                                               |
| `parent`      | `str`                | Optional    | `None`        | previous node name. The first node do not have one                                                           |
| `tags`        | `dict`               | Optional    | `None`        | extra tags. Both key and value should be a string                                                            |
| `fields`      | `dict`               | Optional    | `None`        | extra fields. Key should be a string, value should be a string/integer/float/boolean value                   |

Either `duration` or `duration_ms` should be spcified.



---



###### *method* `DataWay.write_flows(flows)`

Write many flows

|         Parameter         |         Type         |   Required  | Default Value |                                                 Description                                                  |
|---------------------------|----------------------|-------------|---------------|--------------------------------------------------------------------------------------------------------------|
| `flows`                   | `list`               | Required    |               | flow list                                                                                                    |
| `flows[#]`                | `dict`               | Required    |               | flow data                                                                                                    |
| `flows[#]["app"]`         | `str`                | Required    |               | app name                                                                                                     |
| `flows[#]["trace_id"]`    | `str`                | Required    |               | flow trace ID                                                                                                |
| `flows[#]["name"]`        | `str`                | Required    |               | node name                                                                                                    |
| `flows[#]["timestamp"]`   | `int`/`long`/`float` | Required    |               | timestamp, Support second/millisecond/microsecond/nanosecond. SDK will detect and auto convert to nanosecond |
| `flows[#]["duration"]`    | `int`/`long`         | Alternative |               | duration of the flow on the node (second)                                                                    |
| `flows[#]["duration_ms"]` | `int`/`long`         | Alternative |               | duration of the flow on the node (millisecond)                                                               |
| `flows[#]["parent"]`      | `str`                | Optional    | `None`        | previous node name. The first node do not have one                                                           |
| `flows[#]["tags"]`        | `dict`               | Optional    | `None`        | extra tags. Both key and value should be a string                                                            |
| `flows[#]["fields"]`      | `dict`               | Optional    | `None`        | extra fields. Key should be a string, value should be a string/integer/float/boolean value                   |

## Announcement

We picked some code from [six](https://github.com/benjaminp/six) for Python 2.x/3.x compatibility.

## License

[Apache License Version 2.0](LICENSE)
