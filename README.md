# PubTransTrack

## About

This project attempts to create a number of tools for using the [Transport API](https://www.transportapi.com/), an API for accessing publicly accessible public transport data.

- [PubTransTrack](#pubtranstrack)
  - [About](#about)
  - [Initialisationbus=api.busCreate(busdata)bus=api.busCreate(busdata)](#initialisationbusapibuscreatebusdatabusapibuscreatebusdata)
  - [`api` module](#api-module)
    - [Functions and classes](#functions-and-classes)
      - [`api.getFromATCO(ATCO)`](#apigetfromatcoatco)
        - [Example](#example)
        - [Output](#output)
      - [`api.getFromTIPLOCCRS(TIPLOCCRS)`](#apigetfromtiploccrstiploccrs)
        - [Example](#example-1)
        - [Output](#output-1)
      - [`api.busCreate(dict)`](#apibuscreatedict)
      - [`api.trainCreate(dict)`](#apitraincreatedict)

## Initialisationbus=api.busCreate(busdata)bus=api.busCreate(busdata)

To use the tools in this project, it is necessary to initialise the `apidata.json` file that the `api` package can read settings from. You can find your `appid` and `appkey` from your Transport API dashboard (provided you have signed up, of course). The `default_ATCO` parameter is used as a failover when an ATCO Code is not provided. You can set this to any valid ATCO code, an example of which is `43000983403`. Create a file called `apidata.json` in the main directory of the project with the following contents:

```json
{
    "appdata": {
        "appid": "Your App ID",
        "appkey": "Your App Key"
    },
    "default_settings": {
        "default_ATCO": "Insert an ATCO Code Here",
        "default_TIPLOCCRS": "Insert a TIPLOC or CRS Code Here"
    }
}
```

## `api` module

The `api` module is provided to give easy native Python interfacing with the Transport API. When the module is imported, the `initialise()` function is used to instantiate an object `progvars` which is of the class `initialsettings`. The aforementioned variables are read from file and can be accessed through using `api.progvars.appid`, `api.progvars.appkey` and `api.progvars.default_ATCO`. Functions existing in `__init__.py` make use of these variables by default, as the `progvars` object is global.

### Functions and classes

#### `api.getFromATCO(ATCO)`

Accepts an ATCO Code (which must be of type `str`), creates an HTTP `GET` request to the Transport API providing the defined ATCO code (and App ID and Key), gets the `json` formatted response and converts it into a Python `dict`.

##### Example

```python
import api, pprint

response=api.getFromATCO('43000983403')

pprint.pprint(response)
```

##### Output

**Note:** Results redacted after 2<sup>nd</sup> element to avoid an unnecessarily long code block, a maximum of 10 results are returned by Transport API.

```python
{'atcocode': '43000983403',
 'bearing': 'W',
 'departures': {'all': [{'aimed_departure_time': '09:51',
                         'best_departure_estimate': '09:51',
                         'date': '2020-05-23',
                         'dir': 'outbound',
                         'direction': 'Wednesbury, Wednesbury Bus Station',
                         'expected_departure_date': None,
                         'expected_departure_time': None,
                         'id': 'https://transportapi.com/v3/uk/bus/route/TNXB/40/outbound/43000983403/2020-05-23/09:51/timetable.json?app_id=[app_id]&app_key=[app_key]',
                         'line': '40',
                         'line_name': '40',
                         'mode': 'bus',
                         'operator': 'TNXB',
                         'operator_name': 'National Express West Midlands',
                         'source': 'NextBuses',
                         'status': {'cancellation': {'reason': None,
                                                     'value': False}}},
                        {'aimed_departure_time': '10:21',
                         'best_departure_estimate': '10:21',
                         'date': '2020-05-23',
                         'dir': 'outbound',
                         'direction': 'Wednesbury, Wednesbury Bus Station',
                         'expected_departure_date': None,
                         'expected_departure_time': None,
                         'id': 'https://transportapi.com/v3/uk/bus/route/TNXB/40/outbound/43000983403/2020-05-23/10:21/timetable.json?app_id=[app_id]&app_key=[app_key]',
                         'line': '40',
                         'line_name': '40',
                         'mode': 'bus',
                         'operator': 'TNXB',
                         'operator_name': 'National Express West Midlands',
                         'source': 'NextBuses',
                         'status': {'cancellation': {'reason': None,
                                                     'value': False}}},
 'indicator': '',
 'locality': 'Stone Cross, West Bromwich',
 'location': {'coordinates': [-1.98403, 52.54528], 'type': 'Point'},
 'name': 'Stone Cross',
 'request_time': '2020-05-23T09:45:50+01:00',
 'smscode': 'nwmtmgdw',
 'source': 'NextBuses',
 'stop_name': 'Stone Cross'}
```

#### `api.getFromTIPLOCCRS(TIPLOCCRS)`

Accepts a TIPLOC or CRS Code (which must be of type `str`), creates an HTTP `GET` request to the Transport API providing the defined TIPLOC/CRS code (and App ID and Key), gets the `json` formatted response and converts it into a Python `dict`.

##### Example

```python
import api, pprint

response=api.getFromTIPLOCCRS('sgb')

pprint.pprint(response)
```

##### Output

```python
{'date': '2020-05-23',
 'departures': {'all': [{'aimed_arrival_time': '18:43',  
                         'aimed_departure_time': '18:43',
                         'aimed_pass_time': None,
                         'best_arrival_estimate_mins': 5,
                         'best_departure_estimate_mins': 5,
                         'category': 'OO',
                         'destination_name': 'Kidderminster',
                         'expected_arrival_time': '19:40',
                         'expected_departure_time': '19:40',
                         'mode': 'train',
                         'operator': 'LM',
                         'operator_name': 'West Midlands Trains',
                         'origin_name': 'Dorridge',
                         'platform': '1',
                         'service': '12257320',
                         'service_timetable': {'id': 'https://transportapi.com/v3/uk/train/service/train_uid:C15528/2020-05-23/timetable.json?app_id=[app_id]&app_key=[app_key]&darwin=true&live=true'},
                         'source': 'Network Rail',
                         'status': 'LATE',
                         'train_uid': 'C15528'},
                        {'aimed_arrival_time': '19:02',
                         'aimed_departure_time': '19:03',
                         'aimed_pass_time': None,
                         'best_arrival_estimate_mins': 0,
                         'best_departure_estimate_mins': 1,
                         'category': 'OO',
                         'destination_name': 'Worcester Shrub Hill',
                         'expected_arrival_time': '19:35',
                         'expected_departure_time': '19:36',
                         'mode': 'train',
                         'operator': 'LM',
                         'operator_name': 'West Midlands Trains',
                         'origin_name': 'Dorridge',
                         'platform': '1',
                         'service': '12257320',
                         'service_timetable': {'id': 'https://transportapi.com/v3/uk/train/service/train_uid:C17003/2020-05-23/timetable.json?app_id=[app_id]&app_key=[app_key]&darwin=true&live=true'},
                         'source': 'Network Rail',
                         'status': 'LATE',
                         'train_uid': 'C17003'},
 'request_time': '2020-05-23T19:34:08+01:00',
 'station_code': 'sgb',
 'station_name': 'Smethwick Galton Bridge (Low Level)',
 'time_of_day': '19:34'}
```

**Note:** Results redacted after 2<sup>nd</sup> element to avoid an unnecessarily long code block, a maximum of 10 results are returned by Transport API.

#### `api.busCreate(dict)`

Returns a list, the elements of which are of class `bus`, with data taken from the dict returned from `api.getFromATCO(ATCO)`. The `bus` class contains five objects:


| Object        | Type                 | Definition                                                                                                                    |
| ------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `line`        | `str`                | The line "number" for the corresponding bus, i.e. "40" or "the mickleover".                                                   |
| `destination` | `str`                | The terminus for the corresponding bus, i.e. "Wednesbury, Wednesbury Bus Station" or "Derby".                                 |
| `arrival`     | `datetime.datetime`  | The best estimate of the arrival time for the bus.                                                                            |
| `eta`         | `datetime.timedelta` | The difference in time between the best estimate for the arrival time of the bus and the current time.                        |
| `cancel`      | `bool`               | `True` or `False` depending on whether the bus has been cancelled or not. If data is not available, this defaults to `False`. |

#### `api.trainCreate(dict)`

Returns a list, the elements of which are of class `train`, with the data taken form the dict returned from `api.getFromTIPLOCCRS(TIPLOCCRS)`. The `train` class contains seven objects:

| Object        | Type                | Definition                                                            |
| ------------- | ------------------- | --------------------------------------------------------------------- |
| `arrival`     | `datetime.datetime` | The best estimate of the arrival time for the train.                  |
| `eta`         | `int`               | An `int` with minutes until the train arrives.                        |
| `operator`    | `str`               | The TOC operating the train.                                          |
| `destination` | `str`               | The terminus station for the train.                                   |
| `origin`      | `str`               | The origin station for the train.                                     |
| `status`      | `str`               | A short description of the train's current status provided by Darwin. |
| `uid`         | `str`               | The UID of the train as provided in TRUST.                            |