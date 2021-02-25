# DataFlux DataWay Python SDK -nodep

Python 版 DataFlux DataWay SDK。

## 特性

1. 兼容不同单位的时间戳：
    - 秒
    - 毫秒（1/1000 秒）
    - 微秒（1/1000,000 秒）
    - 纳秒（1/1000,000,000 秒）

2. Low-Level API 支持，包括：
    - 发送GET请求
    - 发送行协议POST请求
    - 发送JSON POST请求

3. High-Level API 支持，包括：
    - 写入指标数据（`metric`/`point`）
    - 写入关键事件数据（`keyevent`）

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

dw = DataWay(url='http://localhost:9528/v1/write/metric?token=xxxxxx')

# 写入指标数据
dw.write_metric(measurement='M1', tags={'T1': 'X'}, fields={'F1': 'A'}, timestamp=1577808001)

# 批量写入指标数据
dw.write_metrics([
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

### 通用

#### *class* `DataWay(url=None, host=None, port=None, protocol=None, path=None, token=None, rp=None, access_key=None, secret_key=None, debug=False, dry_run=False)`

DataWay 类

|            参数           |     类型    | 是否必须 |        默认值        |                                     说明                                     |
|---------------------------|-------------|----------|----------------------|------------------------------------------------------------------------------|
| `url`                     | `str`       | 可选     | `None`               | DataWay 完整地址，如：`"http://localhost:9528/v1/write/metric?token=xxxxxx"` |
| `host`                    | `str`       | 可选     | `"localhost"`        | DataWay 主机地址                                                             |
| `port`                    | `int`       | 可选     | `9528`               | DataWay 主机端口                                                             |
| `protocol`                | `str`       | 可选     | `"http"`             | DataWay 访问协议。`"http"`/`"https"`                                         |
| `path`                    | `str`       | 可选     | `"/v1/write/metric"` | DataWay 数据上报路径                                                         |
| `token`                   | `str`       | 可选     | `None`               | DataFlux 工作空间上报Token。只有OpenWay和内部DataWay需要填写                 |
| `rp`                      | `str`       | 可选     | `None`               | 写入目标`retention policy`                                                   |
| `access_key`/`secret_key` | `str`/`str` | 可选     | `None`/`None`        | DataWay 认证用 AccessKey 和 SecretKey                                        |
| `debug`                   | `bool`      | 可选     | `False`              | 是否打印详细调试信息                                                         |
| `dry_run`                 | `bool`      | 可选     | `False`              | 是否仅以演习方式运行（不实际发送HTTP请求）                                   |


以下两种初始化方式等价：
- `DataWay(url="http://localhost:9528/v1/write/metric?token=xxxxxx")`
- `DataWay(host="localhost", port="9528", protocol="http", path="/v1/write/metric", token='xxxxxx')`

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



### Low-Level API

#### *method* `DataWay.get(path, query=None, headers=None)`

发送GET请求

|    参数   |  类型  | 是否必须 | 默认值 |          说明         |
|-----------|--------|----------|--------|-----------------------|
| `path`    | `str`  | 必须     |        | 请求路径，如：`/ping` |
| `query`   | `dict` | 可选     | `None` | 请求Query参数         |
| `headers` | `dict` | 可选     | `None` | 请求Headers参数       |



---



#### *method* `DataWay.post_line_protocol(path, points, path=None, query=None, headers=None, with_rp=False)`

使用POST方式发送行协议数据

|            参数            |         类型         | 是否必须 |           默认值            |                               说明                              |
|----------------------------|----------------------|----------|-----------------------------|-----------------------------------------------------------------|
| `points`                   | `list`               | 必须     |                             | 数据点列表                                                      |
| `points[#]`                | `dict`               | 必须     |                             | 数据点                                                          |
| `points[#]["measurement"]` | `str`                | 必须     |                             | 指标集名称                                                      |
| `points[#]["tags"]`        | `dict`               | 可选     | `None`                      | 标签。键名和键值必须都为字符串                                  |
| `points[#]["fields"]`      | `dict`               | 必须     |                             | 指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |
| `points[#]["timestamp"]`   | `int`/`long`/`float` | 可选     | 当前时间                    | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒        |
| `path`                     | `str`                | 可选     | `DataWay`实例化时指定的路径 | 请求路径，如：`/v1/write/keyevent`                              |
| `query`                    | `dict`               | 可选     | `None`                      | 请求Query参数                                                   |
| `headers`                  | `dict`               | 可选     | `None`                      | 请求Headers参数                                                 |
| `with_rp`                  | `bool`               | 可选     | `False`                     | 是否自动附带`rp`参数                                            |

*注意：由于SDK会自动将时间戳`timestamp`转换为纳秒，因此请勿在`query`中额外指定`precision`参数*



---



#### *method* `DataWay.post_json(path, json_obj, path, query=None, headers=None, with_rp=False)`

使用POST方式发送JSON数据

|    参数    |       类型      | 是否必须 | 默认值  |            说明            |
|------------|-----------------|----------|---------|----------------------------|
| `json_obj` | `list` / `dict` | 必须     |         | JSON数据                   |
| `path`     | `str`           | 必须     |         | 请求路径，如：`/v1/object` |
| `query`    | `dict`          | 可选     | `None`  | 请求Query参数              |
| `headers`  | `dict`          | 可选     | `None`  | 请求Headers参数            |
| `with_rp`  | `bool`          | 可选     | `False` | 是否自动附带`rp`参数       |




### High-Level API

#### *method* `DataWay.write_metric(measurement, tags=None, fields=None, timestamp=None)`

写入指标数据

|      参数     |         类型         | 是否必须 |  默认值  |                               说明                              |
|---------------|----------------------|----------|----------|-----------------------------------------------------------------|
| `measurement` | `str`                | 必须     |          | 指标集名称                                                      |
| `tags`        | `dict`               | 可选     | `None`   | 标签。键名和键值必须都为字符串                                  |
| `fields`      | `dict`               | 可选     | `None`   | 指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |
| `timestamp`   | `int`/`long`/`float` | 可选     | 当前时间 | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒        |



---



#### *method* `DataWay.write_metrics(data)`

批量写入指标数据

|           参数           |         类型         | 是否必须 |  默认值  |                               说明                              |
|--------------------------|----------------------|----------|----------|-----------------------------------------------------------------|
| `data`                   | `list`               | 必须     |          | 数据点列表                                                      |
| `data[#]`                | `dict`               | 必须     |          | 数据点                                                          |
| `data[#]["measurement"]` | `str`                | 必须     |          | 指标集名称                                                      |
| `data[#]["tags"]`        | `dict`               | 可选     | `None`   | 标签。键名和键值必须都为字符串                                  |
| `data[#]["fields"]`      | `dict`               | 可选     | `None`   | 指标。键名必须为字符串，键值可以为字符串/整数/浮点数/布尔值之一 |
| `data[#]["timestamp"]`   | `int`/`long`/`float` | 可选     | 当前时间 | 时间戳，支持秒/毫秒/微秒/纳秒。SDK会判断并自动转换为纳秒        |



---



#### *method* `DataWay.write_point(measurement, tags=None, fields=None, timestamp=None)`

「写入指标数据」方法`DataWay.write_metric(...)`的别名



---



#### *method* `DataWay.write_points(points)`

「批量写入指标数据」方法`DataWay.write_metric(...)`的别名

## 声明

我们从 [six](https://github.com/benjaminp/six) 摘录了部分代码，主要用于实现 Python 2.x/3.x 兼容。

## 许可协议

[Apache License Version 2.0](LICENSE)
