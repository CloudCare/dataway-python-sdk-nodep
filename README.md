# DataFlux DataWay Python SDK -nodep

Python 版 DataFlux DataWay SDK。

[English Version](README-en.md)

## 特性

1. 兼容 Python 2.x 和 Python 3.x，在以下版本中通过测试：
    - `2.6.9` / `2.7.15`
    - `3.4.10` / `3.5.9` / `3.6.9` / `3.7.5` / `3.8.0`

2. 兼容不同单位的时间戳：
    - 秒
    - 毫秒（1/1000 秒）
    - 微秒（1/1000,000 秒）
    - 纳秒（1/1000,000,000 秒）

3. 关键事件（`Keyevent`）/ 流程行为（`FLow`）/ 告警（`Alert`）支持。

4. DataWay 认证支持。

5. HTTP/HTTPS 支持。

6. 单文件即可使用。

7. 无第三方包依赖。

## 安装

无需通过 `pip`/`easy_install`，只要拷贝文件`dataway.py`到项目中，引用即可使用。

见 [example.py](example.py)

## 简单示例

```python
from dataway import DataWay

dw = DataWay(url='http://localhost:9528/v1/write/metrics?token=xxxxxx')

# 写入一个数据点
dw.write_point(measurement='M1', tags={'T1': 'X'}, fields={'F1': 'A'}, timestamp=1577808001)

# 写入多个数据点
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

## API文档

###### *class* `DataWay(url=None, host=None, port=None, protocol=None, path=None, token=None, rp=None, access_key=None, secret_key=None, debug=False)`

DataWay 类

|            参数           |     类型    | 是否必须 |        默认值         |                                      说明                                     |
|---------------------------|-------------|----------|-----------------------|-------------------------------------------------------------------------------|
| `url`                     | `str`       | 可选     | `None`                | DataWay 完整地址，如：`"http://localhost:9528/v1/write/metrics?token=xxxxxx"` |
| `host`                    | `str`       | 可选     | `"localhost"`         | DataWay 主机地址                                                              |
| `port`                    | `int`       | 可选     | `9528`                | DataWay 主机端口                                                              |
| `protocol`                | `str`       | 可选     | `"http"`              | DataWay 访问协议。`"http"`/`"https"`                                          |
| `path`                    | `str`       | 可选     | `"/v1/write/metrics"` | DataWay 数据上报路径                                                          |
| `token`                   | `str`       | 可选     | `None`                | DataFlux 工作空间上报Token。只有OpenWay和内部DataWay需要填写                  |
| `rp`                      | `str`       | 可选     | `None`                | 写入目标`retention policy`                                                    |
| `access_key`/`secret_key` | `str`/`str` | 可选     | `None`/`None`         | DataWay 认证用 AccessKey 和 SecretKey                                         |
| `debug`                   | `bool`      | 可选     | `False`               | 是否打印详细调试信息                                                          |

以下两种初始化方式等价：
- `DataWay(url="http://localhost:9528/v1/write/metrics?token=xxxxxx")`
- `DataWay(host="localhost", port="9528", protocol="http", path="/v1/write/metrics", token='xxxxxx')`

`token`可以在`url`中作为参数出现，或者通过`token`传递。

`access_key`/`secret_key` 只有在 DataWay 开启认证后才需要填写。DataWay 开启认证方式如下：

```shell
sudo vim /usr/local/cloudcare/forethought/dataway/dataway.yaml
```

修改以下内容

```yaml
routes_config:
    - name: default
      ak_open: false # true 为开启认证；false 为关闭认证
      lua:
```

最后，AccessKey 和 SecretKey 即为文件中的`access_key`和`secret_key`。



---



###### *method* `DataWay.write_point(measurement, tags=None, fields=None, timestamp=None)`

写入数据点

|      参数     |         类型         | 是否必须 |  默认值  |                               说明                              |
|---------------|----------------------|----------|----------|-----------------------------------------------------------------|
| `measurement` | `str`                | 必须     |          | 指标集名称                                                      |
| `tags`        | `dict`               | 可选     | `None`   | 标签。键名和键值必须都为字符串                                  |
| `fields`      | `dict`               | 可选     | `None`   | 指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |
| `timestamp`   | `int`/`long`/`float` | 可选     | 当前时间 | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒        |



---



###### *method* `DataWay.write_points(points)`

写入多个数据点

|            参数            |         类型         | 是否必须 |  默认值  |                               说明                              |
|----------------------------|----------------------|----------|----------|-----------------------------------------------------------------|
| `points`                   | `list`               | 必须     |          | 数据点列表                                                      |
| `points[#]`                | `dict`               | 必须     |          | 数据点                                                          |
| `points[#]["measurement"]` | `str`                | 必须     |          | 指标集名称                                                      |
| `points[#]["tags"]`        | `dict`               | 可选     | `None`   | 标签。键名和键值必须都为字符串                                  |
| `points[#]["fields"]`      | `dict`               | 可选     | `None`   | 指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |
| `points[#]["timestamp"]`   | `int`/`long`/`float` | 可选     | 当前时间 | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒        |



---



###### *method* `DataWay.write_keyevent(title, timestamp, duration=None, duration_ms=None, event_id=None, source=None, status=None, rule_id=None, rule_name=None, type_=None, alert_item_tags=None, action_type=None, content=None, tags=None, fields=None)`

写入关键事件

|        参数       |         类型         |  是否必须  | 默认值 |                               说明                              |
|-------------------|----------------------|------------|--------|-----------------------------------------------------------------|
| `title`           | `str`                | 必须       |        | 标题                                                            |
| `timestamp`       | `int`/`long`/`float` | 必须       |        | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒        |
| `duration`        | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（秒）                              |
| `duration_ms`     | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（毫秒）                            |
| `event_id`        | `str`                | 可选       | `None` | 事件ID                                                          |
| `source`          | `str`                | 可选       | `None` | 来源                                                            |
| `status`          | `str`                | 可选       | `None` | "critical" / "error" / "warning" / "info" / "ok" 之一           |
| `rule_id`         | `str`                | 可选       | `None` | 规则ID                                                          |
| `rule_name`       | `str`                | 可选       | `None` | 规则名称                                                        |
| `type_`           | `str`                | 可选       | `None` | 类型（注意：由于`type`在Python中为关键字，此处取`type_`）       |
| `alert_item_tags` | `str`                | 可选       | `None` | 告警对象标签。键名和键值必须都为字符串                          |
| `action_type`     | `str`                | 可选       | `None` | 动作类型                                                        |
| `content`         | `str`                | 可选       | `None` | 内容                                                            |
| `tags`            | `dict`               | 可选       | `None` | 标签。键名和键值必须都为字符串                                  |
| `fields`          | `dict`               | 可选       | `None` | 指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |



---



###### *method* `DataWay.write_keyevents(keyevents)`

写入多个关键事件

|              参数             |         类型         |  是否必须  | 默认值 |                               说明                              |
|-------------------------------|----------------------|------------|--------|-----------------------------------------------------------------|
| `keyevents`                   | `list`               | 必须       |        | 关键事件列表                                                    |
| `keyevents[#]`                | `dict`               | 必须       |        | 关键事件                                                        |
| `keyevents[#]title`           | `str`                | 必须       |        | 标题                                                            |
| `keyevents[#]timestamp`       | `int`/`long`/`float` | 必须       |        | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒        |
| `keyevents[#]duration`        | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（秒）                              |
| `keyevents[#]duration_ms`     | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（毫秒）                            |
| `keyevents[#]event_id`        | `str`                | 可选       | `None` | 事件ID                                                          |
| `keyevents[#]source`          | `str`                | 可选       | `None` | 来源                                                            |
| `keyevents[#]status`          | `str`                | 可选       | `None` | "critical" / "error" / "warning" / "info" / "ok" 之一           |
| `keyevents[#]rule_id`         | `str`                | 可选       | `None` | 规则ID                                                          |
| `keyevents[#]rule_name`       | `str`                | 可选       | `None` | 规则名称                                                        |
| `keyevents[#]type`            | `str`                | 可选       | `None` | 类型                                                            |
| `keyevents[#]alert_item_tags` | `str`                | 可选       | `None` | 告警对象标签。键名和键值必须都为字符串                          |
| `keyevents[#]action_type`     | `str`                | 可选       | `None` | 动作类型                                                        |
| `keyevents[#]content`         | `str`                | 可选       | `None` | 内容                                                            |
| `keyevents[#]tags`            | `dict`               | 可选       | `None` | 标签。键名和键值必须都为字符串                                  |
| `keyevents[#]fields`          | `dict`               | 可选       | `None` | 指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |



---



###### *method* `DataWay.write_flow(app, trace_id, name, timestamp, duration=None, duration_ms=None, parent=None, fields=None, tags=None)`

写入流程行为

|      参数     |         类型         |  是否必须  | 默认值 |                                 说明                                |
|---------------|----------------------|------------|--------|---------------------------------------------------------------------|
| `app`         | `str`                | 必须       |        | 应用名                                                              |
| `trace_id`    | `str`                | 必须       |        | 标示一个流程单的唯一ID                                              |
| `name`        | `str`                | 必须       |        | 节点名称                                                            |
| `timestamp`   | `int`/`long`/`float` | 必须       |        | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒            |
| `duration`    | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（秒）                                  |
| `duration_ms` | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（毫秒）                                |
| `parent`      | `str`                | 可选       | `None` | 上一个节点的名称。第一个节点不用上报                                |
| `tags`        | `dict`               | 可选       | `None` | 额外标签。键名和键值必须都为字符串                                  |
| `fields`      | `dict`               | 可选       | `None` | 额外指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |

`duration`和`duration_ms`两者必须填一个



---



###### *method* `DataWay.write_flows(flows)`

写入多个流程行为

|            参数           |         类型         |  是否必须  | 默认值 |                                 说明                                |
|---------------------------|----------------------|------------|--------|---------------------------------------------------------------------|
| `flows`                   | `list`               | 必须       |        | 流程行为列表                                                        |
| `flows[#]`                | `dict`               | 必须       |        | 流程行为                                                            |
| `flows[#]["app"]`         | `str`                | 必须       |        | 应用名                                                              |
| `flows[#]["trace_id"]`    | `str`                | 必须       |        | 标示一个流程单的唯一ID                                              |
| `flows[#]["name"]`        | `str`                | 必须       |        | 节点名称                                                            |
| `flows[#]["timestamp"]`   | `int`/`long`/`float` | 必须       |        | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒            |
| `flows[#]["duration"]`    | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（秒）                                  |
| `flows[#]["duration_ms"]` | `int`/`long`         | 必须二选一 |        | 在当前节点滞留时间或持续时间（毫秒）                                |
| `flows[#]["parent"]`      | `str`                | 可选       | `None` | 上一个节点的名称。第一个节点不用上报                                |
| `flows[#]["tags"]`        | `dict`               | 可选       | `None` | 额外标签。键名和键值必须都为字符串                                  |
| `flows[#]["fields"]`      | `dict`               | 可选       | `None` | 额外指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |

## 声明

我们从 [six](https://github.com/benjaminp/six) 摘录了部分代码，主要用于实现 Python 2.x/3.x 兼容。

## 许可协议

[Apache License Version 2.0](LICENSE)
