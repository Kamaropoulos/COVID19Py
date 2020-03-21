# COVID19Py
Python API Wrapper for tracking Coronavirus (COVID-19, SARS-CoV-2) via https://github.com/ExpDev07/coronavirus-tracker-api

[![Downloads](https://pepy.tech/badge/covid19py)](https://pepy.tech/project/covid19py)
[![Downloads](https://pepy.tech/badge/covid19py/month)](https://pepy.tech/project/covid19py/month)
[![Downloads](https://pepy.tech/badge/covid19py/week)](https://pepy.tech/project/covid19py/week)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![HitCount](http://hits.dwyl.com/Kamaropoulos/COVID19Py.svg)](http://hits.dwyl.com/Kamaropoulos/COVID19Py)
[![GitHub stars](https://img.shields.io/github/stars/Kamaropoulos/COVID19Py.svg?style=social&label=Star)](https://github.com/Kamaropoulos/COVID19Py)

## Installation

In order install this package, simply run:

```bash
pip install COVID19Py
```

## Usage

To use COVID19Py, you first need to import the package and then create a new instance:

```python
import COVID19Py
covid19 = COVID19Py.COVID19()
```

### Getting latest amount of total confirmed cases, deaths, and recoveries:

```python
latest = covid19.getLatest()
```

### Getting all locations:

```python
locations = covid19.getLocations()
```

or:

```python
locations = covid19.getLocations(timelines=True)
```
to also get timelines.

You can also rank the results by `confirmed`, `deaths` or `recovered`.

```python
locations = covid19.getLocations(rank_by='recovered')
```

### Getting location by country code:

```python
location = covid19.getLocationByCountryCode("US")
```
or:
```python
location = covid19.getLocationByCountryCode("US", timelines=True)
```
to also get timelines.

### Getting a specific location (includes timelines by default):

```python
location = covid19.getLocationById(39)
```

### Getting all data at once:

You can also get all the available data with one command.

```python
data = covid19.getAll()
```
or:
```python
data = covid19.getAll(timelines=True)
```
to also get timelines.

`latest` will be available on `data["latest"]` and `locations` will be available on `data["locations"]`.

### Getting `latest` deltas:

When using `getAll()`, COVID19Py will also store the previous version of the retrieved data. This allows us to easily see how data changed since the last time we requested them.

```python
changes = covid19.getLatestChanges()
```
```json
{
    "confirmed": 512,
    "deaths": 16,
    "recovered": 1024
}
```
